from flask import render_template, redirect, url_for, flash, request as flask_request, jsonify
from app import db
from app.models import Users
from . import main
from app.main.forms import MeetingNotesForm, StaffDirectorySearchForm
from datetime import datetime
from app.main.utils import create_post


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/news-updates', methods=['GET', 'POST'])
def news_and_updates():
    return render_template('news_and_updates.html')


@main.route('/news-updates/new', methods=['GET', 'POST'])
def new_post():
    form = MeetingNotesForm()

    if flask_request.method == 'POST':
        post_id = create_post(title=form.title.data,
                              meeting_date=form.meeting_date.data)
        print(post_id)

        # if form.validate_on_submit():
        flash('Form submitted.')
        return redirect(url_for('main.news_and_updates'))
    return render_template('new_meeting_notes.html', form=form)


@main.route('/staff-directory', methods=['GET', 'POST'])
def staff_directory():
    """
    Searches the Users table based on the filter and returns a list of users matching the input
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
    else:
        users = Users.query.order_by(Users.last_name)

    return render_template('staff_directory.html', users=users, form=form)


@main.route('/get_filter_options_list/<string:filter_value>', methods=['GET'])
def get_filter_options_list(filter_value):
    """
    Sets the autocomplete choices for each filter option

    :param filter_value: string containing which filter is currently selected
    :return: a JSON with all possible choices that can be searched for with autocomplete
    """
    users = Users.query.all()
    choices_array = []

    if filter_value == "First Name":
        for user in users:
            choices_array.append(user.first_name)

    if filter_value == "Last Name":
        for user in users:
            choices_array.append(user.last_name)

    if filter_value == "Division":
        for user in users:
            choices_array.append(user.division)

    if filter_value == "Title":
        for user in users:
            choices_array.append(user.title)

    # Remove duplicates in the list
    choices_array = list(set(choices_array))
    return jsonify(choices_array), 200


@main.route('/it-support/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html')


@main.route('/employee-resources', methods=['GET', 'POST'])
def employee_resources():
    return render_template('employee_resources.html')


@main.route('/tools-and-applications', methods=['GET', 'POST'])
def tools_and_applications():
    return render_template('tools_and_applications.html')


@main.route('/it-support', methods=['GET', 'POST'])
def it_support():
    return render_template('it_support.html')
