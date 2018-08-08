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




@main.route('/staff-directory/<int:page_num>', methods=['GET', 'POST'])
def staff_directory(page_num):
    form = Staff_Directory_Search_Form()
    num=page_num

    if form.search.data is "":
        users = Users.query.order_by(Users.last_name).paginate(per_page=10, page=page_num)
    elif form.filters.data == 'First Name':
        users = Users.query.filter(Users.first_name.ilike('%'+form.search.data+'%')).paginate(per_page=10, page=page_num)
    elif form.filters.data == 'Last Name':
        users = Users.query.filter(Users.last_name.ilike('%' + form.search.data + '%')).paginate(per_page=10, page=page_num)
    elif form.filters.data == 'Division':
        users = Users.query.filter(Users.division.ilike('%'+form.search.data+'%')).paginate(per_page=10, page=page_num)
    elif form.filters.data == 'Title':
        users = Users.query.filter(Users.title.ilike('%' + form.search.data + '%')).paginate(per_page=10, page=page_num)
    else:
        users = Users.query.order_by(Users.last_name).paginate(per_page=10, page=page_num)

    return render_template('staff_directory.html', users=users, form=form, num=num)


@main.route('/get_user_first_names/', methods=['GET'])
def get_user_list():

    # if option=='First Name':
    #     users=Users.query.filter(Users.first_name)
    # elif option=='Last Name':
    #     users=Users.query.filter(Users.last_name)
    # elif option=='Division':
    #     users=Users.query.filter(Users.division)
    # elif option=='Title':
    #     users=Users.query.filter(Users.title)
    # else:

    users = Users.query.all()
    users_array = []
    for user in users:
        users_array.append(user.first_name)

    return jsonify(users_array), 200

@main.route('/get_user_last_names/', methods=['GET'])
def get_user_list():
    users = Users.query.all()
    users_array = []
    for user in users:
        users_array.append(user.last_name)

    return jsonify(users_array), 200

@main.route('/get_user_division/', methods=['GET'])
def get_user_list():
    users = Users.query.all()
    users_array = []
    for user in users:
        users_array.append(user.division)

    return jsonify(users_array), 200

@main.route('/get_user_title/', methods=['GET'])
def get_user_list():
    users = Users.query.all()
    users_array = []
    for user in users:
        users_array.append(user.title)

    return jsonify(users_array), 200