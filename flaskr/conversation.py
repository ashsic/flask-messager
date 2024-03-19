from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('conversation', __name__)

@bp.route('/')
def index():
    db = get_db()
    conversations = db.execute(
        'SELECT * FROM user'

        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' ORDER BY created DESC'
    ).fetchall()
    return render_template('conversation/index.html', conversations=conversations)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        username = request.form['username'].split(" ")
        body = request.form['body']
        error = None

        if not username:
            error = 'username is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO app_conversation (is_group)'
                ' VALUES (?)'
                'INSERT INTO user_conversation_membership'
                ' VALUES (?, ?)'
                'INSERT INTO user_message'

                ,
                (len(username) > 1, g.user['id'], username)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
