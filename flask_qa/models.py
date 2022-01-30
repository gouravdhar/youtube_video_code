from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    questions_asked = db.relationship(
        'Question', 
        foreign_keys='Question.asked_by_id', 
        backref='asker', 
        lazy=True
    )

    answers_requested = db.relationship(
        'Question',
        foreign_keys='Question.expert_id',
        backref='expert',
        lazy=True
    )

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text)
    username = db.Column(db.Text)

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.Text)
    loc = db.Column(db.Text)
    city = db.Column(db.Text)
    country = db.Column(db.Text)
    org = db.Column(db.Text)
    postal = db.Column(db.Text)
    region = db.Column(db.Text)
    timezone = db.Column(db.Text)
    time = db.Column(db.Text)
    