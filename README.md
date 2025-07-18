
2 weeks ago

Create main.py
        return None



async def is_assistant_in_chat(chat_id):
    try:
        member = await assistant.get_chat_member(chat_id, ASSISTANT_USERNAME)
        return member.status is not None
    except Exception as e:
        error_message = str(e)
        if "USER_BANNED" in error_message or "Banned" in error_message:
            return "banned"
        elif "USER_NOT_PARTICIPANT" in error_message or "Chat not found" in error_message:
            return False
        print(f"Error checking assistant in chat: {e}")
        return False

async def is_api_assistant_in_chat(chat_id):
    try:
        member = await bot.get_chat_member(chat_id, API_ASSISTANT_USERNAME)
        return member.status is not None
    except Exception as e:
        print(f"Error checking API assistant in chat: {e}")
        return False
    
def iso8601_to_seconds(iso_duration):
    try:
        duration = isodate.parse_duration(iso_duration)
        return int(duration.total_seconds())
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return 0


def iso8601_to_human_readable(iso_duration):
    try:
        duration = isodate.parse_duration(iso_duration)
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"
        return f"{minutes}:{seconds:02}"
    except Exception as e:
        return "Unknown duration"

async def fetch_youtube_link(query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}{query}") as response:
                if response.status == 200:
                    data = await response.json()
                    # Check if the API response contains a playlist
                    if "playlist" in data:
                        return data
                    else:
                        return (
                            data.get("link"),
                            data.get("title"),
                            data.get("duration"),
                            data.get("thumbnail")
                        )
                else:
                    raise Exception(f"API returned status code {response.status}")
    except Exception as e:
        raise Exception(f"Failed to fetch YouTube link: {str(e)}")


    
async def fetch_youtube_link_backup(query):
    if not BACKUP_SEARCH_API_URL:
        raise Exception("Backup Search API URL not configured")
    # Build the correct URL:
    backup_url = (
        f"{BACKUP_SEARCH_API_URL.rstrip('/')}"
        f"/search?title={urllib.parse.quote(query)}"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(backup_url, timeout=30) as resp:
                if resp.status != 200:
                    raise Exception(f"Backup API returned status {resp.status}")
                data = await resp.json()
                # Mirror primary API’s return:
                if "playlist" in data:
                    return data
                return (
                    data.get("link"),
                    data.get("title"),
                    data.get("duration"),
                    data.get("thumbnail")
                )
    except Exception as e:
        raise Exception(f"Backup Search API error: {e}")
2 weeks ago

Update main.py
    
BOT_NAME = os.environ.get("BOT_NAME", "Frozen Music")
BOT_LINK = os.environ.get("BOT_LINK", "https://t.me/vcmusiclubot")
2 weeks ago

Create main.py

4 days ago

Update main.py
from pyrogram.errors import UserAlreadyParticipant, RPCError

4 days ago

Update main.py
async def invite_assistant(chat_id, invite_link, processing_message):
    """
    Internally invite the assistant to the chat by using the assistant client to join the chat.
4 days ago

Update main.py
    If the assistant is already in the chat, treat as success.
    On other errors, display and return False.
4 days ago

Update main.py
    """
2 weeks ago

Create main.py
    try:
4 days ago

Update main.py
        # Attempt to join via invite link
4 days ago

Update main.py
        await assistant.join_chat(invite_link)
4 days ago

Update main.py
        return True
4 days ago

Update main.py

    except UserAlreadyParticipant:
        # Assistant is already in the chat, no further action needed
        return True

    except RPCError as e:
        # Handle other Pyrogram RPC errors
        error_message = f"❌ Error while inviting assistant: Telegram says: {e.code} {e.error_message}"
        await processing_message.edit(error_message)
        return False

4 days ago

Update main.py
    except Exception as e:
4 days ago

Update main.py
        # Catch-all for any unexpected exceptions
        error_message = f"❌ Unexpected error while inviting assistant: {str(e)}"
4 days ago

Update main.py
        await processing_message.edit(error_message)
2 weeks ago

Create main.py
        return False
5 days ago

Update main.py

4 days ago

Update main.py

2 weeks ago

Create main.py
# Helper to convert ASCII letters to Unicode bold
def to_bold_unicode(text: str) -> str:
    bold_text = ""
    for char in text:
        if 'A' <= char <= 'Z':
            bold_text += chr(ord('𝗔') + (ord(char) - ord('A')))
        elif 'a' <= char <= 'z':
            bold_text += chr(ord('𝗮') + (ord(char) - ord('a')))
        else:
            bold_text += char
    return bold_text

@bot.on_message(filters.command("start"))
async def start_handler(_, message):
    user_id = message.from_user.id
    raw_name = message.from_user.first_name or ""
    styled_name = to_bold_unicode(raw_name)
    user_link = f"[{styled_name}](tg://user?id={user_id})"

    add_me_text = to_bold_unicode("Add Me")
    updates_text = to_bold_unicode("Updates")
    support_text = to_bold_unicode("Support")
    help_text = to_bold_unicode("Help")

    caption = (
        f"👋 нєу {user_link} 💠, 🥀\n\n"
2 weeks ago

Update main.py
        f">🎶 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 {BOT_NAME.upper()}! 🎵\n"
2 weeks ago

Create main.py
        ">🚀 𝗧𝗢𝗣-𝗡𝗢𝗧𝗖𝗛 24×7 𝗨𝗣𝗧𝗜𝗠𝗘 & 𝗦𝗨𝗣𝗣𝗢𝗥𝗧\n"
        ">🔊 𝗖𝗥𝗬𝗦𝗧𝗔𝗟-𝗖𝗟𝗘𝗔𝗥 𝗔𝗨𝗗𝗜𝗢\n"
        ">🎧 𝗦𝗨𝗣𝗣𝗢𝗥𝗧𝗘𝗗 𝗣𝗟𝗔𝗧𝗙𝗢𝗥𝗠𝗦: YouTube | Spotify | Resso | Apple Music | SoundCloud\n"
        ">✨ 𝗔𝗨𝗧𝗢-𝗦𝗨𝗚𝗚𝗘𝗦𝗧𝗜𝗢𝗡𝗦 when queue ends\n"
        ">🛠️ 𝗔𝗗𝗠𝗜𝗡 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦: Pause, Resume, Skip, Stop, Mute, Unmute, Tmute, Kick, Ban, Unban, Couple\n"
        ">❤️ 𝗖𝗢𝗨𝗣𝗟𝗘 𝗦𝗨𝗚𝗚𝗘𝗦𝗧𝗜𝗢𝗡 (pick random pair in group)\n"
        f"๏ ᴄʟɪᴄᴋ {help_text} ʙᴇʟᴏᴡ ғᴏʀ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ."
    )

    buttons = [
        [
2 weeks ago

Update main.py
            InlineKeyboardButton(f"➕ {add_me_text}", url=f"{BOT_LINK}?startgroup=true"),
2 weeks ago

Create main.py
            InlineKeyboardButton(f"📢 {updates_text}", url="https://t.me/vibeshiftbots")
        ],
        [
            InlineKeyboardButton(f"💬 {support_text}", url="https://t.me/Frozensupport1"),
            InlineKeyboardButton(f"❓ {help_text}", callback_data="show_help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_animation(
        animation="https://frozen-imageapi.lagendplayersyt.workers.dev/file/2e483e17-05cb-45e2-b166-1ea476ce9521.mp4",
        caption=caption,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
