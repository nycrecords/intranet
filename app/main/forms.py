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
    title = StringField('Title')
    meeting_type = SelectField("Meeting Type", choices=choices.MEETING_TYPES)
    Division = SelectField("Division", choices=choices.DIVISIONS)
    meeting_date = StringField('Meeting Date')
    meeting_location = StringField('Location')
    meeting_leader = StringField('Meeting Leader')
    meeting_note_taker = StringField('Meeting Notetaker')
    start_time = StringField('Start Time')
    end_time = StringField('End Time')
    attendees = StringField('Attendees')
    content = TextAreaField('Discussion')
    tags = StringField('Tags')
    next_meeting_date = StringField('Next Meeting Date')
    next_meeting_leader = StringField('Next Meeting Leader')
    next_meeting_note_taker = StringField('Next Meeting Notetaker')
    submit = SubmitField()

