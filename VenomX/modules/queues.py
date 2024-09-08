queue = {}


async def add_to_queue(chat_id: int, **kwargs) -> int:
    queue_dict = queue.get(chat_id)
    if queue_dict:
        queue[chat_id].append({**kwargs})
    else:
        queue[chat_id] = []
        queue[chat_id].append({**kwargs})
    return len(queue[chat_id]) - 1


async def get_from_queue(chat_id: int) -> int:
    queue_dict = queue.get(chat_id)
    if queue_dict:
        try:
            return queue_dict[0]
        except:
            return 0
    return 0


async def is_queue_empty(chat_id: int) -> bool:
    queues = await get_from_queue(chat_id)
    if queues != 0:
        return False
    return True


async def task_done(chat_id: int) -> bool:
    empty_queue = await is_queue_empty(chat_id)
    if empty_queue:
        return False
    queue[chat_id].pop(0)
    return True


async def clear_queue(chat_id: int) -> bool:
    queue_dict = queue.get(chat_id)
    if not queue_dict:
        return False
    queue.pop(int(chat_id))
    return True
