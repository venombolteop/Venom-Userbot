from ... import app, cdx, eor, super_user_only
from ...console import SUDOERS
from ...modules.mongo.sudoers import add_sudo, del_sudo


@app.on_message(cdx(["addsudo", "as"]))
@super_user_only
async def add_sudo_user(client, message):
    try:
        aux = await eor(message, "**🔄 ᴘʀᴏᴄᴇssɪɴɢ ...**")
        if not message.reply_to_message:
            if len(message.command) != 2:
                return await aux.edit(
                    "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ username/user_id."
                )
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            user = await app.get_users(user)
            if user.id in SUDOERS:
                return await aux.edit(
                "{0} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.".format(user.mention)
            )
            added = await add_sudo(user.id)
            if added:
                SUDOERS.append(user.id)
                await aux.edit("ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs.".format(user.mention))
            else:
                await aux.edit("ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ɪɴ sᴜᴅᴏ ᴜsᴇʀs")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id in SUDOERS:
            return await aux.edit(
                "{0} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.".format(
                    message.reply_to_message.from_user.mention
                )
            )
        added = await add_sudo(user_id)
        if added:
            SUDOERS.append(user_id)
            await aux.edit(
                "ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs.".format(
                    message.reply_to_message.from_user.mention
                )
            )
        else:
            await aux.edit("sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")
        return
    except Exception as e:
        print("ᴇʀʀᴏʀ: `{e}`")
        return


@app.on_message(cdx(["delsudo", "ds"]))
@super_user_only
async def del_sudo_user(client, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ username/user_id.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in SUDOERS:
            return await message.edit("ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏғ ʙᴏᴛ's sᴜᴅᴏ.")
        removed = await del_sudo(user.id)
        if removed:
            SUDOERS.remove(user.id)
            await message.edit("ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ʙᴏᴛ's sᴜᴅᴏ ᴜsᴇʀ")
            return
        else:
            await message.edit(f"sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")
            return
    user_id = message.reply_to_message.from_user.id
    if user_id not in SUDOERS:
        return await message.edit("ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏғ ʙᴏᴛ's sᴜᴅᴏ.")
    removed = await del_sudo(user_id)
    if removed:
        SUDOERS.remove(user_id)
        await message.edit("ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ʙᴏᴛ's sᴜᴅᴏ ᴜsᴇʀ")
        return
    else:
        await message.edit(f"sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")
        return


@app.on_message(cdx(["sudousers", "sudolist", "sl"]))
@super_user_only
async def sudo_users_list(client, message):
    text = "➻<u> **sᴜᴘᴇʀ ᴜsᴇʀ:**</u>\n"
    count = 0
    try:
        user = (
            app.me.name if not app.me.mention else app.me.mention
        )
    except Exception:
        pass
    text += f"➻ {user}\n"
    users = 0
    for user_id in SUDOERS:
        if user_id != app.me.id:
            try:
                user = await app.get_users(user_id)
                user = (
                    user.first_name
                    if not user.mention
                    else user.mention
                )
                if users == 0:
                    users += 1
                    text += "\n➻<u> **sᴜᴅᴏ ᴜsᴇʀs:**</u>\n"
                count += 1
                text += f"{count}➻ {user}\n"
            except Exception:
                continue
    if not text:
        await message.edit("ɴᴏ sᴜᴅᴏ ᴜsᴇʀs ғᴏᴜɴᴅ!")
    else:
        await message.edit(text)


__NAME__ = "Sudo"
__MENU__ = f"""
**➻ ᴀᴅᴅ ᴏʀ ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ ᴜsᴇʀs
ғʀᴏᴍ ʏᴏᴜʀ ᴜsᴇʀʙᴏᴛ ✨...**

`.addsudo` - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ
ᴛᴏ ᴀᴅᴅ ᴀɴ ᴜsᴇʀ ɪɴ sᴜᴅᴏ ʟɪsᴛ.

`.delsudo` - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ
ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀɴ ᴜsᴇʀ ғʀᴏᴍ sᴜᴅᴏ.

`.sudolist` - ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴜᴅᴏ
ᴜsᴇʀs ʙʏ ɢᴇᴛᴛɪɴɢ ᴀ ʟɪsᴛ.

**➻ sᴏᴍᴇ sʜᴏʀᴛᴄᴜᴛ ᴄᴏᴍᴍᴀɴᴅs:**
=> [`.as`, `.ds`, `.sl`]
"""
