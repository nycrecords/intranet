from flask import render_template, redirect, url_for, session, request as flask_request, jsonify, current_app, flash, send_file, send_from_directory
from flask_login import login_required, current_user
from app.models import Users, Posts, EventPosts, Documents, Monitor
from . import main
from app.main.forms import MeetingNotesForm, NewsForm, EventForm, StaffDirectorySearchForm, EnfgForm, UploadForm, AppDevIntakeForm
from app.main.utils import (create_meeting_notes,
                            create_news,
                            create_event_post,
                            get_users_by_division,
                            get_rooms_by_division,
                            create_document,
                            allowed_file,
                            VirusDetectedException,
                            scan_file,
                            process_documents_search,
                            process_posts_search,
                            render_email,
                            ping_website)
from datetime import datetime, timezone
from io import BytesIO
import pytz
from flask_mail import Message
from app.constants import choices
from sqlalchemy import extract, or_
from werkzeug.utils import secure_filename
import os
import json
from app import mail


@main.route('/', methods=['GET'])
def index():
    """
    View function to handle the home page
    Queries for the 20 most recent posts to display in the What's New section
    Queries for the next 4 events from today forward to display in the Calendar section
    :return: HTML template for home page
    """
    posts = Posts.query.filter_by(deleted=False).order_by(Posts.date_created.desc()).limit(20).all()
    events = EventPosts.query.filter(Posts.deleted == False, EventPosts.event_date >= datetime.utcnow()).order_by(
        EventPosts.event_date.asc()).limit(4).all()

    return render_template('index.html', posts=posts, events=events)


# Start view functions for posting
# TODO: Make a Post blueprint

@main.route('/news-and-updates', methods=['GET'])
def news_and_updates():
    """
    View function to handle the news and updates landing page
    Renders the page as empty then uses ajax to fill in the post rows
    :return: HTML template for news and updates landing page
    """
    posts_counter = {
        'event_posts': 0,
        'meeting_notes': 0,
        'news': 0
    }
    # Get only the tags used
    posts = Posts.query.filter_by(deleted=False).all()
    tags_counter = {}
    for tag in choices.TAGS:
        tags_counter[tag] = 0
    # Count the number of times each tag appears in all posts
    for post in posts:
        posts_counter[post.post_type] = posts_counter[post.post_type] + 1
        for tag in post.tags:
            tags_counter[tag] = tags_counter[tag] + 1
    sorted_tags = []
    # Resort the tags in alphabetical order
    for key in sorted(tags_counter.keys()):
        if tags_counter[key] != 0:
            sorted_tags.append((key, tags_counter[key]))

    search_term = flask_request.args.get('search_term', None)
    return render_template('news_and_updates.html', tags=sorted_tags, search_term=search_term, posts_counter=posts_counter)


@main.route('/posts/search/', methods=['GET'])
def search_posts():
    """
    AJAX endpoint to handle querying the database for Posts objects on the News and Updates pages

    GET Request
    Expected arguments:
    - sort_by: a string containing the currently selected option in the Sort By dropdown. Default value is 'Date(Newest)'.
    - search_term: a string containing the search term that was entered in the Search By field.
    - post_type: an array of strings containing the post types to be filtered on.
    - tags: an array of strings containing the tags selected to filter on.
    - posts_start: an integer for the start range of posts to be displayed.
    - posts_end: an integer for the end range of posts to be displayed.
    - meeting_type: an array of strings containing the meeting types to be filtered on.
    :return: A JSON with the rendered templates for post rows based on the search criteria
             and values to determine what range is being displayed on screen.
    """
    # Get passed in arguments
    sort_by = flask_request.args.get('sort_by', 'all')
    search_term = flask_request.args.get('search_term', None)
    post_type = flask_request.args.getlist('post_type[]')
    tags = flask_request.args.getlist('tags[]', None)
    posts_start = flask_request.args.get('posts_start', type=int)
    posts_end = flask_request.args.get('posts_end', type=int)
    meeting_type = flask_request.args.getlist('meeting_type[]', None)

    # Query the Posts table based on filters. Then process the templates to be rendered.
    data = process_posts_search(post_type=post_type,
                                sort_by=sort_by,
                                search_term=search_term,
                                tags=tags,
                                posts_start=posts_start,
                                posts_end=posts_end,
                                meeting_type=meeting_type)
    return jsonify(data)


