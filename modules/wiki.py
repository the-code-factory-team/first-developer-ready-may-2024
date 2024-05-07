from flask import Blueprint, render_template, request, redirect, session, abort
import sqlite3
import datetime

wiki = Blueprint('wiki', __name__, template_folder='templates')


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
    wikis = databaserequest(f'''SELECT id, title, author, datetime FROM wiki''')
    return render_template('wiki/wiki.html', wikis=wikis)


@wiki.route('/wiki/<int:id>')
def get_one_wiki(id):
    cur_wiki = databaserequest(f'''SELECT id, title, author, content FROM wiki WHERE id='{id}' ''')
    return render_template('wiki/cur_wiki.html', wiki=cur_wiki)


@wiki.route('/wiki_add', methods=['GET', 'POST'])
def add_wiki():
    if request.method == 'POST':
        try:
            title, content = request.form.get('title'), request.form.get('ckeditor')
            date_time = datetime.date.today()
            author = session['nickname']

            databaserequest(f'''INSERT INTO wiki(title, content, author, datetime) 
            VALUES('{title}', '{content}', '{author}', '{date_time}')''')
            return redirect('/wiki')
        except KeyError:
            abort(413)
    return render_template('wiki/add.html')


@wiki.route('/wiki_redact/<int:id>', methods=['GET', 'POST'])
def redact_wiki(id):
    cur_wiki = databaserequest(f'''SELECT title, author, content FROM wiki WHERE id='{id}' ''')
    if request.method == 'POST':
        try:
            title, content = request.form.get('title'), request.form.get('ckeditor')
            date_time = datetime.date.today()
            author = session['nickname']

            databaserequest(f'''UPDATE wiki SET title='{title}', content='{content}', 
            datetime='{date_time}', author='{author}' WHERE id='{id}' ''')
            return redirect('/wiki')
        except KeyError:
            abort(413)
    return render_template('wiki/redact.html', cur_wiki=cur_wiki, id=id)


@wiki.route('/wiki_delete/<int:id>', methods=['GET', 'POST'])
def delete_wiki(id):
    databaserequest(f'''DELETE from wiki WHERE id='{id}' ''')
    return redirect('/wiki')