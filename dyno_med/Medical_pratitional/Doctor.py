#!/usr/bin/env python3
"""Doctors module"""
from flask_Wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from dyno_med import database


class Doctor():
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=30)])
    middle_name = StringField('Middle Name', validators=Length(min=3, max=30))
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=30)])
    passWord = S
    comfirm_pass_word = S
    

