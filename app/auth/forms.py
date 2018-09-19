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
    email = StringField('EMAIL', validators=[DataRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
