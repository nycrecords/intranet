from flask import render_template, redirect, url_for, flash
from app import db
from . import main
from app.main.forms import Meeting_Notes_Form
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = Meeting_Notes_Form()
    if form.validate_on_submit():
        flash('Form submitted.')
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form)


@main.route('/news-updates', methods=['GET', 'POST'])
def news_and_updates():
    return render_template('news_and_updates.html')


@main.route('/news-updates/new', methods=['GET', 'POST'])
def new_post():
    form = Meeting_Notes_Form()
    if form.validate_on_submit():
        flash('Form submitted.')
        return redirect(url_for('main.index'))
    return render_template('new_meeting_notes.html', form=form)
