from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField
)
from wtforms.validators import DataRequired, Optional
from app.constants import choices


# class Sign_In_Form(FlaskForm):
#     """
#     Library Archive sign in form
#     """
#     first_name = StringField('First Name *', validators=[DataRequired()])
#     last_name = StringField("Last Name *", validators=[DataRequired()])
#     affiliation = StringField("Affiliation", validators=[Optional()])
#     email = StringField("Email", validators=[Optional()])
#     phone = StringField("Phone", validators=[Optional()])
#     address = StringField("Address", validators=[Optional()])
#     city = StringField("City", validators=[Optional()])
#     state = SelectField("State", choices=choices.STATES, validators=[Optional()])
#     zipcode = StringField("Zipcode", validators=[Optional()])
#     country = SelectField("Country", choices=choices.COUNTRIES, validators=[Optional()])
#     library = BooleanField("Library")
#     archives = BooleanField("Archives")
#     genealogy = BooleanField("Genealogy")
#     submit = SubmitField()


class Meeting_Notes_Form(FlaskForm):
    title = StringField('TITLE')
    meeting_type = SelectField("MEETING TYPE", choices=choices.MEETING_TYPES)
    division = SelectField("DIVISION", choices=choices.DIVISIONS)
    meeting_date = StringField('MEETING DATE')
    meeting_location = StringField('LOCATION')
    meeting_leader = StringField('MEETING LEADER')
    meeting_note_taker = StringField('MEETING NOTETAKER')
    start_time = StringField('START TIME')
    end_time = StringField('END TIME')
    attendees = StringField('ATTENDEES')
    content = TextAreaField('DISCUSSION')
    tags = StringField('TAGS')
    next_meeting_date = StringField('NEXT MEETING DATE')
    next_meeting_leader = StringField('NEXT MEETING LEADER')
    next_meeting_note_taker = StringField('NEXT MEETING NOTETAKER')
    submit = SubmitField()

