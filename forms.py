import os

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectMultipleField, RadioField, SelectField
from wtforms.fields.html5 import EmailField, DateField, IntegerField
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError, NumberRange, EqualTo
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_components import ColorField


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class ShippingForm(FlaskForm):
    firstname = StringField('Name', validators=[InputRequired()])
    lastname = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    city = StringField('city', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


