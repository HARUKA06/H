import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from yt_dlp import YoutubeDL
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from config import *
from queue import add_to_queue, get_queue, pop_next, clear_queue

app = Client("vc_spotify_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
vc = PyTgCalls(app)

spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

ydl_opts = {"format": "bestaudio", "quiet": True, "outtmpl": "downloads/%(title)s.%(ext)s"}

@vc.on_stream_end()
async def stream_ended(_, update):
    next_track = pop_next(update.chat_id)
    if next_track:
        await vc.change_stream(update.chat_id, InputAudioStream(next_track["file"]))

@app.on_message(filters.command("play") & filters.group)
async def play(_, msg):
    query = " ".join(msg.command[1:])
    if not query:
        return await msg.reply("🎵 Give a song name or Spotify link.")

    if "spotify.com" in query:
        track = spotify.track(query)
        query = f"{track['name']} {track['artists'][0]['name']}"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        file = ydl.prepare_filename(info)
        title = info['title']

    add_to_queue(msg.chat.id, title, file)
    if not vc.active_calls.get(msg.chat.id):
        await vc.join_group_call(msg.chat.id, InputAudioStream(file))
        await msg.reply(f"▶️ Now playing: **{title}**")
    else:
        await msg.reply(f"✅ Added to queue: **{title}**")

@app.on_message(filters.command("pause") & filters.group)
async def pause(_, msg):
    await vc.pause_stream(msg.chat.id)
    await msg.reply("⏸ Music paused.")

@app.on_message(filters.command("resume") & filters.group)
async def resume(_, msg):
    await vc.resume_stream(msg.chat.id)
    await msg.reply("▶️ Music resumed.")

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, msg):
    clear_queue(msg.chat.id)
    await vc.leave_group_call(msg.chat.id)
    await msg.reply("⏹ Music stopped and VC left.")

@app.on_message(filters.command("skip") & filters.group)
async def skip(_, msg):
    next_track = pop_next(msg.chat.id)
    if next_track:
        await vc.change_stream(msg.chat.id, InputAudioStream(next_track["file"]))
        await msg.reply(f"⏭ Skipping to: **{next_track['title']}**")
    else:
        await vc.leave_group_call(msg.chat.id)
        await msg.reply("❌ No more songs in the queue.")

@app.on_message(filters.command("queue") & filters.group)
async def show_queue(_, msg):
    q = get_queue(msg.chat.id)
    if not q:
        return await msg.reply("📭 Queue is empty.")
    text = "**🎶 Current Queue:**\n" + "\n".join([f"{i+1}. {s['title']}" for i, s in enumerate(q)])
    await msg.reply(text)

@app.on_message(filters.command("clear") & filters.group)
async def clear(_, msg):
    clear_queue(msg.chat.id)
    await msg.reply("🧹 Queue cleared.")

vc.start()
app.run()
