#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

import datetime, hashlib, urllib
from flask_mongoengine import MongoEngine
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer

db = MongoEngine()

# Video Models

class Thumbnail(db.Document):
    thumbnail_uri = db.StringField(max_length=200, required=True)
    thumbnail_type = db.StringField(max_length=50, required=True)


class VideoURI(db.Document):
    video_low = db.StringField(max_length=200, required=True)
    video_mid = db.StringField(max_length=200, required=True)
    video_high = db.StringField(max_length=200, required=True)


class Video(db.Document):
    video_id = db.StringField(max_length=100, required=True, unique=True, primary_key=True)
    user_id = db.StringField(max_length=100, required=True)
    video_title = db.StringField(max_length=50, required=True, unique=True)
    video_tag = db.ListField(db.StringField)
    video_category = db.ListField(db.StringField)
    video_description = db.StringField(max_length=1000, default="")
    video_language = db.StringField(max_length=20)
    video_status = db.StringField(max_length=20, default="public", required=True)
    video_content = db.StringField()
    video_content_status = db.StringField(max_length=20, required=True)
    video_size = db.FloatField(default=0)
    video_view = db.LongField(default=0)
    video_like = db.LongField(default=0)
    video_dislike = db.LongField(default=0)
    video_comment = db.LongField(default=0)
    video_star = db.LongField(default=0)
    video_share = db.LongField(default=0)
    video_thumbnail = db.EmbeddedDocumentField(Thumbnail, required=True)
    video_upload_date = db.DateTimeField(default=datetime.now())
    video_uri = db.EmbeddedDocumentField(VideoURI, required=False)