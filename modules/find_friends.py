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
        forms_db = databaserequest('SELECT * FROM `find_friends`')

        today = date.today()
        for form in forms_db:
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
                               session=session, forms=forms)


@find_friends.route('/find_friends_actions', methods=["GET", "POST"])
def edit_find_friends():
    if not isloggin():
        session['redirect'] = url_for(
            "find_friends.edit_find_friends") + f"?id={request.args.get('id')}&delete={request.args.get('delete')}"
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
                            "games=?, games_exp=? WHERE id=?",
                            params=[request.form.get("text"), request.form.get("time_zone"),
                                    request.form.get("birthday"), ' '.join(games), request.form.get("games_exp"),
                                    request.form.get("id")],
                            commit=True)
        else:
            databaserequest("INSERT INTO `find_friends`(`user_id`, `text`, `time_zone`, `birthday`, `games`, "
                            "`games_exp`) VALUES (?, ?, ?, ?, ?, ?)",
                            params=[session['id'], request.form.get("text"), request.form.get("time_zone"),
                                    request.form.get("birthday"), ' '.join(games), request.form.get("games_exp")],
                            commit=True)
    else:
        if request.args.get("id") and request.args.get("id") != "None":
            edit = databaserequest('SELECT * FROM `find_friends` WHERE `id`=?', params=[request.args.get("id")],
                                   fetchone=True)
            if edit['user_id'] != session['id']:
                return redirect(url_for('find_friends.main_find_friends'))
            return render_template('find_friends/edit.html', title="Управление заявкой", session=session,
                                   edit=edit, time_zones=pytz.all_timezones)
        elif request.args.get("delete") and request.args.get("delete") != "None":
            databaserequest("DELETE from find_friends WHERE id=?", params=[request.args.get("delete")], commit=True)
        else:
            return render_template('find_friends/edit.html', title="Добавление заявки",
                                   session=session, time_zones=pytz.all_timezones)
    return redirect(url_for('find_friends.main_find_friends'))
