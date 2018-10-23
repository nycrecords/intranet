from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField,
    SelectMultipleField
)
from wtforms.validators import DataRequired
from app.constants import choices


class MeetingNotesForm(FlaskForm):
    """
    Form for posting meeting notes

    title: Input field for the title of the post
    meeting_type: Dropdown containing the possible types of meetings
    division: Dropdown containing choices for division
    meeting_date: The date that the meeting occurred
    meeting_location: The location of the meeting
    meeting_leader: The leader of the meeting
    meeting_note_taker: The note taker of the meeting
    start_time: The time that the meeting started
    end_time: The time that the meeting ended
    attendees: List of Users that attended the meeting
    content: HTML formatted string that contains the discussion of the meeting
    tags: List of tags that best describe the post
    next_meeting_date: The date of the next meeting
    next_meeting_leader: The leader of the next meeting
    next_meeting_note_taker: The note taker of the next meeting
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


class NewsForm(FlaskForm):
    """
    Form for posting news announcements

    title: Input field for the title of the post
    content: HTML formatted string that contains the news announcement
    tags: List of tags that best describe the post
    """
    title = StringField('TITLE')
    content = TextAreaField('ANNOUNCEMENT')
    tags = StringField('TAGS')
    submit = SubmitField()


class EventForm(FlaskForm):
    """
    Form for posting events

    event_date: The date of the event
    event_location: The location of the event
    event_leader: The leader of the event
    start_time: The start time of the event
    end_time: The end time of the event
    title: Input field for the title of the post
    sponsor: The sponsor of the event (Optional)
    content: HTML formatted string that contains the event description
    tags: List of tags that best describe the post
    """
    event_date = StringField('EVENT DATE')
    event_location = StringField('EVENT LOCATION')
    event_leader = StringField('EVENT LEADER')
    start_time = StringField('START TIME')
    end_time = StringField('END TIME')
    title = StringField ('TITLE')
    sponsor = StringField ('SPONSOR')
    content = TextAreaField('DESCRIPTION')
    tags = StringField('TAGS')
    submit = SubmitField()


class StaffDirectorySearchForm(FlaskForm):
    """
    Form for searching the staff directory

    search: Input field with the search term being entered
    filters: Dropdown containing the different filters you can search on (first name, last name, division, title)
    submit: Submit button for search form
    """
    search = StringField('Search')
    filters = SelectField("Filters", choices=choices.STAFF_DIRECTORY_FILTERS)
    submit = SubmitField('Search')


class EnfgForm(FlaskForm):
    """
    Form for the Easy Not Found Generator page

    type: Select dropdown with choices for different certificate types
    name: String for the name on the certificate you are looking for
    bride_name: String for the bride name on the certificate you are looking for
    year: String for the year on the certificate you are looking for
    borough: String for the boroughs on the certificate you are looking for
    signature: Boolean to determine if a signature should appear on the letter when printing
    submit: Submit button for the form
    """
    type = SelectField('Type *', choices=choices.CERT_TYPE, validators=[DataRequired()])
    name = StringField('Name *', validators=[DataRequired()])
    bride_name = StringField('Bride\'s Name:')
    year = StringField('Year *', validators=[DataRequired()])
    borough = SelectMultipleField('Borough', choices=choices.BOROUGHS)
    signature = BooleanField('Print without signature')
    submit = SubmitField('Print')
