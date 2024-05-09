from flask import Blueprint, render_template, request, redirect, session, abort
import sqlite3
import datetime

wiki = Blueprint('wiki', __name__, template_folder='templates')

wiki_categories = {'characters': "Персонажи", "weapons": "Оружие", "enemies": "Враги", "gameplay": "Геймплей"}


def databaserequest(req):
    con = sqlite3.connect("database.db", check_same_thread=False)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    result = cur.execute(req).fetchall()
    con.commit()
    con.close()
    return result


@wiki.route('/wiki')
def main_wiki():
    return render_template('wiki/wiki.html', session=session, title="База данных Ишимуры")


@wiki.route('/wiki/<category>')
def categories(category):
    wikis = databaserequest(f'''SELECT id, title, author, datetime FROM wiki WHERE category='{category}' ''')
    return render_template('wiki/wiki_categories.html', session=session,
                           title=f"{wiki_categories[category]} - База данных Ишимуры", wikis=wikis,
                           category=wiki_categories[category])


@wiki.route('/wiki/<int:id>')
def get_one_wiki(id):
    cur_wiki = databaserequest(f'''SELECT id, title, author, content FROM wiki WHERE id='{id}' ''')
    return render_template('wiki/wiki_page.html', session=session,
                           title=f"{cur_wiki[0]['title']} - База данных Ишимуры", wiki=cur_wiki)


@wiki.route('/wiki_add', methods=['GET', 'POST'])
def add_wiki():
    if request.method == 'POST':
        try:
            title, content, category = (request.form.get('title'),
                                        request.form.get('ckeditor'),
                                        request.form.get('category'))
            date_time = datetime.date.today()
            author = session['nickname']

            databaserequest(f'''INSERT INTO wiki(title, content, author, datetime, category) 
            VALUES('{title}', '{content}', '{author}', '{date_time}', '{category}')''')
            return redirect('/wiki')
        except KeyError:
            abort(413)
    return render_template('wiki/add.html', session=session, title="Добавление вики-страницы")


@wiki.route('/wiki_edit/<int:id>', methods=['GET', 'POST'])
def edit_wiki(id):
    cur_wiki = databaserequest(f'''SELECT title, author, content, category FROM wiki WHERE id='{id}' ''')
    if request.method == 'POST':
        try:
            title, content, category = (request.form.get('title'),
                                        request.form.get('ckeditor'),
                                        request.form.get('category'))
            date_time = datetime.date.today()
            author = session['nickname']

            databaserequest(f'''UPDATE wiki SET title='{title}', content='{content}', 
            datetime='{date_time}', author='{author}', category='{category}' WHERE id='{id}' ''')
            return redirect('/wiki')
        except KeyError:
            abort(413)
    return render_template('wiki/edit.html', session=session, title="Редактирование вики-страницы",
                           cur_wiki=cur_wiki, id=id)


@wiki.route('/wiki_delete/<int:id>', methods=['GET', 'POST'])
def delete_wiki(id):
    databaserequest(f'''DELETE from wiki WHERE id='{id}' ''')
    return redirect('/wiki')
