#!/usr/bin/env python
from getpass import getpass

import os
from flask_migrate import Migrate, upgrade
# from flask_script import Manager, Shell
# from flask_script.commands import InvalidCommand
from flask.cli import main

from app import create_app, db
from app.constants.choices import DIVISIONS
from app.models import Documents, EventPosts, Events, MeetingNotes, News, Posts, Roles, Users

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(app)
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
        Events=Events,
        Documents=Documents
    )


# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)


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


# @app.cli.command()
# @click.option("-f", "--fname", dest="first_name", default=None)
# @click.option("-m", "--minitial", dest='middle_initial', default='')
# @click.option("-l", "--lname", dest="last_name", default=None)
# @click.option("-e", "--email", dest="email", default=None)
# @click.option("-d", "--division", dest="division", default=None)
# @click.option("-p", "--phone", dest="phone_number", default=None)
# @click.option("-t", "--title", dest="title", default=None)
# @click.option("-r", "--room", dest="room", default=None)
# @click.option("--role", dest="role", default=None)
# def create_local_user(
#         first_name=None,
#         middle_initial='',
#         last_name=None,
#         email=None,
#         division=None,
#         phone_number=None,
#         title=None,
#         room=None,
#         role=None
# ):
#     """Create a local auth user.
#
#         Valid options for Role are:
#             Anonymous User
#             Employee
#             Administrator
#             Super User
#
#         Valid options for Division are:
#             Administration & Human Resources
#             Executive
#             External Affairs
#             Grants Unit
#             Information Technology
#             Legal
#             Municipal Archives
#             Municipal Library
#             Municipal Records Management
#             Operations
#     """
#     divisions = [d[0] for d in DIVISIONS]
#     roles = [r.name for r in Roles.query.all()]
#     roles.insert(0, '')
#
#     if first_name is None:
#         first_name = input('Enter First Name: ')
#         if first_name == '':
#             raise InvalidCommand("First name is required")
#
#     if last_name is None:
#         last_name = input('Enter Last Name: ')
#         if last_name == '':
#             raise InvalidCommand("Last name is required")
#
#     if email is None:
#         email = input('Enter Email: ')
#         if email == '':
#             raise InvalidCommand("Email is required")
#
#     if division is None:
#         division = input('Enter Division ({}): '.format(', '.join(divisions[1:])))
#         if division == '':
#             raise InvalidCommand("Division is required. Options are: \n{}".format('\n\t'.join(divisions[1:])))
#
#     if phone_number is None:
#         phone_number = input('Enter Phone Number: ')
#         if phone_number == '':
#             raise InvalidCommand("Phone is required")
#
#     if title is None:
#         title = input('Enter Title: ')
#         if title == '':
#             raise InvalidCommand("Title is required")
#
#     if room is None:
#         room = input('Enter Room: ')
#         if room == '':
#             raise InvalidCommand("Room is required")
#
#     if role is None:
#         role = input('Enter Role ({}}: '.format(', '.join(roles[1:])))
#         if role == '':
#             raise InvalidCommand("Role is required. Options are: \n{}".format('\n\t'.join(roles[1:])))
#
#     role_id = Roles.query.filter_by(name=role).first().id
#
#     password = getpass("Enter your desired password: ")
#     confirm_password = getpass("Re-enter your password: ")
#
#     if password != confirm_password:
#         return print("Passwords are not the same. Please try again.")
#
#     user = Users(
#         first_name=first_name,
#         middle_initial=middle_initial,
#         last_name=last_name,
#         email=email,
#         division=division,
#         phone_number=phone_number,
#         title=title,
#         room=room,
#         role_id=role_id,
#         password=password
#     )
#
#     db.session.add(user)
#     db.session.commit()
#
#     print(user)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    main()
