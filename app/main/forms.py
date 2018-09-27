from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField,
    SelectMultipleField
)
from wtforms import widgets

from wtforms.validators import DataRequired, Optional, Email
from app.constants import choices


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


class EnfgForm(FlaskForm):
    """
    Form for the Easy Not Found Generator page

    type: Select dropdown with choices for different certificate types
    name: String for the name on the certificate you are looking for
    bride_name: String for the bride name on the certificate you are looking for
    year: String for the year on the certificate you are looking for
    borough: String for the boroughs on the certificate you are looking for
    signature: Boolean to determine if a signature should appear on the letter when printing
    submit: submit button for the form
    """
    type = SelectField('Type *', choices=choices.CERT_TYPE, validators=[DataRequired()])
    name = StringField('Name *', validators=[DataRequired()])
    bride_name = StringField('Bride\'s Name:')
    year = StringField('Year *', validators=[DataRequired()])
    borough = SelectMultipleField('Borough', choices=choices.BOROUGHS)
    signature = BooleanField('Print without signature')
    submit = SubmitField('Print')
