from app import db
from datetime import datetime
import csv
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    JSONB
)
from flask_login import (
    UserMixin,
    AnonymousUserMixin
)
import csv
from flask import current_app
from app.constants import (
    permission,
    role_name,
)


class Roles(db.Model):
    """
    Define the Roles class with the following columns and relationships:

    Roles - Default sets of permissions.

    id -- Column: Integer, PrimaryKey
    name -- Column: String(64), Unique
    default -- Column: Boolean, Default = False
    permissions -- Column: Integer
    users -- Relationship: 'Users', 'Roles'
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.BigInteger)

    @classmethod
    def populate(cls):
        """
        Insert permissions for each role.
        """
        roles = {
            role_name.ANONYMOUS: (
                permission.NONE
            ),
            role_name.EMPLOYEE: (
                permission.CREATE_POST |
                permission.UPLOAD_DOCUMENT
            ),
            role_name.ADMINISTRATOR: (
                    permission.CREATE_POST |
                    permission.EDIT_POST |
                    permission.DELETE_POST |
                    permission.UPLOAD_DOCUMENT |
                    permission.EDIT_DOCUMENT |
                    permission.DELETE_DOCUMENT
            ),
            role_name.SUPER_USER: (
                    permission.CREATE_POST |
                    permission.EDIT_POST |
                    permission.DELETE_POST |
                    permission.UPLOAD_DOCUMENT |
                    permission.EDIT_DOCUMENT |
                    permission.DELETE_DOCUMENT |
                    permission.CREATE_USER |
                    permission.EDIT_USER |
                    permission.DELETE_USER
            )
        }

        for name, value in roles.items():
            role = Roles.query.filter_by(name=name).first()
            if role is None:
                role = cls(name=name)
            role.permissions = value
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Roles %r>' % self.id


class Users(UserMixin, db.Model):
    """
    Define the Users class with the following columns and relationships:

    id -- Column: Integer, PrimaryKey
    first_name -- Column: String(32)
    middle_name -- Column: String(1)
    last_name -- Column: String(64)
    email -- Column: String(64)
    division -- Column: String()
    title -- Column: String(64)
    phone_number -- Column: String(25)
    room -- Column: String(3)
    role_id -- Column: Integer, foreign key to Roles table.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(254))
    division = db.Column(db.String)
    title = db.Column(db.String(64))
    phone_number = db.Column(db.String(25))
    room = db.Column(db.String(3))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def name(self):
        """
        Property to return a User's full name, including middle initial if applicable.
        :return:
        """
        if self.middle_initial:
            return self.first_name + " " + self.middle_initial + " " + self.last_name
        return self.first_name + " " + self.last_name

    @classmethod
    def populate(cls):
        roles_dict = {}
        roles = Roles.query.all()
        for role in roles:
            roles_dict[role.name] = role.id

        with open(current_app.config['USER_DATA'], 'r') as data:
            dictreader = csv.DictReader(data)

            for row in dictreader:
                user = cls(
                    first_name=row['first_name'],
                    middle_initial=row['middle_initial'],
                    last_name=row['last_name'],
                    email=row['email'],
                    division=row['division'],
                    phone_number=row['phone_number'],
                    title=row['title'],
                    room=row['room'],
                    role_id=roles_dict[row['role']]
                )
                db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<Users %r>' % self.id


class Anonymous(AnonymousUserMixin):

    def __repr__(self):
        return '<Anonymous User>'


