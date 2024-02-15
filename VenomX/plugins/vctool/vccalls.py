from ... import *
from pyrogram import filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat


async def get_vc_call(client, message):
    chat_id = message.chat.id
    chat_peer = await client.resolve_peer(chat_id)
    if isinstance(chat_peer,
        (InputPeerChannel, InputPeerChat)
    ):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(
                    GetFullChannel(channel=chat_peer)
                )
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(
                    GetFullChat(chat_id=chat_peer.chat_id)
                )
            ).full_chat
            
        if full_chat is not None:
            return full_chat.call
            
    return False

@app.on_message(cdx(["svc", "startvc"]) & ~filters.private)
@sudo_users_only
async def create_video_chat(client, message):
    chat_id = message.chat.id
    try:
        aux = await eor(message, "**🔄 ᴘʀᴏᴄᴇssɪɴɢ ...**")
        vc_call = await get_vc_call(client, message)
        if vc_call:
            return await aux.edit("**➻ ᴠᴄ ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴇ❗**")
        peer = await client.resolve_peer(chat_id)
        await client.invoke(
            CreateGroupCall(
                peer=peer,
                random_id=client.rnd_id() // 9000000000,
            ),
        )
        await aux.edit("**➻ sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴀʀᴛᴇᴅ ᴠᴄ.**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        pass



@app.on_message(cdx(["dvc", "evc", "stopvc", "endvc"]) & ~filters.private)
@sudo_users_only
async def discard_video_chat(client, message):
    user_id = message.from_user.id
    try:
        aux = await eor(message, "**🔄 ᴘʀᴏᴄᴇssɪɴɢ ...**")
        vc_call = await get_vc_call(client, message)
        if not vc_call:
            return await aux.edit("**➻ ᴠᴄ ɴᴏᴛ sᴛᴀʀᴛᴇᴅ ʏᴇᴛ❗**")
        await client.invoke(
            DiscardGroupCall(call=vc_call)
        )
        return await aux.edit("**➻ sᴜᴄᴄᴇsғᴜʟʟʏ ᴇɴᴅᴇᴅ ᴠᴄ.**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        pass


@app.on_message(cdx(["rvc", "restartvc"]) & ~filters.private)
@sudo_users_only
async def discard_video_chat(client, message):
    chat_id = message.chat.id
    try:
        aux = await eor(message, "**🔄 ᴘʀᴏᴄᴇssɪɴɢ ...**")
        vc_call = await get_vc_call(client, message)
        if not vc_call:
            return await aux.edit("**➻ ᴠᴄ ɴᴏᴛ sᴛᴀʀᴛᴇᴅ ʏᴇᴛ❗**")
        peer = await client.resolve_peer(chat_id)
        await client.invoke(
            DiscardGroupCall(call=vc_call)
        )
        await aux.edit("**➻ sᴜᴄᴄᴇsғᴜʟʟʏ ᴇɴᴅᴇᴅ ᴠᴄ.**")
        await client.invoke(
            CreateGroupCall(
                peer=peer,
                random_id=client.rnd_id() // 9000000000,
            ),
        )
        return await aux.edit("**➻ sᴜᴄᴄᴇsғᴜʟʟʏ ʀᴇsᴛᴀʀᴛᴇᴅ ᴠᴄ.**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        pass




__NAME__ = "VC"
__MENU__ = """
**➻ sᴛᴀʀᴛ ᴏʀ ᴇɴᴅ ᴠᴄ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ
ᴏʀ ɢʀᴏᴜᴘ ʙʏ sɪᴍᴘʟᴇ ᴄᴏᴍᴍᴀɴᴅs.**

`.svc` - sᴛᴀʀᴛ ᴠᴄ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
`.dvc` - ᴇɴᴅ ᴠᴄ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
`.rvc` - ʀᴇsᴛᴀʀᴛ ᴠᴄ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ. 
"""
