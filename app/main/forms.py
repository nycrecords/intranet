from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    BooleanField,
    SelectMultipleField
)
from flask_wtf.file import FileField
from wtforms.fields.html5 import DateField, EmailField, TelField
from wtforms.validators import DataRequired, Optional

from app.constants import choices
from app.constants.intake import (
    PROJECT_TYPE,
    ENHANCEMENT,
    PRIORITY,
    PROJECT_ACCESS,
    YES_NO
)


class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.

    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://gist.github.com/devxoul/7638142#file-wtf_required_if-py
    """

    field_flags = ("requiredif",)

    def __init__(self, message=None, *args, **kwargs):
        super(RequiredIf).__init__()
        DataRequired.__init__(self)
        self.message = message
        self.conditions = kwargs

    # field is requiring that name field in the form is data value in the form
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)


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
    meeting_type = SelectField('MEETING TYPE', choices=choices.MEETING_TYPES)
    division = SelectField('DIVISION', choices=choices.DIVISIONS)
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
    title = StringField('TITLE')
    sponsor = StringField('SPONSOR')
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


class AppDevIntakeForm(FlaskForm):
    # Submission Information
    submitter_name = StringField("Submitter Name:", validators=[DataRequired()])
    submitter_email = EmailField("Submitter Email:", validators=[DataRequired()])
    submitter_phone = TelField("Submitter Phone:", validators=[DataRequired()])
    submitter_title = StringField("Submitter Title", validators=[DataRequired()])
    submitter_division = StringField(
        "Submitter Division:", validators=[DataRequired()]
    )

    # Project Information
    project_name = StringField("Name:", validators=[DataRequired()])
    enhancement_or_new_project = SelectField(
        "Is this a new project or an enhancement to an existing project?",
        choices=PROJECT_TYPE,
        validators=[DataRequired()],
    )
    current_project_name = StringField(
        "If this is an enhancement, please provide the name of the current project:",
        validators=[
            RequiredIf(
                enhancement_or_new_project=ENHANCEMENT,
                message="You must provide the current project name if this is an enhancement",
            )
        ],
    )
    project_background = TextAreaField("Background:", validators=[DataRequired()])
    rationale = TextAreaField("Rationale:", validators=[DataRequired()])
    project_goals = TextAreaField("Goals:", validators=[DataRequired()])
    priority = SelectField("Priority:", choices=PRIORITY, validators=[DataRequired()])
    completion_date = DateField(
        "When do you want this project to be delivered?", validators=[DataRequired()]
    )
    supplemental_materials_one = FileField("Supplemental Materials:")
    supplemental_materials_one_desc = StringField(
        "Supplemental Materials Description: ",
        validators=[RequiredIf(supplemental_materials_one != "None")],
    )
    supplemental_materials_two = FileField("Supplemental Materials")
    supplemental_materials_two_desc = StringField(
        "Supplemental Materials Description: ",
        validators=[RequiredIf(supplemental_materials_two != "None")],
    )
    supplemental_materials_three = FileField("Supplemental Materials:")
    supplemental_materials_three_desc = StringField(
        "Supplemental Materials Description: ",
        validators=[RequiredIf(supplemental_materials_three != "None")],
    )
    designated_business_owner_name = StringField(
        "Designated Business Owner Name:", validators=[DataRequired()]
    )
    designated_business_owner_email = EmailField(
        "Designated Business Owner Email:", validators=[DataRequired()]
    )
    designated_business_owner_phone = TelField(
        "Designated Business Owner Phone:", validators=[DataRequired()]
    )
    designated_business_owner_title = StringField(
        "Designated Business Owner Title", validators=[DataRequired()]
    )
    designated_business_owner_division = SelectField(
        "Designated Business Owner Division:",
        choices=choices.DIVISIONS,
        validators=[DataRequired()],
    )

    # Technical Information
    project_access = SelectField(
        "Who needs access to the final application?",
        choices=PROJECT_ACCESS,
        validators=[DataRequired()],
    )
    login_required = SelectField(
        "Is login and account management functionality required?",
        choices=YES_NO,
        validators=[DataRequired()],
    )
    ui_ux_needed = SelectField(
        "Is UI / UX design needed?", choices=YES_NO, validators=[DataRequired()]
    )

    # Submit
    submit = SubmitField("Submit Intake Request")


class UploadForm(FlaskForm):
    """
    """
    file_title = StringField('Title')
    document_type = SelectField('Type', choices=choices.DOCUMENT_TYPES)
    division = SelectField('Division', choices=choices.DIVISIONS)
    file_object = FileField('File')
    submit = SubmitField('Upload')