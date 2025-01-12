from myproject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Run(db.Model):

    # Create a table in the db
    __tablename__ = 'runs'

    id = db.Column(db.Integer, primary_key = True)
    kilometers = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, kilometers, date):
        self.kilometers = kilometers
        self.date = date

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

class Dict(db.Model):

    # Create a table in the db
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key = True)
    word_spanish = db.Column(db.String(64), index=True)
    word_german = db.Column(db.String(64), index=True)
    created_at = db.Column(db.DateTime)
    score = db.Column(db.Integer, default=0)

    def __init__(self, word_spanish, word_german, created_at, score=0):
        self.word_spanish = word_spanish
        self.word_german = word_german
        self.created_at = created_at
        self.score = score
