import subprocess
import os
import traceback
import requests
from flask import current_app, render_template
from app.models import Posts, MeetingNotes, Monitor, News, EventPosts, Events, Users, Documents
from app import db, mail
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.constants import file_types
from flask_mail import Message


class VirusDetectedException(Exception):
    """
    Raise when scanner detects an infected file.
    """
    def __init__(self, filename):
        super(VirusDetectedException, self).__init__(
            "Infected file '{}' removed.".format(filename))


def create_object(obj):
    """
    Add a database record and its elasticsearch counterpart.

    If 'obj' is a Requests object, nothing will be added to
    the es index since a UserRequests record is created after
    its associated request and the es doc requires a
    requester id. 'es_create' is called explicitly for a
    Requests object in app.request.utils.

    :param obj: object (instance of sqlalchemy model) to create

    :return: string representation of created object
        or None if creation failed
    """
    try:
        db.session.add(obj)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to CREATE {}".format(obj))
        return None


def create_meeting_notes(meeting_date,
                         meeting_location,
                         meeting_leader,
                         meeting_note_taker,
                         start_time,
                         end_time,
                         attendees,
                         next_meeting_date,
                         next_meeting_leader,
                         next_meeting_note_taker,
                         meeting_type,
                         division,
                         author,
                         title,
                         content,
                         tags):
    """
    Util function for creating a MeetingNotes object. Function will take parameters passed in from the form
    and create a meeting notes along with the event object.
    """
    meeting_notes = MeetingNotes(meeting_date=meeting_date,
                                 meeting_location=meeting_location,
                                 meeting_leader=meeting_leader,
                                 meeting_note_taker=meeting_note_taker,
                                 start_time=start_time,
                                 end_time=end_time,
                                 attendees=attendees,
                                 next_meeting_date=next_meeting_date or None,
                                 next_meeting_leader=next_meeting_leader or None,
                                 next_meeting_note_taker=next_meeting_note_taker or None,
                                 meeting_type=meeting_type,
                                 division=division,
                                 author=author,
                                 title=title,
                                 content=content,
                                 tags=tags)
    create_object(meeting_notes)

    # Create meeting_notes_created Event
    event = Events(post_id=meeting_notes.id,
                   user_id=author,
                   type="meeting_notes_created",
                   previous_value={},
                   new_value=meeting_notes.val_for_events)
    create_object(event)

    return meeting_notes.id


def create_news(author,
                title,
                content,
                tags):
    """
    Util function for creating a News object. Function will take parameters passed in from the form
    and create a News along with the event object.
    """
    news = News(author=author,
                title=title,
                content=content,
                tags=tags)
    create_object(news)

    # Create news_created Event
    event = Events(post_id=news.id,
                   user_id=author,
                   type="news_created",
                   previous_value={},
                   new_value=news.val_for_events)
    create_object(event)

    return news.id


def create_event_post(event_date,
                      event_location,
                      event_leader,
                      start_time,
                      end_time,
                      sponsor,
                      author,
                      title,
                      content,
                      tags):
    """
    Util function for creating a EventPost object. Function will take parameters passed in from the form
    and create a event post along with the event object.
    """
    event_post = EventPosts(event_date=event_date,
                            event_location=event_location,
                            event_leader=event_leader,
                            start_time=start_time,
                            end_time=end_time,
                            sponsor=sponsor,
                            author=author,
                            title=title,
                            content=content,
                            tags=tags)
    create_object(event_post)

    # Create event_post_created Event
    event = Events(post_id=event_post.id,
                   user_id=author,
                   type="event_post_created",
                   previous_value={},
                   new_value=event_post.val_for_events)
    create_object(event)

    return event_post.id


def get_users_by_division(division):
    """
    Query the database for a list of users based on the division passed in
    :param division: Division to filter by
    :return: A list of users sorted by last name and filtered by division
    """

    return Users.query.filter_by(division=division).order_by(Users.last_name).all()


def get_rooms_by_division(division):
    """
    Query the database for a list of rooms based on the division passed in
    :param division: Division to filter by
    :return: A list of rooms that a division uses
    """

    rooms = [u[0] for u in
             Users.query.with_entities(Users.room).filter_by(division=division).order_by(Users.room).all()]
    rooms = filter(None, rooms)
    return list(set(rooms))


def render_email(data, template):
    """
    Render the given email template with the given data
    :param data: Data to populate in the email template
    :param template: Path to the email template
    :return: HTML String
    """
    today = str(datetime.now().today().date())
    return render_template(template, today=today, form=data)


