

from sqlalchemy import Column, Numeric, String, UnicodeText, BigInteger

from . import BASE, SESSION


class Filters(BASE):
  
    __tablename__ = "filters"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(BigInteger, nullable=False)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, user_id, chat_id, keyword, reply, f_mesg_id):
        self.user_id = str(user_id)
        self.chat_id = int(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = int(f_mesg_id)

    def __eq__(self, other):
        return bool(
            isinstance(other, Filters)
            and self.user_id == other.user_id
            and self.chat_id == other.chat_id
            and self.keyword == other.keyword
        )


Filters.__table__.create(checkfirst=True)


def get_filter(user_id, chat_id, keyword):
    try:
        return SESSION.query(Filters).get((str(user_id), chat_id, keyword))
    except:
        return None
    finally:
        SESSION.close()


def get_filters(user_id):
    try:
        filters_list = SESSION.query(Filters).filter(Filters.user_id == str(user_id)).all()
        return filters_list if len(filters_list) > 0 else None
    except:
        return None
    finally:
        SESSION.close()



def add_filter(user_id, chat_id, keyword, reply, f_mesg_id):
    to_check = get_filter(user_id, chat_id, keyword)
    if not to_check:
        adder = Filters(str(user_id), chat_id, keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
    else:
        rem = SESSION.query(Filters).get(str(user_id), chat_id, keyword, reply, f_mesg_id)
        SESSION.delete(rem)
        SESSION.commit()
        adder = Filters(str(user_id), chat_id, keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()


def remove_filter(user_id, chat_id, keyword):
    cek = get_filter(user_id, chat_id, keyword)
    if not cek:
        return False
    else:
        SESSION.delete(cek)
        SESSION.commit()
        return True
