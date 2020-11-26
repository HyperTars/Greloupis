#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

from flask_mongoengine import MongoEngine

db = MongoEngine()


# VideoOp Model
class VideoOp(db.Document):
    user_id = db.StringField(max_length=100, required=True)
    video_id = db.StringField(max_length=100, required=True)
    process = db.IntField(required=False, default=0)
    comment = db.StringField(max_length=1000, required=True)
    like = db.BooleanField(default=False)
    dislike = db.BooleanField(default=False)
    star = db.BooleanField(default=False)
    process_date = db.DateTimeField(required=False)
    comment_date = db.DateTimeField(required=False)
    like_date = db.DateTimeField(required=False)
    dislike_date = db.DateTimeField(required=False)
    star_date = db.DateTimeField(required=False)

    # Convert to dict
    def to_dict(self):
        video_op_dict = {'video_op_id': str(self.id), 'user_id': self.user_id,
                         'video_id': self.video_id,
                         'process': self.process, 'comment': self.comment,
                         'like': self.like, 'dislike': self.dislike,
                         'star': self.star, 'process_date': self.process_date,
                         'comment_date': self.comment_date,
                         'like_date': self.like_date,
                         'dislike_date': self.dislike_date,
                         'star_date': self.star_date}

        return video_op_dict
