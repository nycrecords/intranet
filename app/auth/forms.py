from flask_wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    Email,
    DataRequired,
    Length
)
from flask_login import current_user
import string


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


class PasswordForm(Form):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[Length(min=8, max=32)])

    def validate(self):
        base_validation = super().validate()
        is_valid_current_password = current_user.check_password(self.current_password.data)
        is_valid_new_password = current_user.is_new_password(self.new_password.data)
        specials = set(string.punctuation)
        has_num = any(c.isdigit() for c in self.new_password.data)
        has_upper = any(c.isupper() for c in self.new_password.data)
        has_lower = any(c.islower() for c in self.new_password.data)
        has_special = any(c in specials for c in self.new_password.data)

        if not has_num:
            self.new_password.errors.append("Your new password must contain at least 1 number.")
        if not has_upper:
            self.new_password.errors.append("Your new password must contain at least 1 capital letter.")
        if not has_lower:
            self.new_password.errors.append("Your new password must contain at least 1 lower case letter.")
        if not has_special:
            self.new_password.errors.append("Your new password must contain at least 1 special character.")

        if not is_valid_new_password:
            self.new_password.errors.append(
                "Your new password cannot be the same as your current password or your last 3 passwords.")
        if not is_valid_current_password:
            self.current_password.errors.append("Incorrect password.")

        return (
            base_validation and
            is_valid_current_password and
            is_valid_new_password and
            has_num and
            has_upper and
            has_lower and
            has_special
        )