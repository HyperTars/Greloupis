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

class Thumbnail(db.EmbeddedDocument):
    thumbnail_uri = db.StringField(max_length=200, required=True)
    thumbnail_type = db.StringField(max_length=50, required=True)


class VideoURI(db.EmbeddedDocument):
    video_low = db.StringField(max_length=200, required=True)
    video_mid = db.StringField(max_length=200, required=True)
    video_high = db.StringField(max_length=200, required=True)


class Video(db.Document):
    _id = db.StringField()
    user_id = db.StringField(max_length=100, required=True)
    video_title = db.StringField(max_length=50, required=True, unique=True)
    video_tag = db.ListField(db.StringField())
    video_category = db.ListField(db.StringField())
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
    video_thumbnail = db.EmbeddedDocumentField('Thumbnail', required=True)
    video_upload_date = db.DateTimeField(required=True)
    video_uri = db.EmbeddedDocumentField('VideoURI', required=False)

    def to_dict(self):
        video_dict = {}
        video_tag_array = []
        video_category_array = []
        video_thumbnail_dict = {}
        video_uri_dict = {}

        for tag in self.video_tag:
            video_tag_array.append(tag)
        
        for category in self.video_category:
            video_category_array.append(category)
        
        video_thumbnail_dict['video_thumbnail_uri'] = self.video_thumbnail.thumbnail_uri or None
        video_thumbnail_dict['video_thumbnail_type'] = self.video_thumbnail.thumbnail_type or None

        video_uri_dict['video_uri_high'] = self.video_uri.video_high
        video_uri_dict['video_uri_mid'] = self.video_uri.video_mid
        video_uri_dict['video_uri_low'] = self.video_uri.video_low

        video_dict['video_id'] = str(self._id)
        video_dict['video_title'] = self.video_title
        video_dict['video_tag'] = video_tag_array
        video_dict['video_category'] = video_category_array
        video_dict['video_description'] = self.video_description
        video_dict['video_language'] = self.video_language
        video_dict['video_status'] = self.video_status
        video_dict['video_content'] = self.video_content
        video_dict['video_content_status'] = self.video_content_status
        video_dict['video_size'] = self.video_size or None
        video_dict['video_view'] = self.video_view
        video_dict['video_like'] = self.video_like
        video_dict['video_dislike'] = self.video_dislike
        video_dict['video_comment'] = self.video_comment
        video_dict['video_star'] = self.video_star
        video_dict['video_share'] = self.video_share
        video_dict['video_thumbnail'] = video_thumbnail_dict
        video_dict['video_upload_date'] = self.video_upload_date
        video_dict['video_uri'] = video_uri_dict

        return video_dict