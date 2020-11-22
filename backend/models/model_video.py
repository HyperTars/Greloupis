#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

from flask_mongoengine import MongoEngine

db = MongoEngine()


# Video Models
class VideoURI(db.EmbeddedDocument):
    video_uri_low = db.StringField(max_length=200, required=True, default="")
    video_uri_mid = db.StringField(max_length=200, required=True, default="")
    video_uri_high = db.StringField(max_length=200, required=True, default="")


class Video(db.Document):
    user_id = db.StringField(max_length=100, required=True, default="")
    """
    video_raw_content description:
    user will get a raw video URI after uploading raw video to cache
    (temp storage space where videos waiting for being transcoded)
    transcoder will start transcoding, but user can create a video now
    """
    video_title = db.StringField(max_length=50, default="")
    video_raw_content = db.StringField(default="")
    video_raw_status = db.StringField(max_length=20, default="pending")
    video_raw_size = db.FloatField(default=0)  # in MB
    video_duration = db.IntField(default=0)  # in second
    video_channel = db.StringField(default="self-made")
    video_tag = db.ListField(db.StringField())
    video_category = db.ListField(db.StringField())
    video_description = db.StringField(max_length=1000, default="")
    video_language = db.StringField(max_length=20)
    video_status = db.StringField(max_length=20, default="public")
    video_view = db.LongField(default=0)
    video_comment = db.LongField(default=0)
    video_like = db.LongField(default=0)
    video_dislike = db.LongField(default=0)
    video_star = db.LongField(default=0)
    video_share = db.LongField(default=0)
    video_thumbnail = db.StringField(max_length=200, default="")
    video_upload_date = db.DateTimeField()
    video_uri = db.EmbeddedDocumentField('VideoURI')

    def to_dict(self):
        video_dict = {}
        video_tag_array = []
        video_category_array = []
        video_uri_dict = {}

        for tag in self.video_tag:
            video_tag_array.append(tag)

        for category in self.video_category:
            video_category_array.append(category)

        video_uri_dict['video_uri_high'] = self.video_uri.video_uri_high or ""
        video_uri_dict['video_uri_mid'] = self.video_uri.video_uri_mid or ""
        video_uri_dict['video_uri_low'] = self.video_uri.video_uri_low or ""

        video_dict['video_id'] = str(self.id)
        video_dict['user_id'] = str(self.user_id)
        video_dict['video_title'] = self.video_title or ""
        video_dict['video_raw_content'] = self.video_raw_content or ""
        video_dict['video_raw_status'] = self.video_raw_status or ""
        video_dict['video_raw_size'] = self.video_raw_size or 0
        video_dict['video_duration'] = self.video_duration or 0
        video_dict['video_channel'] = self.video_channel or ""
        video_dict['video_tag'] = video_tag_array or []
        video_dict['video_category'] = video_category_array or []
        video_dict['video_description'] = self.video_description or ""
        video_dict['video_language'] = self.video_language or ""
        video_dict['video_status'] = self.video_status or ""
        video_dict['video_view'] = self.video_view or 0
        video_dict['video_comment'] = self.video_comment or 0
        video_dict['video_like'] = self.video_like or 0
        video_dict['video_dislike'] = self.video_dislike or 0
        video_dict['video_star'] = self.video_star or 0
        video_dict['video_share'] = self.video_share or 0
        video_dict['video_thumbnail'] = self.video_thumbnail or ""
        video_dict['video_upload_date'] = self.video_upload_date or None
        video_dict['video_uri'] = video_uri_dict or VideoURI()

        return video_dict
