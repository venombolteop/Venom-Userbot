import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType

from ... import app, cdx, eor, vars
from ...modules.mongo.pmguard import *


@app.on_message(cdx(["pm", "pmpermit", "pmguard"]) & filters.me)
async def pm_on_off(client, message):
    if len(message.command) < 2:
        return await eor(message,
            "ʜᴇʏ, ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏ ?\n\nᴇxᴀᴍᴘʟᴇ: `.pm on` | `.pm off`")
    aux = await eor(message, "ᴘʀᴏᴄᴇssɪɴɢ ...")
    query = message.text.split(None, 1)[1].lower()
    if query == "on":
        set_permit = await set_pm_permit(True)
        if set_permit:
            return await aux.edit("ᴘᴍ ᴘᴇʀᴍɪᴛ ᴛᴜʀɴᴇᴅ ᴏɴ !")
        return await aux.edit("ᴘᴍ ᴘᴇʀᴍɪᴛ ᴀʟʀᴇᴀᴅʏ ᴏɴ !")
        
    elif query == "off":
        set_permit = await set_pm_permit(False)
        if set_permit:
            return await aux.edit("ᴘᴍ ᴘᴇʀᴍɪᴛ ᴛᴜʀɴᴇᴅ ᴏғғ !")
        return await aux.edit("ᴘᴍ ᴘᴇʀᴍɪᴛ ᴀʟʀᴇᴀᴅʏ ᴏғғ !")
        


@app.on_message(cdx(["a", "approve"]) & filters.private  & filters.me)
async def pm_approve(client, message):
    check = vars.OLD_MSG
    flood = vars.FLOODXD
    uid = message.chat.id
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            return await message.edit("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪs ᴛᴏ ʏᴏᴜʀsᴇʟғ.")
    permit = await add_approved_user(uid)
    if permit:
        if str(uid) in check and str(uid) in flood:
            try:
                await check[str(uid)].delete()
                flood[str(uid)] = 0
            except BaseException:
                pass
        await message.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴘᴘʀᴏᴠᴇᴅ.")
    else:
        await message.edit("ᴛʜɪs ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ.")
    await asyncio.sleep(2)
    return await message.delete()


@app.on_message(cdx(["da", "disapprove"]) & filters.private & filters.me)
async def pm_disapprove(client, message):
    uid = message.chat.id
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            return await message.edit("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪs ᴛᴏ ʏᴏᴜʀsᴇʟғ.")
    permit = await del_approved_user(uid)
    if permit:
        await message.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀᴘᴘʀᴏᴠᴇᴅ.")
    else:
        await message.edit("ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ !")
    await asyncio.sleep(2)
    return await message.delete()


@app.on_message(cdx(["block"]) & filters.me)
async def block_user_func(client, message):
    if message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
    elif message.chat.type != ChatType.PRIVATE:
        if not message.reply_to_message:
            return await message.edit("ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴍᴇssᴀɢᴇ.")
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            return await message.edit("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪs ᴛᴏ ʏᴏᴜʀsᴇʟғ.")
        user_id = replied_user.id
    await message.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ!!!")
    await client.block_user(user_id)


@app.on_message(cdx(["unblock"]) & filters.me)
async def unblock_user_func(client, message):
    if message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
    elif message.chat.type != ChatType.PRIVATE:
        if not message.reply_to_message:
            return await message.edit("  ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ ᴍᴇssᴀɢᴇ.")
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            return await message.edit("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜɪs ᴛᴏ ʏᴏᴜʀsᴇʟғ.")
        user_id = replied_user.id
    await client.unblock_user(user_id)
    await message.edit("ᴜɴʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ !")


__NAME__ = "Guard"
__MENU__ = f"""
**➻ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ sᴇᴄᴜʀɪᴛʏ sʏsᴛᴇᴍ
ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ғʀᴏᴍ ᴅᴍ sᴘᴀᴍs ✨.**

`.pmguard [`on`|off`] - ᴀᴄᴛɪᴠᴀᴛᴇ
ᴏʀ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇ ᴘᴍ ɢᴜᴀʀᴅ sᴇᴄᴜʀɪᴛʏ.

`.approve` - ᴀᴘᴘʀᴏᴠᴇ ᴀɴ ᴜsᴇʀ ғᴏʀ
ᴄʜᴀᴛ ᴡɪᴛʜɪɴ ᴅᴍ.

`.disapprove` - ᴛᴏ ᴅɪsᴀᴘᴘʀᴏᴠᴇ ᴀɴ
ᴜsᴇʀ (Remove From Allowed List).

`.block` - ʙʟᴏᴄᴋ ᴀɴ ᴜsᴇʀ ᴀɴᴅ ᴀᴅᴅ
ɪɴ ʏᴏᴜʀ ʙʟᴏᴄᴋʟɪsᴛ.

`.unblock` - ᴜɴʙʟᴏᴄᴋ ᴀɴ ᴜsᴇʀ ᴀɴᴅ
ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ʏᴏᴜʀ ʙʟᴏᴄᴋʟɪsᴛ.
"""

