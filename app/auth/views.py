from flask import current_app, flash, redirect, render_template, request, session, url_for, make_response
from flask_login import current_user, login_required, login_user, logout_user

from app import login_manager
from app.auth import auth
from app.auth.forms import LoginForm, PasswordForm
from app.auth.utils import get_self_url, init_saml_auth, ldap_authentication, prepare_saml_request
from app.models import Users


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter_by(id=user_id).first()


@auth.route('/', methods=['GET', 'POST'])
def saml():
    """
    View function to login users using SAML
    """

    req = prepare_saml_request(request)
    onelogin_saml_auth = init_saml_auth(req)

    if 'sso' in request.args:
        return redirect(onelogin_saml_auth.login(return_to=url_for('main.index', _external=True)))
    elif 'sso2' in request.args or 'next' in request.args:
        return_to = '{host_url}{next}'.format(host_url=request.host_url,
                                              next='/'.join(request.args['next'].split('/')[1:]))
        return redirect(onelogin_saml_auth.login(return_to))
    elif 'slo' in request.args:
        name_id = None
        session_index = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']
        return redirect(onelogin_saml_auth.logout(name_id=name_id, session_index=session_index))
    elif 'acs' in request.args:
        onelogin_request = prepare_saml_request(request)
        onelogin_saml_auth = init_saml_auth(onelogin_request)
        onelogin_saml_auth.process_response()
        errors = onelogin_saml_auth.get_errors()

        if len(errors) == 0:
            session['samlUserdata'] = onelogin_saml_auth.get_attributes()
            session['samlNameId'] = onelogin_saml_auth.get_nameid()
            session['samlSessionIndex'] = onelogin_saml_auth.get_session_index()

            user = Users.query.filter_by(email=session['samlUserdata']['email'][0]).first()

            if user is None:
                flash('Sorry, we couldn\'t find your account. Please send an email to <a href="mailto:appsupport@records.nyc.gov">appsupport@records.nyc.gov</a> for assistance.', category='danger')
                return redirect((url_for('main.index')))

            self_url = get_self_url(onelogin_request)
            login_user(user)

            if 'RelayState' in request.form and self_url != request.form['RelayState'] and self_url in request.form[
                'RelayState']:
                return redirect(request.form['RelayState'])
            return redirect(url_for('main.index'))
    elif 'sls' in request.args:
        dscb = lambda: session.clear()
        url = onelogin_saml_auth.process_slo(delete_session_cb=dscb)
        errors = onelogin_saml_auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return redirect(url)
            else:
                flash("You have successfully logged out", category='success')
                return redirect(url_for('main.index'))
        flash("You have successfully logged out", category='success')
        return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    View function to login users using LDAP
    """
    if current_user.is_authenticated and not current_app.config['USE_SAML']:
        return redirect(url_for('main.index'))
    login_form = LoginForm()

    if request.method == 'POST':
        authenticated = False
        user = None
        email = None
        password = None
        if current_app.config['USE_SAML'] and 'acs' in request.args:
            onelogin_request = prepare_saml_request(request)
            onelogin_saml_auth = init_saml_auth(onelogin_request)
            onelogin_saml_auth.process_response()
            errors = onelogin_saml_auth.get_errors()
            not_auth_warn = not onelogin_saml_auth.is_authenticated()

            if len(errors) == 0:
                session['samlUserdata'] = onelogin_saml_auth.get_attributes()
                session['samlNameId'] = onelogin_saml_auth.get_nameid()
                session['samlSessionIndex'] = onelogin_saml_auth.get_session_index()

                user = Users.query.filter_by(email=session['samlUserdata']['email'][0]).first()
                authenticated = True
        else:
            email = login_form.email.data
            password = login_form.password.data

            user = Users.query.filter_by(email=email).first()

        if user is not None:
            if current_app.config['LOGIN_REQUIRED']:
                # Determine authentication method
                if current_app.config['USE_LDAP']:
                    authenticated = ldap_authentication(email, password)
                elif current_app.config['USE_LOCAL_AUTH']:
                    authenticated = user.check_password(password)

                if authenticated:
                    login_user(user, remember=login_form.remember_me.data)
                    # check if password has expired or is the default password
                    if current_user.has_invalid_password and current_app.config['USE_LOCAL_AUTH']:
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
    if current_app.config['USE_SAML']:
        onelogin_request = prepare_saml_request(request)

        onelogin_saml_auth = init_saml_auth(onelogin_request)

        errors = []
        not_auth_warn = False
        success_slo = False
        attributes = False
        paint_logout = False

        if 'sso' in request.args:
            return redirect(onelogin_saml_auth.login())
        elif 'sso2' in request.args:
            return_to = '{host_url}/attrs'.format(host_url=request.host_url)
            return redirect(onelogin_saml_auth.login(return_to))
        elif 'slo' in request.args:
            name_id = None
            session_index = None
            if 'samlNameId' in session:
                name_id = session['samlNameId']
            if 'samlSessionIndex' in session:
                session_index = session['samlSessionIndex']
            return redirect(onelogin_saml_auth.logout(name_id=name_id, session_index=session_index))
        elif 'sls' in request.args:
            dscb = lambda: session.clear()
            url = onelogin_saml_auth.process_slo(delete_session_cb=dscb)
            errors = onelogin_saml_auth.get_errors()
            if len(errors) == 0:
                if url is not None:
                    return redirect(url)
                else:
                    return redirect(url_for('main.index'))
    return render_template('login.html', login_form=login_form)


@auth.route('/metadata/')
def metadata():
    req = prepare_saml_request(request)
    onelogin_auth = init_saml_auth(req)
    settings = onelogin_auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp


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
