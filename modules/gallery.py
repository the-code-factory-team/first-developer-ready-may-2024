import os.path
from os import path, getcwd

from flask import Blueprint, render_template, request, redirect, session, url_for
from modules.functions import isloggin, databaserequest, cur, get_datetime_now
from werkzeug.utils import secure_filename

gallery = Blueprint('gallery', __name__, template_folder='templates')
extensions = ['png', 'jpg', 'jpeg']


@gallery.route('/gallery')
def main_gallery():
    photos = databaserequest("SELECT * FROM gallery")
    user_block_photos = list()
    block_photos = list()
    for photo in photos:
        if photo['hide']:
            block_photos.append(photo['id'])
            if 'id' in session:
                if photo['author'] == session['id']:
                    user_block_photos.append([photo['id'], photo['title']])
    return render_template('gallery/gallery.html', session=session, title="Галерея Ишимуры",
                           photos=photos, user_block_photos=user_block_photos, block_photos=block_photos)


@gallery.route('/gallery_actions', methods=['GET', 'POST'])
def gallery_actions():
    if not isloggin():
        session['redirect'] = url_for(
            "gallery.gallery_actions") + f"?id={request.args.get('id')}&delete={request.args.get('delete')}"
        return redirect(url_for('account_login'))

    if request.method == 'POST':
        if request.form.get('id'):
            databaserequest("UPDATE gallery SET title=?, description=?, author_update=?, "
                            "datetime_update=?, hide=0 WHERE id=?",
                            params=[request.form.get("title"), request.form.get("description"),
                                    session['id'], get_datetime_now("%d.%m.%Y в %H:%I"), request.form.get("id")],
                            commit=True)
            return redirect(url_for('gallery.main_gallery') + f'#{request.form.get("id")}')
        else:
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            photo.save(path.join(getcwd(), "static/img/gallery", filename))

            databaserequest("INSERT INTO gallery(`title`, `description`, `author`, `datetime`, `photo_url`) "
                            "VALUES (?, ?, ?, ?, ?)",
                            params=[request.form.get("title"), request.form.get("description"),
                                    session['id'], get_datetime_now("%d.%m.%Y в %H:%I"),
                                    'static/img/gallery/' + filename],
                            commit=True)
            return redirect(url_for('gallery.main_gallery') + f'#{cur.lastrowid}')
    else:
        id = None
        if request.args.get("id") and request.args.get("id") != 'None':
            id = int(request.args.get("id"))
        elif request.args.get("delete") and request.args.get("delete") != 'None':
            id = int(request.args.get("delete"))
        elif request.args.get("block") and request.args.get("block") != 'None':
            id = int(request.args.get("block"))

        edit = databaserequest("SELECT * FROM gallery WHERE id=?", params=[id], fetchone=True)
        if edit is None:
            return render_template("gallery/edit.html", title="Добавление фото", session=session)

        if request.args.get("id") and request.args.get("id") != "None":
            if edit['author'] != session['id']:
                return redirect(url_for('gallery.main_gallery'))
            return render_template("gallery/edit.html", title="Редактирование фото",
                                   session=session, edit=edit)
        elif request.args.get("delete") and request.args.get("delete") != "None":
            databaserequest("DELETE from gallery WHERE id=?", params=[request.args.get("delete")], commit=True)
        elif request.args.get("block") and request.args.get("block") != "None" and int(session['acctype']) >= 2:
            databaserequest("UPDATE gallery SET hide=1 WHERE id=?",
                            params=[request.args.get("block")], commit=True)
    return redirect(url_for('gallery.main_gallery'))
