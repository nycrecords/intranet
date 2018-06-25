from flask import render_template, redirect, url_for, flash
from app import db
from app.models import Sign_In
from . import main
from app.main.forms import Sign_In_Form
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    form = Sign_In_Form()

    if form.validate_on_submit():
        for field in form:
            if field.data is '':
                field.data = None
        first_name = form.first_name.data
        last_name = form.last_name.data
        affiliation = form.affiliation.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        country = form.country.data
        library = form.library.data
        archives = form.archives.data
        genealogy = form.genealogy.data
        timestamp = datetime.now()

        new_user_sign_in = Sign_In(first_name=first_name,
                                   last_name=last_name,
                                   affiliation=affiliation,
                                   email=email,
                                   phone=phone,
                                   address=address,
                                   city=city,
                                   state=state,
                                   zipcode=zipcode,
                                   country=country,
                                   library=library,
                                   archives=archives,
                                   genealogy=genealogy,
                                   timestamp=timestamp)
        db.session.add(new_user_sign_in)
        db.session.commit()
        flash('Form submitted.')
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form)
