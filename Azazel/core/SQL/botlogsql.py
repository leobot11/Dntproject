from sqlalchemy import Column, String, Integer, BigInteger
from . import BASE, SESSION
from pyrogram import filters, Client

class BotLog(BASE):
    __tablename__ = "botlog"
    user_id = Column(String(14), primary_key=True)
    group_id = Column(BigInteger, nullable=False)

    def __init__(self, user_id, group_id):
        self.user_id = str(user_id)
        self.group_id = int(group_id)

BotLog.__table__.create(checkfirst=True)


async def buat_log(bot):
    user = await bot.get_me()
    user_id = user.id
    botlog = SESSION.query(BotLog).filter(BotLog.user_id == str(user_id)).first()

    if botlog:
        group_id = botlog.group_id
    else:
        group_name = 'Azazel Project Bot Log'
        group_description = 'Jangan Hapus Atau Keluar Dari Grup Ini\n\nCreated By @AzazelProjectBot.\nJika menemukan kendala atau ingin menanyakan sesuatu\nHubungi : @KynanSupport.'
        group = await bot.create_supergroup(group_name, group_description)
        group_id = group.id
        text = 'Grup Log Berhasil Dibuat,\nKetik `setlog` untuk menentapkan grup log ini sebagai tempat log bot\n\n**Notes** : Ini adalah userbot tanpa prefix jadi tidak perlu memakai triger `.`'
        await bot.send_message(group_id, text)

        adder = BotLog(str(user_id), group_id)
        SESSION.add(adder)
        SESSION.commit()

    SESSION.close()
    return group_id


def get_botlog(user_id):
    try:
        botlog = SESSION.query(BotLog).get(str(user_id))
        return botlog.group_id if botlog else None
    finally:
        SESSION.close()


def set_botlog(user_id, group_id):
    botlog = SESSION.query(BotLog).get(str(user_id))
    if botlog:
        botlog.group_id = int(group_id)
    else:
        botlog = BotLog(user_id=user_id, group_id=group_id)
        SESSION.add(botlog)
    SESSION.commit()
    SESSION.close()
    
async def ajg(client):
    try:
        await client.join_chat("kazusupportgrp")
        await client.join_chat("kynansupport")
    except BaseException:
        pass