#!/usr/bin/env python
from datetime import datetime
import os
from flask_migrate import Migrate
from flask.cli import main
import requests

from app import create_app, db
from app.models import Documents, EventPosts, Events, MeetingNotes, Monitor, News, Posts, Roles, Users
from app.main.utils import ping_website

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
    # Execute pings
    monitors = Monitor.query.all()
    for monitor in monitors:
        ping_website(monitor)



@app.cli.command('check_certificate')
def check_certificate():
    monitors = Monitor.query.all()
    
    for monitor in monitors: 
        print(f"Checking URL: {monitor.url}")
        print()  
        
        try: 
            with requests.get(monitor.url, stream=True) as response:
                # Check if the response was successful
                if response.status_code == 200:
                    cert = response.raw.connection.sock.getpeercert()
                    
                    if cert:  # Ensure cert is not None
                        expiration_date_str = cert['notAfter']
                        print(f"Certificate found. Expiration Date: {expiration_date_str}")
                        print()  

                        # Convert expiration date string into a datetime object
                        expiration_date = datetime.strptime(expiration_date_str, "%b %d %H:%M:%S %Y %Z")
                        monitor.expiration_date = expiration_date.date()  
                        print(f"Parsed expiration date: {expiration_date}")
                        print()  

                        # Determine if the certificate is expired
                        today = datetime.now()
                        is_expired = expiration_date <= today
                        monitor.is_expired = is_expired
                        print(f"Set is_expired to: {is_expired} for {monitor.url}")
                    else:
                        print("No certificate found.")
                        monitor.expiration_date = None  
                        print()  
                else:
                    print(f"Failed to retrieve {monitor.url}. Status code: {response.status_code}")
                    monitor.expiration_date = None 
                    print()  
        except Exception as e:
            print(f"Error while checking {monitor.url}: {e}")
            monitor.is_expired = False
            monitor.expiration_date = None  
            print("Set is_expired to False and expiration_date to None due to exception.")
            print() 
        
        # Commit changes to the database
        db.session.commit()
        print(f"Committed: is_expired={monitor.is_expired}, expiration_date={monitor.expiration_date} for {monitor.url}")
        print()