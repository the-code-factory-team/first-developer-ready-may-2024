"""

Данный супер код придумала и написала команда кодеров из Липецка

░▀█▀░█▄█▒██▀░░░▄▀▀░▄▀▄░█▀▄▒██▀░░▒█▀▒▄▀▄░▄▀▀░▀█▀░▄▀▄▒█▀▄░▀▄▀
░▒█▒▒█▒█░█▄▄▒░░▀▄▄░▀▄▀▒█▄▀░█▄▄▒░░█▀░█▀█░▀▄▄░▒█▒░▀▄▀░█▀▄░▒█▒

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠋⣰⣦⡄⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠿⠿⠿⠿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠭⠅⠩⠭⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠒⠒⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠩⠠⣤⢈⡓⠚⡋⣠⡄⠍⢙⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣶⣤⣍⡓⠞⣋⣤⣶⠬⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⣘⡉⠃⠿⢿⠉⣈⣧⢸⣿⣿⣿⠀⠭⢙⣠⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⣿⣿⡇⠂⠠⠈⠙⠻⠘⠋⣉⣠⣴⣾⣿⣿⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⣿⣿⣇⣙⠲⠆⢸⣷⢰⣿⣿⣿⠉⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣇⠻⠻⠿⣿⣿⣶⣾⣿⢸⣿⣿⠿⠀⣻⠘⠟⣸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⡆⢇⠈⠛⠻⠟⠸⠿⠳⠂⢨⡄⢸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣿⣶⣤⣤⣶⣿⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿

"""

import hashlib
import os
import sqlite3
import traceback

from flask import Flask, render_template, redirect, session, url_for, request
from flask_ckeditor import CKEditor
from modules import wiki

app = Flask(__name__)
app.secret_key = os.urandom(24)
ckeditor = CKEditor(app)

acctypes = ["Игрок", "Редактор", "Модератор", "Администратор"]

