#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

import datetime, hashlib, urllib
from flask_mongoengine import MongoEngine
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer

db = MongoEngine()


# VideoOp Model

class VideoOp(db.Document):
    _id = db.StringField(max_length=100, required=True)
    user_id = db.StringField(max_length=100, required=True)
    video_id = db.StringField(max_length=100, required=True)
    process = db.IntField(required=False, default=0)
    comment = db.StringField(max_length=1000, required=True)
    like = db.BooleanField(default=False)
    dislike = db.BooleanField(default=False)
    star = db.BooleanField(default=False)
    history_date = db.DateTimeField(required=False)
    comment_date = db.DateTimeField(required=False)
    like_date = db.DateTimeField(required=False)
    dislike_date = db.DateTimeField(required=False)
    star_date = db.DateTimeField(required=False)
    
    def to_dict(self):
        video_op_dict = {}
        video_op_dict['video_op_id'] = str(self._id)
        video_op_dict['user_id'] = self.user_id
        video_op_dict['video_id'] = self.video_id
        video_op_dict['process'] = self.process
        video_op_dict['comment'] = self.comment
        video_op_dict['like'] = self.like
        video_op_dict['dislike'] = self.dislike
        video_op_dict['star'] = self.star
        video_op_dict['history_date'] = self.history_date
        video_op_dict['comment_date'] = self.comment_date
        video_op_dict['like_date'] = self.like_date
        video_op_dict['dislike_date'] = self.dislike_date
        video_op_dict['star_date'] = self.star_date
        return video_op_dict