from flask import render_template, redirect, url_for, flash, request as flask_request
from flask_paginate import Pagination, get_page_parameter
from app import db
from app.models import Users
from . import main
from app.main.forms import Meeting_Notes_Form, Staff_Directory_Search_Form
from datetime import datetime
from app.main.utils import create_post
from sqlalchemy import func


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


    if form.search.data is "":
        users = Users.query.all()
    elif form.filters.data == 'First Name':
        users = Users.query.filter(func.lower(Users.first_name)==func.lower(form.search.data)).all()
    elif form.filters.data == 'Last Name':
        users = Users.query.filter(func.lower(Users.last_name) == func.lower(form.search.data)).all()
    elif form.filters.data == 'Division':
        users = Users.query.filter(func.lower(Users.division) == func.lower(form.search.data)).all()
    elif form.filters.data == 'Title':
        users = Users.query.filter(func.lower(Users.title) == func.lower(form.search.data)).all()
    else:
        users = Users.query.order_by(Users.last_name).all()

    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # pagination = Pagination(page=page, total=users.count())

    return render_template('staff_directory.html', users=users, form=form)
