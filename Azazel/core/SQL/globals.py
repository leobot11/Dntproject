from . import BASE, SESSION
from sqlalchemy import Column, String, UnicodeText, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from pyrogram.filters import chat
from pyrogram import Client


class Globals(BASE):
    __tablename__ = "globals"
    user_id = Column(String(14), primary_key=True)
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, user_id, variable, value):
        self.user_id = str(user_id)
        self.variable = str(variable)
        self.value = value
        


Globals.__table__.create(checkfirst=True)


def addgvar(user_id, variable, value):
    query = SESSION.query(Globals).filter(Globals.user_id == str(user_id)).one_or_none()
    if query is not None:
        SESSION.delete(query)
    adder = Globals(user_id=str(user_id), variable=variable, value=value)
    SESSION.add(adder)
    SESSION.commit()



def delgvar(user_id, variable):
    rem = (
        SESSION.query(Globals)
        .filter(Globals.user_id == str(user_id))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def gvarstatus(user_id, variable):
    try:
        return SESSION.query(Globals).filter(Globals.user_id == str(user_id)).first()
    except BaseException:
        return None
    finally:
        SESSION.close()
        
"""
async def buat_log(bot, variable):
    user = await bot.get_me()
    user_id = user.id
    user_data = SESSION.query(Globals).filter(Globals.user_id == user_id, Globals.variable == str(variable)).first()
    botlog_chat_id = None

    if user_data:
        botlog_chat_id = int(user_data.value)

    if not user_data or not botlog_chat_id:
        group_name = 'Azazel Project Bot Log'
        group_description = 'Jangan Hapus Atau Keluar Dari Grup Ini\n\nCreated By @AzazelProjectBot.\nJika menemukan kendala atau ingin menanyakan sesuatu\nHubungi : @KynanSupport.'
        group = await bot.create_supergroup(group_name, group_description)
        botlog_chat_id = group.id
        text = 'Grup Log Berhasil Dibuat,\nKetik `id` untuk mendapatkan id log grup\nKemudian ketik `setlog` ID_GROUP\n\nContoh : setlog -100749492984'
        await bot.send_message(botlog_chat_id, text)

        if user_data:
            user_data.value = str(botlog_chat_id)
        else:
            user_data = Globals(user_id=user_id, variable=str(variable))
            SESSION.add(user_data)
        SESSION.commit()
    SESSION.close()

    return botlog_chat_id
   
    
async def get_botlog(user_id, variable):
    user_data = SESSION.query(Globals).filter(Globals.user_id == user_id, Globals.variable == str(variable)).first()
    botlog_chat_id = user_data.value if user_data else None
    SESSION.close()
    return int(botlog_chat_id) if botlog_chat_id else None


async def set_botlog(user_id, variable):
    botlog = SESSION.query(Globals).filter_by(Globals.user_id == user_id, Globals.variable == str(variable)).first()
    if botlog:
        botlog.value = str(botlog_chat_id)
    else:
        botlog = Globals(user_id=user_id, variable=str(variable))
        SESSION.add(botlog)
    SESSION.commit()
    SESSION.close()
"""