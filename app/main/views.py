from flask import render_template, redirect, url_for, flash
from app import db
from . import main
from app.main.forms import Sign_In_Form
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/news-updates', methods=['GET', 'POST'])
def news_and_updates():
    return render_template('news_and_updates.html')


@main.route('/news-updates/new', methods=['GET', 'POST'])
def new_post():

    return render_template('news_and_updates.html')
