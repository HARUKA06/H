# queue.py
queue = {}

def add_to_queue(chat_id, title, file):
    if chat_id not in queue:
        queue[chat_id] = []
    queue[chat_id].append({"title": title, "file": file})

def get_queue(chat_id):
    return queue.get(chat_id, [])

def pop_next(chat_id):
    if chat_id in queue and queue[chat_id]:
        return queue[chat_id].pop(0)
    return None

def clear_queue(chat_id):
    queue[chat_id] = []
