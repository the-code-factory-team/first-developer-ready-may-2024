from datetime import date, datetime
from pprint import pprint

import pytz
from flask import Blueprint, render_template, request, redirect, session, url_for
from modules.functions import isloggin, databaserequest, cur, get_datetime_now

find_friends = Blueprint('find_friends', __name__, template_folder='templates')


@find_friends.route('/find_friends', methods=["GET", "POST"])
def main_find_friends():
    if request.method == 'POST':
        pass
    else:
        game_types = ['Dead Space 1', 'Dead Space 2', 'Dead Space 3', "Dead Space Remake"]
        forms = list()
        user_block_form = None
        already_create = False
        forms_db = databaserequest('SELECT * FROM `find_friends`')

        user_id = None
        if 'id' in session:
            user_id = session['id']

        today = date.today()
        for form in forms_db:
            if form['user_id'] == user_id:
                already_create = True

            if form['hide']:
                if form['user_id'] == user_id:
                    user_block_form = form['id']
                continue

            games = []

            born = datetime.strptime(form['birthday'], "%Y-%m-%d")
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            tzdt = datetime.now(pytz.timezone(form['time_zone'])).strftime("%d.%m.%Y %H:%I")

            for game in form['games'].split(' '):
                games.append(game_types[int(game) - 1])

            forms.append({
                'id': form['id'],
                'user_id': form['user_id'],
                'text': form['text'],
                'desc': 'Играет в ' + ', '.join(games) + f' уже {form["games_exp"]} лет/год(-а)',
                'info': f'{age} лет, сейчас {tzdt}'
            })
        return render_template('find_friends/find_friends.html', title="Поиск команды",
                               session=session, forms=forms, already_create=already_create,
                               user_block_form=user_block_form)


@find_friends.route('/find_friends_actions', methods=["GET", "POST"])
def find_friends_actions():
    if not isloggin():
        session['redirect'] = url_for(
            "find_friends.find_friends_actions") + (f"?id={request.args.get('id')}&delete={request.args.get('delete')}"
                                                    f"&block={request.args.get('block')}")
        return redirect(url_for('account_login'))

    if request.method == 'POST':
        games = ""
        if request.form.get('dead_space_1'):
            games += "1"
        if request.form.get('dead_space_2'):
            games += "2"
        if request.form.get('dead_space_3'):
            games += "3"
        if request.form.get('dead_space_4'):
            games += "4"

        if request.form.get("id"):
            databaserequest("UPDATE find_friends SET text=?, time_zone=?, birthday=?, "
                            "games=?, games_exp=?, hide=0 WHERE id=?",
                            params=[request.form.get("text"), request.form.get("time_zone"),
                                    request.form.get("birthday"), ' '.join(games), request.form.get("games_exp"),
                                    request.form.get("id")],
                            commit=True)
            return redirect(url_for('find_friends.main_find_friends') + f"#{request.form.get('id')}")
        else:
            databaserequest("INSERT INTO `find_friends`(`user_id`, `text`, `time_zone`, `birthday`, `games`, "
                            "`games_exp`) VALUES (?, ?, ?, ?, ?, ?)",
                            params=[session['id'], request.form.get("text"), request.form.get("time_zone"),
                                    request.form.get("birthday"), ' '.join(games), request.form.get("games_exp")],
                            commit=True)
            return redirect(url_for('find_friends.main_find_friends') + f"#{cur.lastrowid}")
    else:
        id = None
        if request.args.get("id") and request.args.get("id") != 'None':
            id = int(request.args.get("id"))
        elif request.args.get("delete") and request.args.get("delete") != 'None':
            id = int(request.args.get("delete"))
        elif request.args.get("block") and request.args.get("block") != 'None':
            id = int(request.args.get("block"))

        edit = databaserequest('SELECT * FROM `find_friends` WHERE `id`=?', params=[id],
                               fetchone=True)
        if edit is None:
            return render_template('find_friends/edit.html', title="Добавление заявки",
                                   session=session, time_zones=pytz.all_timezones)

        if request.args.get("id") and request.args.get("id") != "None":
            if edit['user_id'] != session['id']:
                return redirect(url_for('find_friends.main_find_friends'))

            return render_template('find_friends/edit.html', title="Управление заявкой", session=session,
                                   edit=edit, time_zones=pytz.all_timezones)
        elif request.args.get("delete") and request.args.get("delete") != "None":
            if edit['user_id'] != session['id'] and int(session['acctype']) < 2:
                return redirect(url_for('find_friends.main_find_friends'))

            databaserequest("DELETE from find_friends WHERE id=?", params=[request.args.get("delete")], commit=True)
        elif request.args.get("block") and request.args.get("block") != "None" and int(session['acctype']) >= 2:
            databaserequest("UPDATE find_friends SET hide=1 WHERE id=?",
                            params=[request.args.get("block")], commit=True)
    return redirect(url_for('find_friends.main_find_friends'))
