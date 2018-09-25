from flask_wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    Email,
    DataRequired
)


class LoginForm(Form):
    """
    Login form for users

    email: a string for a user's @records.nyc.gov email
    password: a user's network password which will be authenticated using LDAP
    remember_me: a boolean to give users the option to stay logged in after they leave the site
    submit: submit button for login
    """
    email = StringField('EMAIL', validators=[DataRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