class Posts(db.Model):
    """
    Define the Posts class with the following columns and relationships:

    id -- Column: Integer, PrimaryKey
    author -- Column: Integer, foreign key to Users table.
    post_type -- Column: Enum, contains all types of posts that can be made.
    title -- Column: String()
    content -- Column: String()
    tags - Column: Array of strings containing tags that describe a post. Possible tags are from choices.TAGS.
    date_created -- Column: DateTime. Date the post was created, auto generated on object creation.
    date_modified -- Column: DateTime, last timestamp that the post was modified.
    visible -- Column: Boolean, default = True. Determines if the post is visible on the front end. TODO: Is this redundant?
    deleted -- Column: Boolean, default = False. Determines if the post has been deleted.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_type = db.Column(db.Enum('news', 'event_posts', 'meeting_notes', name='post_type'))
    title = db.Column(db.String)
    content = db.Column(db.String)
    tags = db.Column(ARRAY(db.String))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    visible = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)

    __mapper_args__ = {'polymorphic_on': post_type}

    def __init__(self,
                 author,
                 title,
                 content,
                 tags):
        self.author = author
        self.title = title
        self.content = content
        self.tags = tags
        self.date_created = datetime.utcnow()
        self.date_modified = None
        self.visible = True
        self.deleted = False

    @property
    def author_name(self):
        """
        Property to get the full name associated with the author's User id
        :return:
        """
        user = Users.query.filter_by(id=self.author).first()
        return user.name

    def __repr__(self):
        return '<Posts %r>' % self.id


class MeetingNotes(Posts):
    """
    Define the MeetingNotes class with the following columns and relationships:

    id -- Column: Integer, PrimaryKey
    meeting_date -- Column: DatetTime
    meeting_location -- Column: String()
    meeting_leader -- Column: String(), Contains the name of the meeting leader.
    meeting_note_taker -- Column: String(), contains the name of the meeting note taker.
    start_time -- Column: String(), contains a string representation of the meeting start time. Ex) 09:00 AM
    end_time -- Column: String(), contains a string representation of the meeting end time. Ex) 09:30 AM
    attendees -- Column: Array of strings containing the names of Users who attended the meeting.
    next_meeting_date -- Column: DatetTime
    next_meeting_leader -- Column: String(), Contains the name of the next meeting leader.
    next_meeting_note_taker -- Column: String(), contains the name of the  next meeting note taker.
    meeting_type -- Column: Enum, contains all types of meetings notes that can be posted about.
    division -- Column: Enum, contains all divisions in the agency.
    """
    __tablename__ = 'meeting_notes'
    __mapper_args__ = {'polymorphic_identity': 'meeting_notes'}

    id = db.Column(db.Integer, db.ForeignKey(Posts.id), primary_key=True)
    meeting_date = db.Column(db.DateTime)
    meeting_location = db.Column(db.String)
    meeting_leader = db.Column(db.String)
    meeting_note_taker = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    attendees = db.Column(ARRAY(db.String))
    next_meeting_date = db.Column(db.DateTime)
    next_meeting_leader = db.Column(db.String)
    next_meeting_note_taker = db.Column(db.String)
    meeting_type = db.Column(db.Enum('Division', 'Strategic Planning', 'Senior Staff', 'Project',
                                     'Agency', name='meeting_type'))
    division = db.Column(db.Enum('Administration & Human Resources', 'Executive', 'External Affairs', 'Grants Unit',
                                 'Information Technology', 'Legal', 'Municipal Archives', 'Municipal Library',
                                 'Municipal Records Management', 'Operations',  name='divisions'))

    def __init__(self,
                 meeting_date,
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
        super(MeetingNotes, self).__init__(author,
                                           title,
                                           content,
                                           tags)
        self.meeting_date = meeting_date
        self.meeting_location = meeting_location
        self.meeting_leader = meeting_leader
        self.meeting_note_taker = meeting_note_taker
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees
        self.next_meeting_date = next_meeting_date
        self.next_meeting_leader = next_meeting_leader
        self.next_meeting_note_taker = next_meeting_note_taker
        self.meeting_type = meeting_type
        self.division = division

    @property
    def val_for_events(self):
        """
        JSON to store in Events 'new_value' field.
        """
        next_meeting_date = self.next_meeting_date.isoformat() if self.next_meeting_date else None

        return {
            'meeting_date': self.meeting_date.isoformat(),
            'meeting_location': self.meeting_location,
            'meeting_leader': self.meeting_leader,
            'meeting_note_taker': self.meeting_note_taker,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'attendees': self.attendees,
            'next_meeting_date': next_meeting_date,
            'next_meeting_leader': self.next_meeting_leader,
            'next_meeting_note_taker': self.next_meeting_note_taker,
            'meeting_type': self.meeting_type,
            'division': self.division,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'date_modified': None,
            'visible': self.visible,
            'deleted': self.deleted
        }

    def __repr__(self):
        return '<MeetingNotes %r>' % self.id


class EventPosts(db.Model):
    __tablename__ = 'event_posts'
    __mapper_args__ = {'polymorphic_identity': 'event_posts'}

    id = db.Column(db.Integer, db.ForeignKey(Posts.id), primary_key=True)
    event_date = db.Column(db.DateTime)
    event_location = db.Column(db.String)
    leader = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    title = db.Column(db.String)
    sponser = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Events %r>' % self.id


class News(Posts):
    """
    Define the News class with the following columns and relationships:

    id -- Column: Integer, PrimaryKey
    """
    __tablename__ = 'news'
    __mapper_args__ = {'polymorphic_identity': 'news'}

    id = db.Column(db.Integer, db.ForeignKey(Posts.id), primary_key=True)

    def __init__(self,
                 author,
                 title,
                 content,
                 tags):
        super(News, self).__init__(author,
                                   title,
                                   content,
                                   tags)

    @property
    def val_for_events(self):
        """
        JSON to store in Events 'new_value' field.
        """

        return {
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'date_modified': None,
            'visible': self.visible,
            'deleted': self.deleted
        }

    def __repr__(self):
        return '<News %r>' % self.id


class Events(db.Model):
    """
    Define the Events class with the following columns and relationships:

    Events are a log of all important actions that are performed throughout the system.
    Ex) Post created, post deleted, post edited.

    id -- Column: Integer, PrimaryKey
    post_id -- Column: Integer, foreign key to Posts table. Determines which Post the action was performed on.
    user_id -- Column: Integer, foreign key to Users table. Determines which User performed the action.
    type -- Column: String(), the type of action that was performed.
    timestamp -- Column: DateTime, autogenerated on object creation.
    previous_value -- Column: JSON, contains the previous value of the object before changes were made.
    new_value -- Column: JSON, contains the new value of the object after changes were made.
    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)

    def __init__(self,
                 type,
                 post_id=None,
                 user_id=None,
                 previous_value=None,
                 new_value=None):
        self.post_id = post_id
        self.user_id = user_id
        self.type = type
        self.timestamp = datetime.utcnow()
        self.previous_value = previous_value
        self.new_value = new_value

    def __repr__(self):
        return '<Events %r>' % self.id
