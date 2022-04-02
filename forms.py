from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FileField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


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
    submit = SubmitField('Search')


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
