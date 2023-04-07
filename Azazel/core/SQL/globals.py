"""
try:
    from . import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class Globals(BASE):
    __tablename__ = "globals"
    user_id = Column(String(14), primary_key=True)
    variable = Column(String, nullable=False)
    value = Column(UnicodeText, nullable=False)

    def __init__(self, user_id, variable, value):
        self.user_id = str(user_id)
        self.variable = variable
        self.value = value


Globals.__table__.create(checkfirst=True)


def gvarstatus(user_id, variable):
    try:
        return (
            SESSION.query(Globals)
            .filter(Globals.user_id == str(user_id))
            .filter(Globals.variable == variable)
            .first()
            .value
        )
    except BaseException:
        return None
    finally:
        SESSION.close()


def addgvar(user_id, variable, value):
    if SESSION.query(Globals).filter(Globals.user_id == str(user_id)).one_or_none():
        delgvar(user_id, variable)
    adder = Globals(str(user_id), variable, value)
    SESSION.add(adder)
    SESSION.commit()


def delgvar(user_id, variable):
    rem = (
        SESSION.query(Globals)
        .filter(Globals.user_id == str(user_id))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.commit()
"""

try:
    from . import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class Globals(BASE):
    __tablename__ = "globals"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)
    user_id = Column(String(14), primary_key=True)

    def __init__(self, variable, value, user_id):
        self.variable = str(variable)
        self.value = value
        self.variable = str(user_id)


Globals.__table__.create(checkfirst=True)


def gvarstatus(variable):
    try:
        return (
            SESSION.query(Globals)
            .filter(Globals.variable == str(variable), variable)
            .first()
            .value
        )
    except BaseException:
        return None
    finally:
        SESSION.close()


def addgvar(variable, value, user_id):
    if SESSION.query(Globals).filter(Globals.variable == str(variable)).one_or_none():
        delgvar(user_id, variable)
    adder = Globals(variable, value, user_id)
    SESSION.add(adder)
    SESSION.commit()


def delgvar(user_id, variable):
    rem = (
        SESSION.query(Globals)
        .filter(Globals.user_id == str(user_id))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.commit()