con = sqlite3.connect("database.db", check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, nickname TEXT, acctype INTEGER DEFAULT (0), first_name TEXT, last_name TEXT, password TEXT, about TEXT DEFAULT(''), website TEXT DEFAULT(''), vk TEXT DEFAULT(''), tg TEXT DEFAULT(''), discord TEXT DEFAULT(''), game_exp INTEGER DEFAULT(0), game_part INTEGER DEFAULT(0));""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author TEXT, datetime TEXT, likes INTEGER DEFAULT(0));""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS wiki (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author TEXT, datetime TEXT, likes INTEGER DEFAULT(0), category INTEGER);""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS wiki_categories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT);""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS gallery (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, author TEXT, datetime TEXT, likes INTEGER DEFAULT(0));""")


def databaserequest(text, params=None, commit=False, fetchone=False):
    if params is None:
        params = []
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
                                      params=[session['id']])
        if len(testaccount) != 0:
            return True
        else:
            return redirect(url_for('account_quit'))
    return False


def render_page(template, title="", typeneed=[0], **kwargs):
    if typeneed[0] != 0 and int(session['acctype']) not in typeneed:
        return render_template('error.html', title="Ошибка", session=session,
                               error='У вас нет доступа для просмотра данной страницы!')

    return render_template(template, title=title, session=session, **kwargs)


@app.route('/')
def index():
    return render_page('main.html', title="Добро пожаловать!")


@app.route('/register', methods=['GET', 'POST'])
def account_register():
    if isloggin():
        return redirect(url_for('account_view'))

    if request.method == 'POST':
        error = "Данный адрес электронной почты уже зарегистрирован!"
        if len(databaserequest("SELECT * FROM accounts WHERE `email`=?", params=[request.form.get('email')])) == 0:
            error = "Данный никнейм уже использован!"
            if len(databaserequest("SELECT * FROM accounts WHERE `nickname`=?",
                                   params=[request.form.get('nickname')])) == 0:
                error = "Пароли не совпадают!"

                if request.form.get("password") == request.form.get("password2"):
                    md5password = str(hashlib.md5(request.form.get("password").encode(encoding='UTF-8',
                                                                                      errors='strict')).hexdigest())
                    databaserequest("INSERT INTO accounts (`email`, `nickname`, `first_name`, "
                                    "`last_name`, `password`) VALUES (?, ?, ?, ?, ?)",
                                    params=[request.form.get('email'), request.form.get('nickname'),
                                            request.form.get('first_name'), request.form.get('last_name'),
                                            md5password], commit=True)
                    session['id'] = cur.lastrowid
                    session['nickname'] = request.form.get('nickname')
                    session['first_name'] = request.form.get('first_name')
                    session['last_name'] = request.form.get('last_name')
                    session['acctype'] = 0
                    return redirect(url_for('account_view'))

        return render_page('account/register.html', title="Регистрация", error=error + " 😔")
    else:
        return render_page('account/register.html', title="Регистрация")


@app.route('/auth', methods=['GET', 'POST'])
def account_login():
    if isloggin():
        return redirect(url_for('account_view'))

    if request.method == 'POST':
        testaccount = databaserequest("SELECT * FROM accounts WHERE `nickname`=? OR `email`=?",
                                      params=[request.form.get('login'), request.form.get('login')], fetchone=True)
        if len(testaccount) != 0:
            md5password = str(hashlib.md5(request.form.get("password").encode(encoding='UTF-8',
                                                                              errors='strict')).hexdigest())
            if testaccount['password'] == md5password:
                session['id'] = testaccount['id']
                session['nickname'] = testaccount['nickname']
                session['first_name'] = testaccount['first_name']
                session['last_name'] = testaccount['last_name']
                session['acctype'] = testaccount['acctype']
                return redirect(url_for('account_view'))

        return render_page('account/login.html', title="Авторизация", error="Неверный логин или пароль! 😔")
    else:
        return render_page('account/login.html', title="Авторизация")


@app.route('/account', methods=['GET', 'POST'])
def account_view():
    if not isloggin():
        return redirect(url_for('account_login'))

    if request.method == 'POST':
        databaserequest("UPDATE accounts SET about = ?, website = ?, vk = ?, tg = ?, discord = ?, "
                        "game_exp = ?, game_part = ? WHERE id = ?",
                        params=[request.form.get('about'), request.form.get('website'), request.form.get('vk'),
                                request.form.get('tg'), request.form.get('discord'), request.form.get('game_exp'),
                                request.form.get('game_part'), session['id']],
                        commit=True)

    account = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[session['id']],
                              fetchone=True)
    return render_page('account/settings.html', title="Настройки аккаунта", acctypes=acctypes, account=account)


@app.route('/logout')
def account_quit():
    session.pop('id', None)
    session.pop('nickname', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('acctype', None)
    return redirect(url_for('index'))


@app.route('/profile', defaults={'nickname': None})
@app.route('/profile/<nickname>')
def profile(nickname=None):
    if not isloggin():
        return redirect(url_for('account_login'))

    if not nickname:
        account = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[int(session['id'])],
                                   fetchone=True)
    elif 'id' in nickname:
        account = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[int(nickname[1:])],
                                  fetchone=True)
    else:
        account = databaserequest("SELECT * FROM `accounts` WHERE `nickname`=?", params=[nickname], fetchone=True)

    return render_page('account/profile.html', title=f"Профиль {account['nickname']}",
                       profile=account)


@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_page('error.html', title="Страница не найдена",
                       error='Извините, мы не можем найти данную страницу!'), 404


@app.errorhandler(500)
def on_error(e):
    print("ОШИБКА:\n")
    print(traceback.format_exc())
    return render_page('error.html', title="Произошла ошибка",
                       error=f'Извините, произошла ошибка при выполнении запроса!'), 500


@app.errorhandler(413)
def unauthorized(e):
    return redirect(url_for('account_login'))


if __name__ == '__main__':
    app.register_blueprint(wiki.wiki)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 80)), debug=True)  # DEBUG
    con.close()
