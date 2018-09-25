from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField,
    PasswordField
)
from wtforms.validators import DataRequired, Optional, Email
from app.constants import choices


class MeetingNotesForm(FlaskForm):
    """
    Form for posting meeting notes
    """
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


class StaffDirectorySearchForm(FlaskForm):
    """
    Form for searching the staff directory
    """
    search = StringField('Search')
    filters = SelectField("Filters", choices=choices.STAFF_DIRECTORY_FILTERS)
    submit = SubmitField('Search')