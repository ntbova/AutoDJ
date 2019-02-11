import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = 'error'
        user = None

        # todo: login with spotify api

        if error is None:
            # user's id is stored in a new session
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        # error is shown to the user if authentication fails
        flash(error)

    # login page is shown when the user initially navigates to auth/login or there was authentication error
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, store user on g.user;
    If there is no user id, or if the id doesn't exist, g.user will be None
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        pass  # todo: get user from spotify


@bp.route('/logout')
def logout():
    # remove the user id from the session
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    This decorator returns a new view function that wraps the original view it's applied to.
    The new function checks if a user is loaded and redirects to the login page otherwise.
    If a user is loaded, the original view is called and continues normally.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
