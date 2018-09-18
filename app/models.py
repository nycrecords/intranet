from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    JSONB
)
from flask_login import (
    UserMixin
)


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.BigInteger)

    def __repr__(self):
        return '<Roles %r>' % self.id


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(254))
    division = db.Column(db.String)
    title = db.Column(db.String(64))
    phone_number = db.Column(db.String(25))
    profile_picture_path = db.Column(db.String)
    permissions = db.Column(db.BigInteger)

    def __repr__(self):
        return '<Users %r>' % self.id


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Enum('News', 'Event', 'Meeting Notes', name='post_type'))
    title = db.Column(db.String)
    content = db.Column(db.String)
    tags = db.Column(ARRAY(db.String))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    visible = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)

    __mapper_args__ = {'polymorphic_on': type}

    # def __init__(self,
    #              author,
    #              type,
    #              title,
    #              content,
    #              tags):
    #     self.author = author
    #     self.type = type
    #     self.title = title,
    #     self.content = content,
    #     self.tags = tags,
    #     self.date_created = datetime.utcnow()
    #     self.date_modified = None
    #     self.visible = True
    #     self.deleted = False

    def __repr__(self):
        return '<Posts %r>' % self.id


class MeetingNotes(db.Model):
    __tablename__ = 'meeting_notes'
    __mapper_args__ = {'polymorphic_identity': 'meeting_notes'}

    id = db.Column(db.Integer, db.ForeignKey(Posts.id), primary_key=True)
    meeting_date = db.Column(db.DateTime)
    meeting_location = db.Column(db.String)
    meeting_leader = db.Column(db.String)
    note_taker = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    attendees = db.Column(ARRAY(db.Integer))
    next_meeting_date = db.Column(db.DateTime, nullable=True)
    next_meeting_leader = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    next_meeting_note_taker = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    meeting_type = db.Column(db.Enum('Division', 'Strategic', 'Senior Staff', name='meeting_type'))
    meeting_division = db.Column(db.Enum('Admin', 'Executive', 'IT', name='divisions'), nullable=True)

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


class News(db.Model):
    __tablename__ = 'news'
    __mapper_args__ = {'polymorphic_identity': 'news'}

    id = db.Column(db.Integer, db.ForeignKey(Posts.id), primary_key=True)

    def __repr__(self):
        return '<News %r>' % self.id


class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)

    def __repr__(self):
        return '<Events %r>' % self.id