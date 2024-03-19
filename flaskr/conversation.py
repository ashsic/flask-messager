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
    ).fetchall()
    messages = db.execute(
        'SELECT * FROM user_message'
    ).fetchall()
    return render_template('conversation/index.html', conversations=conversations, messages=messages)

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

            if len(usernames) == 1:
                db.execute(

                )

            # Group chats are always created (barring future limitations)
            if len(usernames) > 1:
                db.execute(
                    'INSERT INTO group_conversation (admin_id)'
                    ' VALUES (?)',
                    (g.user['id'],)
                )

                conv_id = db.execute(
                    'SELECT id FROM app_conversation ORDER BY id DESC LIMIT 1;'
                ).fetchone()[0]
                
                usernames.append(g.user['username'])
                for user in usernames:
                    user_id = db.execute(
                        'SELECT id FROM user WHERE username = ?',
                        (user,)
                    ).fetchone()[0]
                    db.execute(
                        'INSERT INTO user_conversation_membership'
                        ' VALUES (?, ?)',
                        (conv_id, user_id)   
                    )
                
                db.execute(
                    'INSERT INTO group_message (sender_id, conversation_id, body)'
                    ' VALUES (?, ?, ?)',
                    (g.user['id'], conv_id, body)
                )
            # else:
            #     # check for existing conversation between 2 users
            #     conv_id = db.execute(
            #         'SELECT id FROM app_conversation ac'
            #         ' INNER JOIN (SELECT * FROM user_conversation_membership WHERE )'
            #         ' WHERE is_group = FALSE'
            #     )
            
            # Happens if group chat, or no existing dm:
            # usernames.append(g.user['username'])
            # for user in usernames:
            #     user_id = db.execute(
            #         'SELECT id FROM user WHERE username = ?',
            #         (user)
            #     )
            #     db.execute(
            #         'INSERT INTO user_conversation_membership'
            #         ' VALUES (?, ?)',
            #         (conv_id, user_id)   
            #     )

            db.commit()
            return redirect(url_for('conversation.index'))

    return render_template('conversation/create.html')
