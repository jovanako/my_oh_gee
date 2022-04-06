from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FileField, FloatField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    search = StringField()
    venue_type = SelectField(validate_choice=True, coerce=int)
    entry_requirement = SelectField(validate_choice=True, coerce=int)
    lat = FloatField(widget=HiddenInput())
    lng = FloatField(widget=HiddenInput())


class VenueForm(FlaskForm):
    name = StringField()
    latitude = FloatField()
    longitude = FloatField()
    address = StringField()
    entry_requirement = SelectField(validate_choice=True, coerce=int)
    venue_type = SelectField(validate_choice=True, coerce=int)
    web_page = StringField()
    image = FileField()
    submit = SubmitField('Add venue')
