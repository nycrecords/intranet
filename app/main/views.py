from flask import render_template, redirect, url_for, flash, request as flask_request
from app import db
from . import main
from app.main.forms import Meeting_Notes_Form, Login_Form
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


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    return render_template('login.html',form=form)


@main.route('/our-mission', methods=['GET', 'POST'])
def our_mission():
    return render_template('our_mission.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@main.route('/divisions', methods=['GET', 'POST'])
def divisions():
    return render_template('divisions.html')


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