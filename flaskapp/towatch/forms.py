from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired

class AddToWatchForm(FlaskForm):
    category = SelectField('Category', choices=[('Movie','Movie'),('Series','Series')])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')