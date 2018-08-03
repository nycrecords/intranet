from flask import render_template, redirect, url_for, flash, request as flask_request, jsonify
from app import db
from . import main
from app.main.forms import Meeting_Notes_Form
from datetime import datetime
from app.main.utils import create_post
from app.main.utils import create_meeting_notes
from app.models import Users
import json


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
        next_meeting_leader = Users.query.filter_by(id=form.next_meeting_leader_id.data).one()
        next_meeting_note_taker = Users.query.filter_by(id=form.next_meeting_note_taker_id.data).one()

        meeting_notes_id = create_meeting_notes(meeting_date=form.meeting_date.data,
                                                meeting_location=form.meeting_location.data,
                                                meeting_leader=form.meeting_leader.data,
                                                meeting_note_taker=form.meeting_note_taker.data,
                                                start_time=form.start_time.data,
                                                end_time=form.end_time.data,
                                                attendees=[],
                                                next_meeting_date=form.next_meeting_date.data,
                                                next_meeting_leader=next_meeting_leader.id,
                                                next_meeting_note_taker=next_meeting_note_taker.id,
                                                meeting_type=form.meeting_type.data,
                                                division=form.division.data)
        print(meeting_notes_id)
        # if form.validate_on_submit():
        flash('Form submitted.')
        return redirect(url_for('main.news_and_updates'))
    return render_template('new_meeting_notes.html', form=form)


@main.route('/get_user_list/', methods=['GET'])
def get_user_list():
    users = Users.query.all()
    users_json = {}
    for user in users:
        users_json[user.id] = user.full_name
    print(users_json)

    return jsonify(users_json), 200