def create_document(uploader_id,
                    file_title,
                    file_name,
                    document_type,
                    file_type,
                    file_path,
                    division):
    """
    Util function to create a Document object and 'document_uploaded' Event
    :param uploader_id: Id of the user who uploaded the file
    :param file_title: Human readable version of the file name
    :param file_name: Actual file name
    :param document_type: Category of document
    :param file_type: Extension of the file
    :param file_path: Full path of where the file is saved on the server
    :param division: Division that the file relates to
    """
    # Create Document object
    document = Documents(uploader_id=uploader_id,
                         file_title=file_title,
                         file_name=file_name,
                         document_type=document_type,
                         file_type=file_type,
                         file_path=file_path,
                         division=division)
    create_object(document)

    # Create document_uploaded Event
    event = Events(document_id=document.id,
                   user_id=uploader_id,
                   type="document_uploaded",
                   previous_value={},
                   new_value=document.val_for_events)
    create_object(event)


def allowed_file(filename):
    """
    Check if the file type is allowed (uses the file extension).
    TODO: Need to use a better method for this.
    :param filename: Name of the file
    :return: Boolean (True if file type is allowed).
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_types.ALLOWED_EXTENSIONS


def scan_file(filepath):
    """
    Scans a file for viruses using McAfee Virus Scan. If an infected
    file is detected, removes the file and raises VirusDetectedException.
    :param filepath: path of file to scan
    """
    if current_app.config['VIRUS_SCAN_ENABLED']:
        options = [
            '--analyze',  # Use heuristic analysis to find possible new viruses
            '--atime-preserve',  # Preserve the file's last-accessed time and date
            '--delete'  # Automatically delete the infected file
        ]
        cmd = ['uvscan'] + options + [filepath]
        subprocess.call(cmd)  # TODO: redirect output to logfile
        # if the file was removed, it was infected
        if not os.path.exists(filepath):
            raise VirusDetectedException(os.path.basename(filepath))


def process_documents_search(document_type_plain_text,
                             document_type,
                             sort_by,
                             search_term,
                             documents_start,
                             documents_end):
    """
    Util function to process the documents search based on search term and sort by value
    :param document_type_plain_text: Plain text version of the document type
    :param document_type: Category of the document
    :param sort_by: String containing the currently selected sort by value
    :param search_term: String containing the search term to be used when querying
    :param documents_start: Start range of rows to be displayed on the frontend
    :param documents_end: End range of rows to be displayed on the frontend
    :return: JSON containing document table templates and ranges to be displayed
    """
    search_term = search_term.lower()
    # Order the results based on the sort by value
    if sort_by == 'all' or sort_by == 'date_newest':
        documents = Documents.query.filter(Documents.document_type == document_type_plain_text, Documents.file_title.ilike('%{}%'.format(search_term), Documents.deleted == False)).order_by(Documents.last_modified.desc()).slice(documents_start, documents_end).all()
    elif sort_by == 'name_a_z':
        documents = Documents.query.filter(Documents.document_type == document_type_plain_text, Documents.file_title.ilike('%{}%'.format(search_term), Documents.deleted == False)).order_by(Documents.file_title.asc()).slice(documents_start, documents_end).all()
    elif sort_by == 'name_z_a':
        documents = Documents.query.filter(Documents.document_type == document_type_plain_text, Documents.file_title.ilike('%{}%'.format(search_term), Documents.deleted == False)).order_by(Documents.file_title.desc()).slice(documents_start, documents_end).all()
    elif sort_by == 'date_oldest':
        documents = Documents.query.filter(Documents.document_type == document_type_plain_text, Documents.file_title.ilike('%{}%'.format(search_term), Documents.deleted == False)).order_by(Documents.last_modified.asc()).slice(documents_start, documents_end).all()
    
    # Get the total number of documents of the specified document type
    documents_max = Documents.query.filter(Documents.document_type == document_type_plain_text, Documents.file_title.ilike('%{}%'.format(search_term)), Documents.deleted == False).count()
    # Create the template for the document type table
    documents_rows = render_template('documents_table.html', document_type=document_type, documents=documents)

    data = {
        'documents': documents_rows,
        'documents_max': documents_max,
        'documents_start': documents_start + 1,
        'documents_end': documents_end,
        'document_type': document_type
    }

    return data


def process_posts_search(post_type,
                         sort_by,
                         search_term,
                         tags,
                         posts_start,
                         posts_end,
                         meeting_type):
    """
    Util function to process the posts search based on search filters passed in
    :param post_type: Array of strings containing the post types to be filtered on
    :param sort_by: A string containing the sort order of the search results
    :param search_term: String containing the search term to be used when querying
    :param tags: An array of strings containing the tags to be filtered on
    :param posts_start: Start range of rows to be displayed on the frontend
    :param posts_end: End range of rows to be displayed on the frontend
    :param meeting_type: An array of strings containing the meeting types to be filtered on
    :return: JSON containing post rows tempalte and range to be displayed
    """
    search_term = search_term.lower()

    # Include MeetingNotes.meeting_type.in_(meeting_type) filter if strictly searching MeetingNotes
    if meeting_type:
        if sort_by == 'date_newest':
            posts = MeetingNotes.query.filter(Posts.post_type.in_(post_type), MeetingNotes.meeting_type.in_(meeting_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.desc()).all()
        elif sort_by == 'date_oldest':
            posts = MeetingNotes.query.filter(Posts.post_type.in_(post_type), MeetingNotes.meeting_type.in_(meeting_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.asc()).all()
        elif sort_by == 'author_a_z':
            posts = MeetingNotes.query.filter(Posts.post_type.in_(post_type), MeetingNotes.meeting_type.in_(meeting_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.desc()).all()
            posts.sort(key=lambda x: x.author_name, reverse=False)
        elif sort_by == 'author_z_a':
            posts = MeetingNotes.query.filter(Posts.post_type.in_(post_type), MeetingNotes.meeting_type.in_(meeting_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.desc()).all()
            posts.sort(key=lambda x: x.author_name, reverse=True)
    else:
        if sort_by == 'date_newest':
            posts = Posts.query.filter(Posts.post_type.in_(post_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.desc()).all()
        elif sort_by == 'date_oldest':
            posts = Posts.query.filter(Posts.post_type.in_(post_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.asc()).all()
        elif sort_by == 'author_a_z':
            posts = Posts.query.filter(Posts.post_type.in_(post_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.desc()).all()
            posts.sort(key=lambda x: x.author_name, reverse=False)
        elif sort_by == 'author_z_a':
            posts = Posts.query.filter(Posts.post_type.in_(post_type), ((Posts.title.ilike('%{}%'.format(search_term))) | (Posts.content.ilike('%{}%'.format(search_term)))), Posts.deleted == False).order_by(Posts.date_created.desc()).all()
            posts.sort(key=lambda x: x.author_name, reverse=True)
    # For author_a_z and author_z_a, sort by author name using lambda function since you can't use order_by on a property
    # Also grab all the query results and then slice because we may need to filter on tags which will affect the max calculation

    # Filter Posts based on tags
    if tags:
        posts_filtered_by_tags = []
        for post in posts:
            # If a post's tags intersects with any of the tags to be filtered on, append to the list of search results
            intersect = set(post.tags).intersection(set(tags))
            if intersect:
                posts_filtered_by_tags.append(post)
        # Get the max of the filtered list of Posts and start/end ranges
        posts_max = len(posts_filtered_by_tags)
        posts = posts_filtered_by_tags[posts_start:posts_end]
    # Otherwise get the max of the query and slice according to the start and end ranges
    else:
        posts_max = len(posts)
        posts = posts[posts_start:posts_end]

    # Create the template for the post rows
    posts_rows = render_template('news_and_updates_rows.html', posts=posts)

    data = {
        'posts': posts_rows,
        'posts_max': posts_max,
        'posts_start': posts_start + 1,
        'posts_end': posts_end,
        'post_type': post_type
    }

    return data


def update_object(data, obj_type, obj_id):
    """
    Update a database record.

    :param data: a dictionary of attribute-value pairs
    :param obj_type: sqlalchemy model
    :param obj_id: id of record

    :return: was the record updated successfully?
    """
    obj = get_object(obj_type, obj_id)

    if obj:
        for attr, value in data.items():
            if isinstance(value, dict):
                # update json values
                attr_json = getattr(obj, attr) or {}
                for key, val in value.items():
                    attr_json[key] = val
                setattr(obj, attr, attr_json)
            else:
                setattr(obj, attr, value)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception("Failed to UPDATE {}".format(obj))
    return False


def get_object(obj_type, obj_id):
    """
    Safely retrieve a database record by its id
    and its sqlalchemy object type.
    """
    if not obj_id:
        return None
    try:
        return obj_type.query.get(obj_id)
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception('Error searching "{}" table for id {}'.format(
            obj_type.__tablename__, obj_id))
        return None


def send_website_down_email(id,
                            name,
                            url,
                            status_code,
                            current_timestamp,
                            last_success_timestamp,
                            response_header,
                            use_ssl,
                            subject):
    """
    Emails configured recipients about a website outage that was detected.

    :param id: ID of the site that went down.
    :param name: Name of the site that went down.
    :param url: URL of the site that went down.
    :param status_code: HTML status code of the site that went down.
    :param current_timestamp: Timestamp of when the site went down.
    :param last_success_timestamp: Timestamp of the last successful ping.
    :param response_header: Information possibly about why the site went down.
    :param use_ssl: Whether this website uses SSL on ping.
    :param subject: Subject of the email being sent.
    """
    email = render_template('email/monitor_email_alert.html',
                            id=id,
                            name=name,
                            url=url,
                            status_code=status_code,
                            current_timestamp=current_timestamp,
                            last_success_timestamp=last_success_timestamp,
                            response_header=response_header,
                            use_ssl=use_ssl)
    sender = current_app.config["MONITOR_EMAIL_SENDER"]
    recipients = current_app.config["MONITOR_EMAIL_RECIPIENTS"]

    msg = Message(
        subject,
        sender=sender,
        recipients=recipients
    )
    msg.html = email
    mail.send(msg)


def ping_website(monitor_info):
    """
    Pings a website, sends emails if error.

    :param monitor_info: the database entry of the monitor we want to ping.

    :return: tuple( successful ping?, timestamp, reason )
    """
    time_now = datetime.utcnow()

    try:
        response = requests.get(monitor_info.url, allow_redirects=True,
                                                  verify=monitor_info.use_ssl,
                                                  timeout=int(current_app.config['REQUEST_TIMEOUT_DURATION']))

        if response.status_code == 200:
            update_object({
                'current_timestamp': time_now,
                'last_success_timestamp': time_now,
                'status_code': response.status_code,
                'response_header': str(response.headers)
            }, Monitor, monitor_info.id)

            return True, time_now, {'status': response.status_code,
                                    'error': None}

        else:
            print("CRASH: ", monitor_info.url, time_now, "CODE: ", response.status_code)
            print(response.headers)

            # Email on initial failure detection
            if monitor_info.status_code == '200':
                send_website_down_email(monitor_info.id,
                                        monitor_info.name,
                                        monitor_info.url,
                                        response.status_code,
                                        time_now,
                                        monitor_info.last_success_timestamp,
                                        response.headers,
                                        monitor_info.use_ssl,
                                        'WEBSITE DOWN: {} - BAD RESPONSE CODE {}'.format(monitor_info.url,
                                                                                         response.status_code))

            update_object({
                'status_code': response.status_code,
                'current_timestamp': time_now,
                'response_header': str(response.headers)
            }, Monitor, monitor_info.id)

            return False, monitor_info.last_success_timestamp, {'status': response.status_code,
                                                                'error': response.headers}

    # Unable to connect to server - update database and return failed.
    except ConnectionError as e:
        error_stack = traceback.format_exc()

        print("CRASH: ", monitor_info.url, time_now)
        print(error_stack)

        # Email on initial failure detection
        if monitor_info.status_code == '200':
            send_website_down_email(monitor_info.id,
                                    monitor_info.name,
                                    monitor_info.url,
                                    'DOWN',
                                    time_now,
                                    monitor_info.last_success_timestamp,
                                    error_stack,
                                    monitor_info.use_ssl,
                                    'WEBSITE DOWN: {} - NO CONNECTION {}'.format(monitor_info.url, type(e).__name__))

        update_object({
            'status_code': 'DOWN',
            'current_timestamp': time_now,
            'response_header': str(e)
        }, Monitor, monitor_info.id)

        return False, monitor_info.last_success_timestamp, {'status': 'DOWN',
                                                            'error': str(e)}

    # Internal tool error
    except Exception as e:
        error_stack = traceback.format_exc()

        print("CRASH: ", monitor_info.url, time_now)
        print(error_stack)

        # Email on initial failure detection
        if monitor_info.status_code == '200':
            send_website_down_email(monitor_info.id,
                                    monitor_info.name,
                                    monitor_info.url,
                                    'ERROR',
                                    time_now,
                                    monitor_info.last_success_timestamp,
                                    error_stack,
                                    monitor_info.use_ssl,
                                    'WEBSITE DOWN: {} - EXCEPTION CAUGHT {}'.format(monitor_info.url, type(e).__name__))

        update_object({
            'status_code': 'ERROR',
            'current_timestamp': time_now,
            'response_header': str(e)
        }, Monitor, monitor_info.id)

        return False, monitor_info.last_success_timestamp, {'status': 'ERROR',
                                                            'error': str(e)}
