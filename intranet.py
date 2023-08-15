#!/usr/bin/env python
import os
from flask_migrate import Migrate
from flask.cli import main
from flask import render_template, current_app

from app import create_app, db
from app.models import Documents, EventPosts, Events, MeetingNotes, Monitor, News, Posts, Roles, Users

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        Roles=Roles,
        Users=Users,
        Posts=Posts,
        MeetingNotes=MeetingNotes,
        Monitor=Monitor,
        News=News,
        EventPosts=EventPosts,
        Events=Events,
        Documents=Documents
    )


@app.cli.command
def reset_database():
    """Setup the database."""
    from flask_migrate import upgrade
    from subprocess import call

    # Reset the database
    call(['sudo', 'service', 'rh-postgresql95-postgresql', 'restart'])
    call(['sudo', '-u', 'postgres', '/opt/rh/rh-postgresql95/root/usr/bin/dropdb', 'intranet'])
    call(['sudo', '-u', 'postgres', '/opt/rh/rh-postgresql95/root/usr/bin/createdb', 'intranet'])

    # Run migrations
    upgrade()

    # pre-populate
    list(
        map(
            lambda x: x.populate(),
            (
                Roles,
                Users
            )
        )
    )


@app.cli.command
def deploy():
    """Upgrade and pre-populate database"""
    from flask_migrate import upgrade
    # Run migrations
    upgrade()

    # pre-populate
    list(
        map(
            lambda x: x.populate(),
            (
                Roles,
                Users
            )
        )
    )


@app.cli.command('ping')
def ping():
    """Ping list of monitored sites and check if they're still alive."""
    from app.main.utils import ping_website

    # Execute pings
    monitors = Monitor.query.all()
    for monitor in monitors:
        ping_website(monitor)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    main()
