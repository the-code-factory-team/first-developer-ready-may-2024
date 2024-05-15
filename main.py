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
import traceback

from flask import render_template, redirect, session, url_for, request, jsonify, Flask
from flask_ckeditor import CKEditor

from modules import wiki, news, find_friends, gallery
from modules.functions import cur, con, acctypes, isloggin, databaserequest, get_datetime_now

app = Flask(__name__)
app.secret_key = os.urandom(24)
ckeditor = CKEditor(app)


@app.route('/')
def index():
    return render_template('main.html', title="Добро пожаловать!")


@app.route('/register', methods=['GET', 'POST'])
def account_register():
    if isloggin():
        return redirect(url_for('account_view'))

    if request.method == 'POST':
        error = "Данный адрес электронной почты уже зарегистрирован!"
        if not databaserequest("SELECT * FROM accounts WHERE `email`=?", params=[request.form.get('email')]):
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

        return render_template('account/register.html', title="Регистрация", session=session, error=error + " 😔")
    else:
        return render_template('account/register.html', title="Регистрация", session=session)


@app.route('/auth', methods=['GET', 'POST'])
def account_login():
    if isloggin():
        return redirect(url_for('account_view'))

    if request.method == 'POST':
        testaccount = databaserequest("SELECT * FROM accounts WHERE `nickname`=? OR `email`=?",
                                      params=[request.form.get('login'), request.form.get('login')], fetchone=True)
        if testaccount:
            md5password = str(hashlib.md5(request.form.get("password").encode(encoding='UTF-8',
                                                                              errors='strict')).hexdigest())
            if testaccount['password'] == md5password:
                session['id'] = testaccount['id']
                session['nickname'] = testaccount['nickname']
                session['first_name'] = testaccount['first_name']
                session['last_name'] = testaccount['last_name']
                session['acctype'] = testaccount['acctype']

                if 'redirect' in session:
                    redirecturl = session['redirect']
                    session.pop('redirect', None)
                    return redirect(redirecturl)

                return redirect(url_for('account_view'))

        return render_template('account/login.html', title="Авторизация", session=session,
                               error="Неверный логин или пароль! 😔")
    else:
        if request.args.get("redirect"):
            session['redirect'] = request.args.get("redirect")
        return render_template('account/login.html', title="Авторизация", session=session)


@app.route('/account', methods=['GET', 'POST'])
def account_view():
    if not isloggin():
        session['redirect'] = url_for("account_view")
        return redirect(url_for('account_login'))

    if request.method == 'POST':
        databaserequest("UPDATE accounts SET about = ?, website = ?, vk = ?, tg = ?, discord = ? WHERE id = ?",
                        params=[request.form.get('about'), request.form.get('website'), request.form.get('vk'),
                                request.form.get('tg'), request.form.get('discord'), session['id']],
                        commit=True)

    account = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[session['id']],
                              fetchone=True)
    return render_template('account/settings.html', title="Настройки аккаунта", session=session, acctypes=acctypes,
                           account=account)


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
    if not nickname:
        if not isloggin():
            session['redirect'] = url_for("profile")
            return redirect(url_for('account_login'))
        account = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[int(session['id'])],
                                  fetchone=True)
    elif 'id' in nickname:
        account = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[int(nickname[2:])],
                                  fetchone=True)
    else:
        account = databaserequest("SELECT * FROM `accounts` WHERE `nickname`=?", params=[nickname], fetchone=True)

    return render_template('account/profile.html', title=f"Профиль {account['nickname']}", session=session,
                           profile=account)


@app.route('/chat', methods=['GET', 'POST'])
def chat_page():
    if not isloggin():
        session['redirect'] = url_for("chat_page")
        return redirect(url_for('account_login'))

    if request.method == 'POST':
        if request.form.get('message'):
            moscow_time = get_datetime_now()

            databaserequest('INSERT INTO `chat`(`user_id`, `message`, `datetime`) VALUES (?, ?, ?)',
                            params=[int(session['id']), request.form.get("message"),
                                    moscow_time],
                            commit=True)
            if cur.lastrowid != 0:
                return jsonify(ok=True, id=cur.lastrowid, datetime=moscow_time)
            return jsonify(ok=False, error="Произошла ошибка при отправке сообщения! 😱")
        else:
            authors = {}
            new_messages = databaserequest('SELECT * FROM `chat` WHERE `id` > ?',
                                           params=[int(request.form.get("last_message_id"))], aslist=True)
            for msg in new_messages:
                author = databaserequest("SELECT * FROM `accounts` WHERE `id`=?", params=[int(msg[1])],
                                         fetchone=True, aslist=True)
                authors[msg[0]] = {'first_name': author[4], 'last_name': author[5],
                                   'nickname': author[2]}
            return jsonify(ok=True, new_messages=new_messages, authors=authors)

    return render_template('chat.html', title="Чат", session=session)


@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    return render_template('error.html', title="Страница не найдена", session=session,
                           error='Извините, мы не можем найти данную страницу!'), 404


@app.errorhandler(500)
def on_error(e):
    print("ОШИБКА:\n")
    print(traceback.format_exc())
    return render_template('error.html', title="Произошла ошибка", session=session,
                           error=f'Извините, произошла ошибка при выполнении запроса!'), 500


@app.errorhandler(413)
def unauthorized(e):
    return redirect(url_for('account_login'))


def create_app():
    global app
    app.register_blueprint(wiki.wiki)
    app.register_blueprint(news.news)
    app.register_blueprint(find_friends.find_friends)
    app.register_blueprint(gallery.gallery)
    return app


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 80)), debug=True)  # DEBUG
    con.close()
