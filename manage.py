#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Roles, Users, Posts, MeetingNotes, News, EventPosts, Events
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app, 
        db=db, 
        Roles=Roles, 
        Users=Users, 
        Posts=Posts,
        MeetingNotes=MeetingNotes,
        News=News,
        EventPosts=EventPosts,
        Events=Events
    )

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
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


@manager.command
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


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