@main.route('/news-and-updates/meeting-notes', methods=['GET'])
def meeting_notes():
    """
    View function to handle the meeting notes landing page
    Renders the page as empty then uses ajax to fill in the post rows
    :return: HTML template for meeting notes landing page
    """
    meeting_type_counter = {
        'Division': 0,
        'Strategic Planning': 0,
        'Senior Staff': 0,
        'Project': 0,
        'Agency': 0
    }
    # Get only the tags used
    posts = Posts.query.filter_by(post_type='meeting_notes', deleted=False).all()
    tags_counter = {}
    for tag in choices.TAGS:
        tags_counter[tag] = 0
    # Count the number of times each tag appears in all posts
    for post in posts:
        meeting_type_counter[post.meeting_type] = meeting_type_counter[post.meeting_type] + 1
        for tag in post.tags:
            tags_counter[tag] = tags_counter[tag] + 1
    sorted_tags = []
    # Resort the tags in alphabetical order
    for key in sorted(tags_counter.keys()):
        if tags_counter[key] != 0:
            sorted_tags.append((key, tags_counter[key]))

    # Get meeting type choices
    meeting_types = choices.MEETING_TYPES[1::]

    return render_template('meeting_notes.html', posts=posts, meeting_types=meeting_types, tags=sorted_tags, meeting_type_counter=meeting_type_counter)


@main.route('/news-and-updates/news', methods=['GET'])
def news():
    """
    View function to handle the news landing page
    Renders the page as empty then uses ajax to fill in the post rows
    :return: HTML template for news landing page
    """
    # Get only the tags used
    posts = Posts.query.filter_by(post_type='news', deleted=False).all()
    tags_counter = {}
    for tag in choices.TAGS:
        tags_counter[tag] = 0
    for post in posts:
        for tag in post.tags:
            tags_counter[tag] = tags_counter[tag] + 1
    sorted_tags = []
    for key in sorted(tags_counter.keys()):
        if tags_counter[key] != 0:
            sorted_tags.append((key, tags_counter[key]))

    return render_template('news.html', posts=posts, tags=sorted_tags)


@main.route('/news-and-updates/events', methods=['GET'])
def events():
    """
    View function to handle the events calendar page
    :return: HTML template for events calendar page
    """
    return render_template('calendar.html')


# Alternate view function for a list view of events. Currently not being used but may need to be implemented later on.
# @main.route('/news-and-updates/events', methods=['GET'])
# def events():
#     """
#     View function to handle the events landing page
#     Queries for posts that are type events and visible and paginates them
#     :return: HTML template for events landing page
#     """
#     # Set up pagination
#     page = flask_request.args.get('page', 1, type=int)
#     posts = Posts.query.filter_by(post_type='event_posts', deleted=False).order_by(Posts.date_created.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], True)
#
#     # Get filter choices
#     tags = choices.TAGS
#
#     return render_template('events.html', posts=posts, tags=tags)


@main.route('/get_events/', methods=['GET'])
def get_events():
    """
    AJAX endpoint to retrieve all EventPosts for a given month and year

    :return: a JSON containing the dates from the query and HTML templates to the event rows section
    """
    # Create JSON to be returned by AJAX
    data = {
        'dates': [],
        'template': ''
    }

    # Query for all EventPosts in that month and year
    month = flask_request.args.get('month')
    year = flask_request.args.get('year')
    posts = EventPosts.query.filter(extract('month', EventPosts.event_date) == month,
                                    extract('year', EventPosts.event_date) == year,
                                    Posts.deleted == False).order_by(EventPosts.event_date.asc()).all()

    # Format dates to be MM/DD/YYYY
    dates = []
    for post in posts:
        dates.append(post.event_date.strftime("%m/%d/%Y "))
    data['dates'] = dates

    # Render event row templates for frontend
    if len(dates) > 0:
        data['template'] = render_template('event_rows.html', posts=posts)
    else:
        data['template'] = render_template('no_event_rows_message.html')

    return jsonify(data), 200


