from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SelectField,
    SubmitField,
    BooleanField
)
from wtforms.validators import DataRequired, Optional
from app.constants import choices


class Sign_In_Form(FlaskForm):
    """
    Library Archive sign in form
    """
    first_name = StringField('First Name *', validators=[DataRequired()])
    last_name = StringField("Last Name *", validators=[DataRequired()])
    affiliation = StringField("Affiliation", validators=[Optional()])
    email = StringField("Email", validators=[Optional()])
    phone = StringField("Phone", validators=[Optional()])
    address = StringField("Address", validators=[Optional()])
    city = StringField("City", validators=[Optional()])
    state = SelectField("State", choices=choices.STATES, validators=[Optional()])
    zipcode = StringField("Zipcode", validators=[Optional()])
    country = SelectField("Country", choices=choices.COUNTRIES, validators=[Optional()])
    library = BooleanField("Library")
    archives = BooleanField("Archives")
    genealogy = BooleanField("Genealogy")
    submit = SubmitField()


