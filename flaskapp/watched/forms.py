from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddWatchedForm(FlaskForm):
    category = SelectField('Category', choices=[('Movie','Movie'),('Series','Series')])
    name = StringField('Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    stars = SelectField('Stars', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], coerce=int)
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Add')

class EditWatchedForm(FlaskForm):
    category = SelectField('Category', choices=[('Movie','Movie'),('Series','Series')])
    name = StringField('Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    stars = SelectField('Stars', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], coerce=int)
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Edit')