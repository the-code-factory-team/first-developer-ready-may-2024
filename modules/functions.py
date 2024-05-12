import sqlite3
from datetime import datetime

import pytz
from flask import session, redirect, url_for, render_template

acctypes = ["Игрок", "Редактор", "Модератор", "Администратор"]

con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, nickname TEXT, 
    acctype INTEGER DEFAULT (0), first_name TEXT, last_name TEXT, password TEXT, about TEXT DEFAULT(''), 
    website TEXT DEFAULT(''), vk TEXT DEFAULT(''), tg TEXT DEFAULT(''), discord TEXT DEFAULT(''));""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author 
    INTEGER, datetime TEXT, author_update INTEGER DEFAULT (0), datetime_update TEXT DEFAULT (''), 
    likes INTEGER DEFAULT(0));""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS wiki (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author 
    TEXT, datetime TEXT, likes INTEGER DEFAULT(0), category INTEGER, author_update TEXT DEFAULT (''), 
    datetime_update TEXT DEFAULT (''));""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, message TEXT, 
    datetime TEXT);""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS find_friends (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, text TEXT, 
    time_zone TEXT, can_play_per_day TEXT, games TEXT, games_exp INTEGER, birthday TEXT, hide INTEGER DEFAULT(0));""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS gallery (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, 
    author INTEGER, datetime TEXT, likes INTEGER DEFAULT(0), author_update TEXT DEFAULT (''), 
    datetime_update TEXT DEFAULT (''), photo_url TEXT, hide INTEGER DEFAULT(0));""")


def databaserequest(text, params=[], commit=False, fetchone=False, aslist=False):
    cur.row_factory = sqlite3.Row
    if aslist:
        cur.row_factory = None
    dbrequest = cur.execute(f"""{text}""", params)
    if not commit:
        if fetchone:
            return dbrequest.fetchone()
        return dbrequest.fetchall()
    else:
        con.commit()
    return True


def isloggin():
    if "id" in session:
        testaccount = databaserequest("SELECT * FROM accounts WHERE id = ?",
                                      params=[session['id']], fetchone=True)
        if testaccount:
            session['acctype'] = testaccount['acctype']
            session['first_name'] = testaccount['first_name']
            session['last_name'] = testaccount['last_name']
            session['nickname'] = testaccount['nickname']
            return True
        else:
            return redirect(url_for('account_quit'))
    return False


def get_datetime_now(format="%d.%m.%Y %H:%I:%S"):
    return datetime.now(pytz.timezone('Europe/Moscow')).strftime(format)
