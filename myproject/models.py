from myproject import db

class Run(db.Model):

    # Create a table in the db
    __tablename__ = 'runs'

    id = db.Column(db.Integer, primary_key = True)
    kilometers = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, kilometers, date):
        self.kilometers = kilometers
        self.date = date
