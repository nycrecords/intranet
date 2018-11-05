import subprocess
import os
from flask import current_app, render_template
from app.models import MeetingNotes, News, EventPosts, Events, Users, Documents
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.constants import file_types


class VirusDetectedException(Exception):
    """
    Raise when scanner detects an infected file.
    """
    def __init__(self, filename):
        super(VirusDetectedException, self).__init__(
            "Infected file '{}' removed.".format(filename))

from app import db
from app.models import MeetingNotes, News, EventPosts, Events, Users


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
    :return:
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