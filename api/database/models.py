import bleach
from sqlalchemy import Column, String, Integer
from api import db


class User(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'

    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # unique name
    name = Column(String(80), unique=True, nullable=False)

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
    print('Connecting to reminder db')
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    supplies = db.Column(db.String(250), nullable=False)
    show_supplies = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('reminders', lazy='dynamic'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=True)
    schedule_reminder = db.relationship('Schedule', backref=db.backref('reminders', lazy='dynamic'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=True)
    location_reminder = db.relationship('Location', backref=db.backref('reminders', lazy='dynamic'))


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

    id = Column(Integer, primary_key=True)
    schedule_name = Column(String(80), unique=True, nullable=False)
    unix_time = db.Column(db.Integer, nullable=False)
    reminder_id = db.Column(db.Integer, nullable=False)
    days = db.Column(db.String(250), nullable=False)
    times = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, schedule_name, unix_time, reminder_id, days, times, schedule_id=None):
        if schedule_name is not None:
            schedule_name = bleach.clean(schedule_name).strip()
            if schedule_name == '':
                schedule_name = None

        self.schedule_name = schedule_name
        self.unix_time = unix_time
        self.days = days
        self.times = times
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

    id = Column(Integer, primary_key=True)
    reminder_id = db.Column(db.Integer, nullable=False)
    location_name = Column(String(80), unique=True, nullable=False)
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
