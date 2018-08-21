from flask import render_template, redirect, url_for, flash, request as flask_request, jsonify
from app import db
from app.models import Users
from . import main
from app.main.forms import Meeting_Notes_Form, Staff_Directory_Search_Form
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
    form = Meeting_Notes_Form()

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
    form = Staff_Directory_Search_Form()
    page = flask_request.args.get('page', 1, type=int)

    if form.search.data is "":
        users = Users.query.order_by(Users.last_name).paginate(page=page, per_page=10)
        next_url = url_for('main.staff_directory', page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('main.staff_directory', page=users.prev_num) \
            if users.has_prev else None
    elif form.filters.data == 'First Name':
        return redirect('/search/'+form.filters.data+'/'+form.search.data)
    elif form.filters.data == 'Last Name':
        return redirect('/search/' + form.filters.data + '/' + form.search.data)
    elif form.filters.data == 'Division':
        return redirect('/search/' + form.filters.data + '/' + form.search.data)
    elif form.filters.data == 'Title':
        return redirect('/search/' + form.filters.data + '/' + form.search.data)
    else:
        users = Users.query.order_by(Users.last_name).paginate(page=page, per_page=10)
        next_url = url_for('main.staff_directory', page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('main.staff_directory', page=users.prev_num) \
            if users.has_prev else None

    return render_template('staff_directory.html', users=users, form=form, page=page, next_url=next_url, prev_url=prev_url)

@main.route('/search/<string:filter>/<string:input>', methods=['GET', 'POST'])
def show_result(filter,input):
    form = Staff_Directory_Search_Form()
    page = flask_request.args.get('page', 1, type=int)

    if filter == 'First Name':
        users = Users.query.filter(Users.first_name.ilike('%' + input + '%')).paginate(page=page, per_page=10)
        next_url = url_for('search', filter=filter, input=input, page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('search', filter=filter, input=input,  page=users.prev_num) \
            if users.has_prev else None

    elif filter == 'Last Name':
        users = Users.query.filter(Users.last_name.ilike('%' + input + '%')).paginate(page=page, per_page=10)
        next_url = url_for('search', filter=filter, input=input, page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('search', filter=filter, input=input, page=users.prev_num) \
            if users.has_prev else None

    elif filter == 'Division':
        users = Users.query.filter(Users.division.ilike('%' + input + '%')).paginate(page=page, per_page=10)
        next_url = url_for('search', filter=filter, input=input, page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('search', filter=filter, input=input, page=users.prev_num) \
            if users.has_prev else None

    elif filter == 'Title':
        users = Users.query.filter(Users.title.ilike('%' + input + '%')).paginate(page=page, per_page=10)
        next_url = url_for('search', filter=filter, input=input, page=users.next_num) \
            if users.has_next else None
        prev_url = url_for('search', filter=filter, input=input, page=users.prev_num) \
            if users.has_prev else None

    return render_template('search.html', users=users, form=form, page=page, filter=filter, input=input, next_url=next_url, prev_url=prev_url)


@main.route('/get_filter_options_list/<string:filter_value>', methods=['GET'])
def get_filter_options_list(filter_value):
    users = Users.query.all()
    users_array = []
    if filter_value == "First Name":
        for user in users:
            users_array.append(user.first_name)
        users_array = list(set(users_array))
    if filter_value == "Last Name":
        for user in users:
            if user not in users_array:
                users_array.append(user.last_name)
    if filter_value == "Division":
        for user in users:
            users_array.append(user.division)
        users_array = list(set(users_array))
    if filter_value == "Title":
        for user in users:
            users_array.append(user.title)
        users_array = list(set(users_array))

    return jsonify(users_array), 200
