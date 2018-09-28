from flask import render_template, redirect, url_for, flash, session, request as flask_request
from flask_login import login_required
from app import db
from . import main
from app.main.forms import Meeting_Notes_Form, EnfgForm
from app.main.utils import create_post
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/news-updates', methods=['GET', 'POST'])
def news_and_updates():
    return render_template('news_and_updates.html')


@main.route('/news-updates/new', methods=['GET', 'POST'])
@login_required
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
