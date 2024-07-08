#!/usr/bin/env python3
"""Doctors module"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from dyno_med import database


class AddressForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=30)])
    city = StringField('City', validators=[DataRequired(), Length(min=2,max=30)])
    town = StringField('Town', validators=[DataRequired(), Length(max=50)])
    street = StringField('Street', validators=[DataRequired(), Length(max=100)])
    House_num = StringField('House Number', validators=[Length(max=15)]),
    email = StringField('Email', validators=[Email(), Length(max=100)])
    telephone_num = StringField('Telephone Number', )
    

