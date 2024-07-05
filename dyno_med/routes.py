#!/usr/bin/python3
from flask import render_template, url_for, flash, redirect, session, request, jsonify
from dyno_med import app

@app.route('/home', methods=['GET'])
def home():
    return jsonify({'message':'Welcome to our Medical application system management'})