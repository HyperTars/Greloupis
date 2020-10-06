from flask import Flask, url_for, request, redirect, render_template
from flask_restx import Api
# from flask_sqlalchemy import SQLAlchemy
from source.models import *

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
