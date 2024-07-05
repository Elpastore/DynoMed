
from flask import Flask


app = Flask(__name__)

from dyno_med import routes
