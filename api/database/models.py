import bleach
from sqlalchemy import Column, String, Integer
from api import db
from marshmallow_jsonapi import fields, Schema
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'

    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # unique name
    name = Column(String(80), nullable=False)

    def __init__(self, name, user_id=None):
        if name is not None:
            name = bleach.clean(name).strip()
            if name == '':
                name = None

        self.name = name
        if user_id is not None:
            self.id = user_id

    def insert(self):
        """
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        updates a new model into a database
        the model must exist in the database
        """
        db.session.commit()

    def delete(self):
        """
        deletes model from database
        the model must exist in the database
        """
        db.session.delete(self)
        db.session.commit()


class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    supplies = db.Column(db.String(250), nullable=False)
    show_supplies = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('reminders', lazy='dynamic'))

    scheduled_reminder = db.relationship('Schedule', backref=db.backref('reminders', lazy='dynamic'))
    location_reminder = db.relationship('Location', backref=db.backref('reminders', lazy='dynamic'))

    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=True)


    def __init__(self, title, supplies, show_supplies, user_id, reminder_id=None):
        if title is not None:
            title = bleach.clean(title).strip()
            if title == '':
                title = None

        self.title = title
        self.supplies = supplies
        self.show_supplies = show_supplies
        self.user_id = user_id
        if reminder_id is not None:
            self.id = reminder_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String(80), nullable=False)
    unix_time = db.Column(db.String(80), nullable=False)
    reminder_id = db.Column(db.Integer, nullable=False)
    days = db.Column(db.String(250), nullable=False)
    repeating = db.Column(db.String(250), nullable=False)
    times = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, schedule_name, unix_time, reminder_id, days, times, repeating, schedule_id=None):
        if schedule_name is not None:
            schedule_name = bleach.clean(schedule_name).strip()
            if schedule_name == '':
                schedule_name = None

        self.schedule_name = schedule_name
        self.unix_time = unix_time
        self.days = days
        self.times = times
        self.repeating = repeating
        self.reminder_id = reminder_id
        self.schedule_id = schedule_id
        if schedule_id is not None:
            self.id = schedule_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    reminder_id = db.Column(db.Integer, nullable=False)
    location_name = Column(String(80), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, location_name, longitude, reminder_id, latitude, address, location_id=None):
        if location_name is not None:
            location_name = bleach.clean(location_name).strip()
            if location_name == '':
                location_name = None

        self.location_name = location_name
        self.reminder_id = reminder_id
        self.longitude = longitude
        self.latitude = latitude
        self.address = address
        self.location_id = location_id
        if location_id is not None:
            self.id = location_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UsersSchema(Schema):
    class Meta:
        type_ = 'users'
        strict = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    creation_date = fields.DateTime()


class SchedulesSchema(Schema):
    class Meta:
        type_ = 'schedules'
        strict = True
    id = fields.Integer(dump_only=True)
    unix_time = fields.String(required=True)
    days = fields.String(required=True)
    times = fields.String(required=True)
    repeating = fields.String(required=True)
    creation_date = fields.DateTime()


class LocationsSchema(Schema):
    class Meta:
        type_ = 'locations'
        strict = True
    id = fields.Integer(dump_only=True)
    location_name = fields.String(required=True)
    longitude = fields.String(required=True)
    latitude = fields.String(required=True)
    address = fields.String(required=True)
    creation_date = fields.DateTime()


class RemindersSchema(ma.Schema, Schema):
    class Meta:
        type_ = 'reminders'
        strict = True
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    supplies = fields.String(required=True)
    show_supplies = fields.Boolean(required=True)
    creation_date = fields.DateTime()
    location_reminder = ma.Nested(LocationsSchema)
    scheduled_reminder = ma.Nested(SchedulesSchema)
