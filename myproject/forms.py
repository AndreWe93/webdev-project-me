from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddRun(FlaskForm):

    kilometers = IntegerField('How many kilometers did you run today?')
    submit = SubmitField('Save')
