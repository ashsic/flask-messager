from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('conversation', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    conversations = db.execute(
        'SELECT * FROM direct_conversation'
    ).fetchall()
    messages = db.execute(
        'SELECT * FROM direct_message'
    ).fetchall()
    
    return render_template('conversation/index.html', conversations=conversations)

@bp.route('/chat/<id>')
@login_required
def chat(id):
    db = get_db()
    messages = db.execute(
        'SELECT * FROM direct_message'
        ' WHERE (conversation_id) = (?)',
        (id,)
    ).fetchall()
    
    return render_template('conversation/chat.html',  messages=messages)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        usernames = request.form['username'].split(" ")
        body = request.form['body']
        error = None

        if not usernames:
            error = 'username is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            # if direct message:
            if len(usernames) == 1:
                user_id = db.execute(
                    'SELECT id FROM user WHERE username = ?',
                    (usernames[0],)
                ).fetchone()[0]

                conv_id = db.execute(
                    'SELECT id FROM direct_conversation'
                    ' WHERE (member_1 = ? AND member_2 = ?) OR (member_1 = ? AND member_2 = ?)',
                    (g.user['id'], user_id, user_id, g.user['id'])
                ).fetchone()

                # If no existing dm, create one
                if not conv_id:
                    db.execute(
                        'INSERT INTO direct_conversation (member_1, member_2)'
                        ' VALUES (?, ?)',
                        (g.user['id'], user_id)
                    )

                    conv_id = db.execute(
                        'SELECT id FROM direct_conversation'
                        ' WHERE (member_1 = ? AND member_2 = ?)',
                        (g.user['id'], user_id)
                    ).fetchone()
                
                db.execute(
                    'INSERT INTO direct_message (sender_id, conversation_id, body)'
                    ' VALUES (?, ?, ?)',
                    (g.user['id'], conv_id[0], body)
                )

            # Group chats are always created (barring future limitations)
            elif len(usernames) > 1:
                db.execute(
                    'INSERT INTO group_conversation (admin_id)'
                    ' VALUES (?)',
                    (g.user['id'],)
                )

                conv_id = db.execute(
                    'SELECT id FROM group_conversation ORDER BY id DESC LIMIT 1;'
                ).fetchone()[0]

                usernames.append(g.user['username'])
                for user in usernames:
                    user_id = db.execute(
                        'SELECT id FROM user WHERE username = ?',
                        (user,)
                    ).fetchone()[0]
                    db.execute(
                        'INSERT INTO group_conversation_membership'
                        ' VALUES (?, ?)',
                        (conv_id, user_id)   
                    )
                
                db.execute(
                    'INSERT INTO group_message (sender_id, conversation_id, body)'
                    ' VALUES (?, ?, ?)',
                    (g.user['id'], conv_id, body)
                )

            db.commit()
            return redirect(url_for('conversation.index'))

    return render_template('conversation/create.html')
