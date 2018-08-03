from flask import current_app
from app.models import Posts, MeetingNotes
from app import db
from sqlalchemy.exc import SQLAlchemyError


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


def create_post(author,
                type,
                title,
                content,
                tags):
    post = Posts(
                 author=author,
                 type=type,
                 title=title,
                 content=content,
                 tags=tags)
    create_object(post)
    return post.id


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
                         division):
    meeting_notes = MeetingNotes(meeting_date=meeting_date,
                                 meeting_location=meeting_location,
                                 meeting_leader=meeting_leader,
                                 meeting_note_taker=meeting_note_taker,
                                 start_time=start_time,
                                 end_time=end_time,
                                 attendees=attendees,
                                 next_meeting_date=next_meeting_date,
                                 next_meeting_leader=next_meeting_leader,
                                 next_meeting_note_taker=next_meeting_note_taker,
                                 meeting_type=meeting_type,
                                 division=division)
    print(meeting_note_taker)
    create_object(meeting_notes)
    return meeting_notes.id
