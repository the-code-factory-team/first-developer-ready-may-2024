from flask import Blueprint, render_template, request, redirect, session, url_for
from modules.functions import isloggin, databaserequest, cur, get_datetime_now

news = Blueprint('news', __name__, template_folder='templates')


@news.route('/news')
def main_news():
    news = databaserequest("SELECT * FROM news")
    return render_template('news/news.html', session=session, title="Новости", news=news)


@news.route('/news/<int:id>')
def news_page(id):
    cur_news = databaserequest("SELECT * FROM news WHERE id=?", params=[id], fetchone=True)
    if cur_news is None:
        return redirect(url_for('news.main_news'))
    author = databaserequest("SELECT * FROM accounts WHERE id=?", params=[cur_news['author']], fetchone=True)
    author_update = None
    if cur_news['author_update']:
        author_update = databaserequest("SELECT * FROM accounts WHERE id=?", params=[cur_news['author_update']],
                                        fetchone=True)
        author_update = f'{author_update["first_name"]} {author_update["last_name"]} ({author_update["nickname"]})'
    return render_template('news/news_page.html', session=session,
                           title=f"{cur_news['title']} - Новости", cur_news=cur_news,
                           author=f'{author["first_name"]} {author["last_name"]} ({author["nickname"]})',
                           author_update=author_update)


@news.route('/news_actions', methods=['GET', 'POST'])
def news_actions():
    if not isloggin():
        session['redirect'] = url_for("news.news_actions") + f"?id={request.args.get('id')}&delete={request.args.get('delete')}"
        return redirect(url_for('account_login'))

    if session['acctype'] < 1:
        return redirect(url_for('news.main_news'))

    if request.method == 'POST':
        if request.form.get('id'):
            databaserequest("UPDATE news SET title=?, content=?, author_update=?, "
                            "datetime_update=? WHERE id=?",
                            params=[request.form.get("title"), request.form.get("ckeditor"),
                                    session['id'], get_datetime_now("%d.%m.%Y в %H:%I"), request.form.get("id")],
                            commit=True)
            return redirect(f'/news/{request.form.get("id")}')
        else:
            databaserequest("INSERT INTO news(`title`, `content`, `author`, `datetime`) VALUES (?, ?, ?, ?)",
                            params=[request.form.get("title"), request.form.get("ckeditor"),
                                    session['id'], get_datetime_now("%d.%m.%Y в %H:%I")], commit=True)
            return redirect(f'/news/{cur.lastrowid}')
    else:
        if request.args.get("id") and request.args.get("id") != "None":
            edit = databaserequest("SELECT * FROM news WHERE id=?", params=[request.args.get("id")], fetchone=True)
            if edit is None:
                return redirect(url_for('news.news_actions') + "?action=add")
            return render_template("news/edit.html", title="Редактирование новости",
                                   session=session, edit=edit)
        elif request.args.get("delete") and request.args.get("delete") != "None":
            databaserequest("DELETE from news WHERE id=?", params=[request.args.get("delete")], commit=True)
        else:
            return render_template("news/edit.html", title="Добавление новости", session=session)
    return redirect(url_for('news.main_news'))
