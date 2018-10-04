from flask import render_template, redirect, url_for, flash, session, request as flask_request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Users, Posts, MeetingNotes
from . import main
from app.main.forms import MeetingNotesForm, StaffDirectorySearchForm, EnfgForm
from app.main.utils import create_meeting_notes
from datetime import datetime
from app.constants import choices

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    View function to handle the home page
    :return: HTML template for home page
    """
    posts = Posts.query.all()
    print(posts)
    return render_template('index.html', posts=posts)


@main.route('/news-updates', methods=['GET', 'POST'])
def news_and_updates():
    """
    View function to handle the new and updates landing page
    :return: HTML template for new and updates landing page
    """
    return render_template('news_and_updates.html')


@main.route('/news-updates/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = MeetingNotesForm()
    users = []
    for user in Users.query.order_by(Users.last_name):
        users.append(user.name)
    tags = choices.TAGS

    if flask_request.method == 'POST':
        post_id = create_meeting_notes(meeting_date=form.meeting_date.data,
                             meeting_location=form.meeting_location.data,
                             meeting_leader=form.meeting_leader.data,
                             meeting_note_taker=form.meeting_note_taker.data,
                             start_time=form.start_time.data,
                             end_time=form.end_time.data,
                             attendees=flask_request.form.getlist('attendees'),
                             next_meeting_date=form.next_meeting_date.data,
                             next_meeting_leader=form.next_meeting_leader.data,
                             next_meeting_note_taker=form.next_meeting_note_taker.data,
                             meeting_type=form.meeting_type.data,
                             division=form.division.data,
                             author=current_user.id,
                             title=form.title.data,
                             content=form.content.data,
                             tags=flask_request.form.getlist('tags'))
        return redirect(url_for('main.view_post', post_id=post_id))
    return render_template('new_meeting_notes.html', form=form, users=users, tags=tags)


@main.route('/news-updates/view/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    author = Users.query.filter_by(id=post.author).first()
    return render_template('view_post.html', post=post, author=author)


@main.route('/get_user_list/', methods=['GET'])
def get_user_list():
    """
    AJAX endpoint to retrieve a list of all users for autocomplete choices

    :return: a JSON with all users that can be entered using autocomplete
    """
    users_list = []
    for user in Users.query.all():
        users_list.append(user.name)
    return jsonify(users_list), 200


@main.route('/staff-directory', methods=['GET', 'POST'])
def staff_directory():
    """
    View function to handle the staff directory page.
    Searches the Users table based on the filter and returns a list of users matching the input.

    GET Request:
    Returns HTML template for the staff directory page

    POST Request:
    Expects dat from the staff directory search form
    On initial page load it will return a list of all users
    Following POST requests will use what is inputted in the search field and what filter is used in order to query
    """
    form = StaffDirectorySearchForm()

    if form.search.data is "":
        users = Users.query.order_by(Users.last_name)
    elif form.filters.data == 'First Name':
        users = Users.query.filter(Users.first_name.ilike('%' + form.search.data + '%'))
    elif form.filters.data == 'Last Name':
        users = Users.query.filter(Users.last_name.ilike('%' + form.search.data + '%'))
    elif form.filters.data == 'Division':
        users = Users.query.filter(Users.division.ilike('%' + form.search.data + '%'))
    elif form.filters.data == 'Title':
        users = Users.query.filter(Users.title.ilike('%' + form.search.data + '%'))
    else: # on initial page load return all users
        users = Users.query.order_by(Users.last_name)

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


@main.route('/our-mission', methods=['GET', 'POST'])
def our_mission():
    """
    View function to handle the Our Mission page
    :return: HTML template for the Our Mission page
    """
    return render_template('our_mission.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    View function to handle the contact page
    :return: HTML template for the contact page
    """
    return render_template('contact.html')


@main.route('/divisions', methods=['GET', 'POST'])
def divisions():
    """
    View function to handle the divisions page
    :return: HTML template for the divisions page
    """
    return render_template('divisions.html')


@main.route('/it-support', methods=['GET', 'POST'])
def it_support():
    """
    View function to handle the IT support page
    :return: HTML template for the IT support page
    """
    return render_template('it_support.html')


@main.route('/it-support/faq', methods=['GET', 'POST'])
def faq():
    """
    View function to handle the FAQ page
    :return: HTML template for the FAQ page
    """
    return render_template('faq.html')


@main.route('/employee-resources', methods=['GET', 'POST'])
def employee_resources():
    """
    View function to handle the employee resources page
    :return: HTML template for the employee resources page
    """
    return render_template('employee_resources.html')


@main.route('/tools-and-applications', methods=['GET', 'POST'])
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
                           date=datetime.today().strftime("%m/%d/%y "),
                           type=session.get('type'),
                           name=session.get('name'),
                           bride_name=session.get('bride_name'),
                           year=session.get('year'),
                           borough=session.get('borough'),
                           signature=session.get('signature'))
