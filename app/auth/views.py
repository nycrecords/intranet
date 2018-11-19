from flask import (
    request,
    redirect,
    render_template,
    url_for,
    flash,
    current_app
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)
from app.auth import auth
from app.auth.forms import LoginForm, PasswordForm
from app.auth.utils import ldap_authentication
from app.models import Users
from app import login_manager


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter_by(id=user_id).first()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    View function to login users using LDAP
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if request.method == 'POST':
        email = login_form.email.data
        password = login_form.password.data

        user = Users.query.filter_by(email=email).first()

        if user is not None:
            if current_app.config['LOGIN_REQUIRED']:
                if current_app.config['USE_LDAP']:
                    authenticated = ldap_authentication(email, password)
                if current_app.config['USE_LOCAL_AUTH']:
                    authenticated = user.check_password(password)
                if authenticated:
                    login_user(user, remember=login_form.remember_me.data)
                    # check if password has expired or is the default password
                    if current_user.has_invalid_password:
                        return redirect(url_for('auth.password'))
                    return redirect(url_for('main.index'))
            else:
                login_user(user, remember=login_form.remember_me.data)
                return redirect(url_for('main.index'))
            flash("Invalid username/password combination.", category="danger")
            return render_template('login.html', login_form=login_form)
        else:
            flash("User not found. Please contact IT to gain access to the system.", category="warning")
            return render_template('login.html', login_form=login_form)
    return render_template('login.html', login_form=login_form)


@auth.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """
    Return the change password page and redirect to the home page
    if password change is successful.
    """
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        current_user.update_password(password_form.current_password.data,
                                     password_form.new_password.data)
        return redirect('/')
    return render_template('change_password.html', password_form=password_form)


@auth.route('/logout', methods=['GET'])
def logout():
    """
    View function to logout users
    """
    logout_user()
    return redirect(url_for('main.index'))