@main.route('/news-and-updates/meeting-notes/new', methods=['GET', 'POST'])
@login_required
def new_meeting_notes():
    """
    View function to handle creating a new MeetingNotes post

    GET Request:
    Returns HTML template to render the Meeting Notes form

    POST Request:
    Expects a properly validated Meeting Notes form to create a MeetingNotes object
    """
    form = MeetingNotesForm()
    users = []
    for user in Users.query.order_by(Users.last_name):
        users.append(user.name)
    tags = choices.TAGS

    if flask_request.method == 'POST' and form.validate_on_submit():
        post_id = create_meeting_notes(meeting_date=form.meeting_date.data,
                                       meeting_location=form.meeting_location.data,
                                       meeting_leader=form.meeting_leader.data.title(),
                                       meeting_note_taker=form.meeting_note_taker.data.title(),
                                       start_time=form.start_time.data,
                                       end_time=form.end_time.data,
                                       attendees=flask_request.form.getlist('attendees'),
                                       next_meeting_date=form.next_meeting_date.data,
                                       next_meeting_leader=form.next_meeting_leader.data.title(),
                                       next_meeting_note_taker=form.next_meeting_note_taker.data.title(),
                                       meeting_type=form.meeting_type.data,
                                       division=form.division.data,
                                       author=current_user.id,
                                       title=form.title.data,
                                       content=form.content.data,
                                       tags=flask_request.form.getlist('tags'))
        return redirect(url_for('main.view_post', post_id=post_id))
    return render_template('new_meeting_notes.html', form=form, users=users, tags=tags)


@main.route('/news-and-updates/news/new', methods=['GET', 'POST'])
@login_required
def new_news():
    """
    View function to handle creating a new News post

    GET Request:
    Returns HTML template to render the News form

    POST Request:
    Expects a properly validated News form to create a News object
    """
    form = NewsForm()
    tags = choices.TAGS

    if flask_request.method == 'POST' and form.validate_on_submit():
        post_id = create_news(author=current_user.id,
                              title=form.title.data,
                              content=form.content.data,
                              tags=flask_request.form.getlist('tags'))
        return redirect(url_for('main.view_post', post_id=post_id))
    return render_template('new_news.html', form=form, tags=tags)


@main.route('/news-and-updates/events/new', methods=['GET', 'POST'])
@login_required
def new_event_post():
    """
    View function to handle creating a new EventPost post

    GET Request:
    Returns HTML template to render the Event form

    POST Request:
    Expects a properly validated Event form to create a EventPosts object
    """
    form = EventForm()
    users = []
    for user in Users.query.order_by(Users.last_name):
        users.append(user.name)
    tags = choices.TAGS

    if flask_request.method == 'POST' and form.validate_on_submit():
        post_id = create_event_post(event_date=form.event_date.data,
                                    event_location=form.event_location.data,
                                    event_leader=form.event_leader.data.title(),
                                    start_time=form.start_time.data,
                                    end_time=form.end_time.data,
                                    sponsor=form.sponsor.data,
                                    author=current_user.id,
                                    title=form.title.data,
                                    content=form.content.data,
                                    tags=flask_request.form.getlist('tags'))
        return redirect(url_for('main.view_post', post_id=post_id))
    return render_template('new_event_post.html', form=form, users=users, tags=tags)


