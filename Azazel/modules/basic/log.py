
import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from . import *
from Azazel.core.SQL import no_log_pms_sql
from Azazel.core.SQL.botlogsql import *
from Azazel.core.SQL.globals import *
from ubotlibs.ubot.utils.tools import get_arg



class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Client.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def monito_p_m_s(client, message):
    chat_id = message.chat.id
    user_id = client.me.id
    botlog_group_id = get_botlog(str(user_id))
    if not botlog_group_id:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    if not no_log_pms_sql.is_approved(message.chat.id) and message.chat.id != 777000:
        if LOG_CHATS_.RECENT_USER != message.chat.id:
            LOG_CHATS_.RECENT_USER = message.chat.id
            if LOG_CHATS_.NEWPM:
                await LOG_CHATS_.NEWPM.edit(
                    LOG_CHATS_.NEWPM.text.replace(
                        "**💌 PESAN BARU**",
                        f" • `{LOG_CHATS_.COUNT}` **Pesan**",
                    )
                )
                LOG_CHATS_.COUNT = 0
            LOG_CHATS_.NEWPM = await client.send_message(
                botlog_group_id,
                f"💌 <b><u>MENERUSKAN PESAN BARU</u></b>\n<b> • Dari :</b> {message.from_user.mention}\n<b> • User ID :</b> <code>{message.from_user.id}</code>",
                parse_mode=enums.ParseMode.HTML,
            )
        try:
            async for pmlog in client.search_messages(message.chat.id, limit=1):
                await pmlog.forward(botlog_group_id)
            LOG_CHATS_.COUNT += 1
        except BaseException:
            pass


@Client.on_message(filters.group & filters.mentioned & filters.incoming & ~filters.bot & ~filters.via_bot)
async def log_tagged_messages(client, message):
    chat_id = message.chat.id
    user_id = client.me.id
    botlog_group_id = get_botlog(str(user_id))
    if not botlog_group_id:
        return
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        return
    if (no_log_pms_sql.is_approved(message.chat.id)):
        return
    result = f"📨<b><u>ANDA TELAH DI TAG</u></b>\n<b> • Dari : </b>{message.from_user.mention}"
    result += f"\n<b> • Grup : </b>{message.chat.title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>Lihat Pesan</a>"
    result += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await client.send_message(
        botlog_group_id,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@Ubot(["pmlog"], "")
async def set_pmlog(client, message):
    cot = get_arg(message)
    if cot == "off":
        noob = False
    elif cot == "on":
        noob = True
    user_id = client.me.id
    if gvarstatus("PMLOG") and gvarstatus("PMLOG").value == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if noob:
            await message.edit("**PM Log Sudah Diaktifkan**")
        else:
            delgvar("PMLOG")
            await message.edit("**PM Log Berhasil Dimatikan**")
    elif noob:
        addgvar("PMLOG", noob)
        await message.edit("**PM Log Berhasil Diaktifkan**")
    else:
        await message.edit("**PM Log Sudah Dimatikan**")

@Ubot(["taglog"], "")
async def set_gruplog(client, message):
    cot = get_arg(message)
    if cot == "off":
        noob = False
    elif cot == "on":
        noob = True
    user_id = client.me.id
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG").value == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if noob:
            await message.edit("**Group Log Sudah Diaktifkan**")
        else:
            delgvar("GRUPLOG")
            await message.edit("**Group Log Berhasil Dimatikan**")
    elif noob:
        addgvar("GRUPLOG", noob)
        await message.edit("**Group Log Berhasil Diaktifkan**")
    else:
        await message.edit("**Group Log Sudah Dimatikan**")


@Ubot("setlog", "")
async def set_log(client, message):
    user_id = client.me.id
    chat_id = message.chat.id
    group_id = await client.get_chat(chat_id)
    chat = await client.get_chat(chat_id)
    if chat.type == "private":
        return await message.reply("Maaf, gunakan perintah ini di grup log anda.")
    set_botlog(str(user_id), group_id)
    await message.reply_text(f"ID Grup Log telah diatur ke {group_id} untuk grup ini.")


add_command_help(
    "Logger",
    [
        [
            "setlog",
            "Sebelum mengaktifkan fitur pmlog dan taglog anda harus mengatur setlog id_grup log anda terlebih dahulu.",
        ],
        [
            "taglog on or off",
            "Sebelum mengaktifkan fitur pmlog dan taglog anda harus mengatur setlog id_grup log anda terlebih dahulu.",
        ],
        [
            "pmlog on or off",
            "Sebelum mengaktifkan fitur pmlog dan taglog anda harus mengatur setlog id_grup log anda terlebih dahulu.",
        ],

    ],
)