@main.route('/news-and-updates/view-post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    """
    View function to handle viewing a single post
    Convert the date_created to EST when passed to the front end
    :param post_id: ID of the Post object being viewed
    :return: HTML template to view a single post
    """
    post = Posts.query.filter_by(id=post_id,deleted=False).first()
    if not post:
        return render_template('404.html'), 404
    post_timestamp = post.date_created.replace(tzinfo=pytz.utc)
    post_timestamp = post_timestamp.astimezone(pytz.timezone("America/New_York"))
    author = Users.query.filter_by(id=post.author).first()
    return render_template('view_post.html', post=post, post_timestamp=post_timestamp, author=author)


@main.route('/get_user_list/', methods=['GET'])
@login_required
def get_user_list():
    """
    AJAX endpoint to retrieve a list of all users for autocomplete choices

    :return: a JSON with all users that can be entered using autocomplete
    """
    users_list = []
    for user in Users.query.all():
        users_list.append(user.name)
    return jsonify(users_list), 200


# End view functions for posting

@main.route('/staff-directory', methods=['GET', 'POST'])
def staff_directory():
    """
    View function to handle the staff directory page.
    Searches the Users table based on the filter and returns a list of users matching the input.

    GET Request:
    Returns HTML template for the staff directory page

    POST Request:
    Expects data from the staff directory search form
    On initial page load it will return a list of all users
    Following POST requests will use what is inputted in the search field and what filter is used in order to query
    """
    form = StaffDirectorySearchForm()

    if form.search.data == "":
        users = Users.query.filter(Users.is_active==True).order_by(Users.last_name)
    elif form.filters.data == 'First Name':
        users = Users.query.filter(Users.first_name.ilike('%' + form.search.data + '%'), Users.is_active==True)
    elif form.filters.data == 'Last Name':
        users = Users.query.filter(Users.last_name.ilike('%' + form.search.data + '%'), Users.is_active==True)
    elif form.filters.data == 'Division':
        users = Users.query.filter(Users.division.ilike('%' + form.search.data + '%'), Users.is_active==True)
    elif form.filters.data == 'Title':
        users = Users.query.filter(Users.title.ilike('%' + form.search.data + '%'), Users.is_active==True)
    else:  # on initial page load return all users
        users = Users.query.filter(Users.is_active==True).order_by(Users.last_name)

    return render_template('staff_directory.html', users=users, form=form)


@main.route('/get_filter_options_list/<string:filter_value>', methods=['GET'])
def get_filter_options_list(filter_value):
    """
    AJAX endpoint to retrieve a list of autocomplete choices for each filter option

    GET Request:
    Uses filter_value which is passed in, in order to return a list of choices

    :param filter_value: string containing which filter is currently selected
    :return: a JSON with all possible choices that can be searched for with autocomplete
    """
    choices_list = []

    if filter_value == "First Name":
        choices_list = [u[0] for u in Users.query.with_entities(Users.first_name).all()]

    if filter_value == "Last Name":
        choices_list = [u[0] for u in Users.query.with_entities(Users.last_name).all()]

    if filter_value == "Division":
        choices_list = [u[0] for u in Users.query.with_entities(Users.division).all()]

    if filter_value == "Title":
        choices_list = [u[0] for u in Users.query.with_entities(Users.title).all()]

    # Remove duplicates in the list
    choices_list = list(set(choices_list))
    return jsonify(choices_list), 200


@main.route('/our-mission', methods=['GET'])
def our_mission():
    """
    View function to handle the Our Mission page
    :return: HTML template for the Our Mission page
    """
    return render_template('our_mission.html')


@main.route('/contact', methods=['GET'])
def contact():
    """
    View function to handle the contact page
    :return: HTML template for the contact page
    """
    return render_template('contact.html')


@main.route('/divisions', methods=['GET'])
def divisions():
    """
    View function to handle the divisions page
    :return: HTML template for the divisions page
    """
    return render_template('divisions.html')


@main.route('/divisions/<string:division_name>', methods=['GET'])
def division_pages(division_name):
    """
    View function to handle an individual division page
    :param division_name: String for the division name in the URL. Uses '-' in place of spaces
    :return: HTML template for an individual division page
    """
    users = get_users_by_division(choices.DIVISION_PAGES[division_name]['plain_text'])
    rooms = get_rooms_by_division(choices.DIVISION_PAGES[division_name]['plain_text'])
    return render_template(
        'divisions/{division_name}.html'.format(division_name=choices.DIVISION_PAGES[division_name]['template_name']),
        users=users, rooms=rooms)


@main.route('/it-support', methods=['GET'])
def it_support():
    """
    View function to handle the IT support page
    :return: HTML template for the IT support page
    """
    return render_template('it_support.html')


@main.route('/it-support/faq', methods=['GET'])
def faq():
    """
    View function to handle the FAQ page
    :return: HTML template for the FAQ page
    """
    return render_template('faq.html')


@main.route('/employee-resources', methods=['GET'])
def employee_resources():
    """
    View function to handle the employee resources page
    :return: HTML template for the employee resources page
    """
    return render_template('employee_resources.html')


@main.route('/employee-resources/employee-benefits', methods=['GET'])
def employee_benefits():
    """
    View function to handle the employee benefits page
    :return: HTML template for the employee benefits page
    """
    return render_template('employee_benefits.html')


@main.route('/employee-resources/orientation', methods=['GET'])
def orientation():
    """
    View function to handle the orientation page
    :return: HTML template for the orientation page
    """
    return render_template('orientation.html')


@main.route('/tools-and-applications', methods=['GET'])
def tools_and_applications():
    """
    View function to handle the tools and applications page
    :return: HTML template for the toold and applications page
    """
    return render_template('tools_and_applications.html')


@main.route('/enfg', methods=['GET', 'POST'])
def enfg():
    """
    View function to handle the Easy Not Found Generator page

    GET Request:
    Returns the html template for the ENFG page

    POST Request:
    Handles submission of ENFG form. If it is validated, redirect to the enfg_result function
    """
    form = EnfgForm()

    if form.validate_on_submit():
        session['type'] = form.type.data
        session['name'] = form.name.data
        session['bride_name'] = form.bride_name.data
        session['year'] = form.year.data
        session['borough'] = ', '.join(form.borough.data)
        session['signature'] = form.signature.data
        return redirect(url_for('main.enfg_result'))
    return render_template('enfg.html', form=form)


@main.route('/enfg/result', methods=['GET'])
def enfg_result():
    """
    View function to display the output of the Easy Not Found Generator form
    :return: HTML template for the ENFG result with data passed in from the successful form submission
    """
    return render_template('enfg_result.html',
                           date=datetime.today().strftime("%m/%d/%y"),
                           type=session.get('type'),
                           name=session.get('name'),
                           bride_name=session.get('bride_name'),
                           year=session.get('year'),
                           borough=session.get('borough'),
                           signature=session.get('signature'))


@main.route('/strategic-planning', methods=['GET'])
def strategic_planning():
    """
    View function to handle the Strategic Planning page
    :return: HTML template for the Strategic Planning page
    """
    return render_template('strategic_planning.html')


@main.route('/it-support/app-dev-intake-form', methods=['GET', 'POST'])
@login_required
def app_dev_intake_form():
    """
    View function to handle the IT Intake Form.

    GET Request:
    Returns the html template for the Intake Form

    POST Request:
    Handles submission of Intake form. If it is validated, redirect to the IT Support page
    """
    form = AppDevIntakeForm()

    # Pre-Fill the Submitter Information - Cannot be edited
    form.submitter_name.data = current_user.name
    form.submitter_email.data = current_user.email
    form.submitter_phone.data = current_user.phone_number
    form.submitter_title.data = current_user.title
    form.submitter_division.data = current_user.division

    if flask_request.method == 'GET':
        # Pre-Fill the Designated Business Owner Information with the Submitters Information - Can be Edited
        form.designated_business_owner_name.data = current_user.name
        form.designated_business_owner_email.data = current_user.email
        form.designated_business_owner_phone.data = current_user.phone_number
        form.designated_business_owner_title.data = current_user.title
        form.designated_business_owner_division.data = current_user.division

    if form.validate_on_submit():
        email = render_email(form.data, 'email/email_app_dev_intake.html')
        sender = form.submitter_email.data
        recipients = current_app.config['APP_DEV_INTAKE_EMAIL_RECIPIENTS'] + [form.submitter_email.data,
                                                                              form.designated_business_owner_email.data]
        msg = Message(
            "App. Dev. Intake Form - {project_name}".format(
                project_name=form.project_name.data
            ),
            sender=sender,
            recipients=recipients,
        )
        msg.html = email
        if form.supplemental_materials_one.data is not None:
            tmp_file = BytesIO()
            flask_request.files['supplemental_materials_one'].save(tmp_file)
            tmp_file.seek(0)
            msg.attach(filename=form.supplemental_materials_one.data.filename,
                       content_type=form.supplemental_materials_one.data.content_type, data=tmp_file.read())
        if form.supplemental_materials_two.data is not None:
            tmp_file = BytesIO()
            flask_request.files['supplemental_materials_two'].save(tmp_file)
            tmp_file.seek(0)
            msg.attach(filename=form.supplemental_materials_two.data.filename,
                       content_type=form.supplemental_materials_two.data.content_type, data=tmp_file.read())
        if form.supplemental_materials_three.data is not None:
            tmp_file = BytesIO()
            flask_request.files['supplemental_materials_three'].save(tmp_file)
            tmp_file.seek(0)
            msg.attach(filename=form.supplemental_materials_three.data.filename,
                       content_type=form.supplemental_materials_three.data.content_type, data=tmp_file.read())
        mail.send(msg)
        flash("Successfully submitted intake form. Please allow 5 business days for a response.")
        return redirect(url_for('main.it_support'))
    else:
        for error in form.errors.items():
            flash(error[1][0], category="danger")
    return render_template("app_dev_intake.html", form=form, current_user=current_user)


@main.route('/documents', methods=['GET'])
def documents():
    """
    View function to handle Documents page
    :return: HTML template for the Documents page
    """
    # default_open determines which documents tab is opened on initial load. if no value is supplied use 'instructions'
    default_open = flask_request.args.get('default_open', 'instructions')
    return render_template('documents.html', default_open=default_open)


@main.route('/documents/search/', methods=['GET'])
def search_documents():
    """
    AJAX endpoint to handle querying the database for Documents objects on the documents page

    GET Request
    Expected arguments:
    - sort_by: a string containing the currently selected option in the Sort By dropdown. Default value is 'all'
    - search_term: a string containing the search term that was entered in the Search By field.
    - page_counters: a JSON that keeps track of what range of each document type is visible on the screen.
                     #TODO: We can probably take this out since every call to this end point will start at 0 and end at 10
    :return: A JSON with the rendered templates of each document type table based on the search criteria
             and values to determine what range is being displayed on screen.
    """
    # Get passed in arguments
    sort_by = flask_request.args.get('sort_by', 'all')
    search_term = flask_request.args.get('search_term', None)
    page_counters = json.loads(flask_request.args.get('page_counters'))

    # TODO (@joelbcastillo): This endpoint should take in the specific tab that is open to reduce the amount of data returned.
    #                        We shouldn't be pulling data from every single tab every time we hit this endpoint.

    # Query the Documents table based on the search term and sort value. Then process the templates to be rendered.
    instructions_data = process_documents_search(document_type_plain_text='Instructions',
                                                 document_type='instructions',
                                                 sort_by=sort_by,
                                                 search_term=search_term,
                                                 documents_start=page_counters['instructions']['start'],
                                                 documents_end=page_counters['instructions']['end'])

    policies_and_procedures_data = process_documents_search(document_type_plain_text='Policies and Procedures',
                                                            document_type='policies-and-procedures',
                                                            sort_by=sort_by,
                                                            search_term=search_term,
                                                            documents_start=page_counters['policies_and_procedures']['start'],
                                                            documents_end=page_counters['policies_and_procedures']['end'])

    templates_data = process_documents_search(document_type_plain_text='Templates',
                                              document_type='templates',
                                              sort_by=sort_by,
                                              search_term=search_term,
                                              documents_start=page_counters['templates']['start'],
                                              documents_end=page_counters['templates']['end'])

    training_materials_data = process_documents_search(document_type_plain_text='Training Materials',
                                                       document_type='training-materials',
                                                       sort_by=sort_by,
                                                       search_term=search_term,
                                                       documents_start=page_counters['training_materials']['start'],
                                                       documents_end=page_counters['training_materials']['end'])
    covid_19_information_data = process_documents_search(document_type_plain_text='COVID-19 Information',
                                                         document_type='covid-19-information',
                                                         sort_by=sort_by,
                                                         search_term=search_term,
                                                         documents_start=page_counters['covid_19_information']['start'],
                                                         documents_end=page_counters['covid_19_information']['end'])
    # Create a dictionary with data for each document type to be passed back to the frontend.
    data = {
        'instructions_data': instructions_data,
        'policies_and_procedures_data': policies_and_procedures_data,
        'templates_data': templates_data,
        'training_materials_data': training_materials_data,
        'covid_19_information_data': covid_19_information_data
    }

    return jsonify(data)


@main.route('/documents/page/', methods=['GET'])
def change_documents_page():
    """
    AJAX endpoint to handle clicking the prev/next buttons and getting the next set of rows to display
    Instead of querying all 4 document types like in search_documents() we only have to query for one document type
    Then get the previous or next set of 10 rows to be displayed
    :return: A JSON with the rendered templates for the currently viewed document type table based on the search criteria
             and values to determine what range is being displayed on screen.
    """
    # Get passed in arguments
    sort_by = flask_request.args.get('sort_by', 'all')
    search_term = flask_request.args.get('search_term', None)
    page_counters = json.loads(flask_request.args.get('page_counters'))
    document_type_plain_text = flask_request.args.get('document_type_plain_text')
    document_type_underscore = flask_request.args.get('document_type_underscore')
    document_type_dash = flask_request.args.get('document_type_dash')
    # TODO: Find a better way to standardize document type variable values when passed in as arguments.
    # Naming conventions of variable names are different between Python, Javascript, and HTML
    # which leads to inconsistent variable names.
    # Python uses underscores
    # Javascript uses underscores and camel case
    # HTML uses dashes
    # Database was originally designed to store the plain text names of document types

    # Query the databse for the next set of rows to display based on document_start and document_end
    data = process_documents_search(document_type_plain_text=document_type_plain_text,
                                    document_type=document_type_dash,
                                    sort_by=sort_by,
                                    search_term=search_term,
                                    documents_start=page_counters[document_type_underscore]['start'],
                                    documents_end=page_counters[document_type_underscore]['end'])

    return jsonify(data)


@main.route('/documents/upload', methods=['GET', 'POST'])
@login_required
def upload_document():
    """
    View function to handle uploading a new document to the documents library

    GET Request
    Renders the template for the upload form on initial page load

    POST Request
    Handles the submission of the upload form and savining it to the database if it passes validation and virus scanning
    """
    form = UploadForm()
    if flask_request.method == 'POST' and form.validate_on_submit():
        file = flask_request.files['file_object']
        filename = secure_filename(file.filename) # use the secure version of the file name
        # Files are unique in both file title and file name, this will be used to check if a file already exists in the database
        # TODO: check file uniqueness using a checksum instead of just filename
        file_exists = Documents.query.filter(or_(Documents.file_name == filename, Documents.file_title == form.file_title.data)).first() or None
        if file_exists:
            if file_exists.file_name == filename: # File with the same name already exists
                flash('This file has already been uploaded. Please select another file.')
                return render_template('upload_document.html', form=form)
            elif file_exists.file_title == form.file_title.data: # file with the same title already exists
                flash('A file with this title has already been uploaded. Please use another title.')
                return render_template('upload_document.html', form=form)
        elif not allowed_file(filename):
            # Files should fall under the list allowed file types
            flash('Invalid file type.')
            return render_template('upload_document.html', form=form)
        # Handle virus scanning
        try:
            file_path = os.path.join(current_app.config['FILE_UPLOAD_PATH'], filename)
            file.save(file_path)
            scan_file(file_path)
        except VirusDetectedException:
            flash('Virus detected. Please contact IT for assistance.')
            return render_template('upload_document.html', form=form)
        # Create Document object
        create_document(uploader_id=current_user.id,
                        file_title=form.file_title.data,
                        file_name=filename,
                        document_type=form.document_type.data,
                        file_type=filename.rsplit('.', 1)[1].lower(),
                        file_path=file_path,
                        division=form.division.data)
        flash('Document successfully uploaded.')
        return redirect(url_for('main.documents'))
    return render_template('upload_document.html', form=form)


@main.route('/return-file/<string:file_name>', methods=['GET', 'POST'])
def return_file(file_name):
    try:
        return send_file(os.path.join(current_app.config['FILE_UPLOAD_PATH'], file_name), attachment_filename=file_name)
    except Exception as e:
        return str(e)


@main.route('/monitor', methods=['GET', 'POST'])
#@login_required
def monitor():
    """
    AJAX endpoint and VIEW function to service requests to check if a list of websites are alive or not. Checks if the
    websites listed are still alive and updates the database records accordingly. If GET, then return webpage.
    :return JSON response with fields describing if the requested websites are still alive or not and the latest updated
            status.
    """

    if flask_request.method == 'POST':

        # For each URL requested, find out if the website is still working and update the server.
        url = flask_request.form['url']
        table_entry = Monitor.query.filter_by(url=url).first()

        # Add timezone information to timestamp
        current_timestamp = pytz.utc.localize(table_entry.current_timestamp)
        last_success_timestamp = pytz.utc.localize(table_entry.last_success_timestamp)

        return jsonify({
            'status_code': table_entry.status_code,
            'current_timestamp': current_timestamp.astimezone(
                                                pytz.timezone('America/New_York')).strftime('%m/%d/%Y, %I:%M:%S %p'),
            'most_recent_success': last_success_timestamp.astimezone(
                                                pytz.timezone('America/New_York')).strftime('%m/%d/%Y, %I:%M:%S %p'),
            'reason': table_entry.response_header
        })

    websites = Monitor.query.order_by(Monitor.id.asc()).all()

    return render_template('monitor.html', websites=websites,
                                           site_refresh_rate=current_app.config['FRONTEND_RESOLUTION'])
