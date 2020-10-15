#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

from flask_mongoengine import MongoEngine
from source.models.model_base import Thumbnail

db = MongoEngine()


# User Models
class UserDetail(db.EmbeddedDocument):
    first_name = db.StringField(max_length=50, default="")
    last_name = db.StringField(max_length=50, default="")
    phone = db.StringField(max_length=50, default="")
    street1 = db.StringField(max_length=100, default="")
    street2 = db.StringField(max_length=100, default="")
    city = db.StringField(max_length=50, default="")
    state = db.StringField(max_length=50, default="")
    country = db.StringField(max_length=50, default="")
    zip = db.StringField(max_length=20, default="")


class LoginDetail(db.EmbeddedDocument):
    login_ip = db.StringField(max_length=50, default="0.0.0.0", required=True)
    login_time = db.DateTimeField()


class User(db.Document):
    _id = db.StringField()
    user_email = db.StringField(max_length=50, required=True, unique=True)
    user_name = db.StringField(max_length=60, required=True, unique=True)
    user_password = db.StringField(max_length=512, required=True, default="")
    user_detail = db.EmbeddedDocumentField('UserDetail', required=True)
    user_status = db.StringField(max_length=50, required=True, default="public")
    user_thumbnail = db.EmbeddedDocumentField('Thumbnail', required=True)
    user_reg_date = db.DateTimeField()
    user_recent_login = db.ListField(db.EmbeddedDocumentField('LoginDetail'))
    user_following = db.ListField(db.StringField())
    user_follower = db.ListField(db.StringField())

    def to_dict(self):
        user_dict = {}
        user_detail_dict = {}
        user_thumbnail_dict = {}
        user_recent_login_array = []
        user_following_array = []
        user_follower_array = []

        user_detail_dict['user_first_name'] = self.user_detail.first_name or ""
        user_detail_dict['user_last_name'] = self.user_detail.last_name or ""
        user_detail_dict['user_phone'] = self.user_detail.phone or ""
        user_detail_dict['user_street1'] = self.user_detail.street1 or ""
        user_detail_dict['user_street2'] = self.user_detail.street2 or ""
        user_detail_dict['user_city'] = self.user_detail.city or ""
        user_detail_dict['user_state'] = self.user_detail.state or ""
        user_detail_dict['user_country'] = self.user_detail.country or ""
        user_detail_dict['user_zip'] = self.user_detail.zip or ""

        user_thumbnail_dict['user_thumbnail_uri'] = self.user_thumbnail.thumbnail_uri or ""
        user_thumbnail_dict['user_thumbnail_type'] = self.user_thumbnail.thumbnail_type or ""

        for login in self.user_recent_login:
            temp_login_detail = {'login_ip': login.login_ip, 'login_time': login.login_time}
            user_recent_login_array.append(temp_login_detail)

        for following in self.user_following:
            user_following_array.append(following)

        for follower in self.user_follower:
            user_follower_array.append(follower)

        user_dict['user_id'] = str(self._id)
        user_dict['user_email'] = self.user_email
        user_dict['user_name'] = self.user_name
        user_dict['user_detail'] = user_detail_dict
        user_dict['user_status'] = self.user_status
        user_dict['user_thumbnail'] = user_thumbnail_dict
        user_dict['user_reg_date'] = self.user_reg_date
        user_dict['user_recent_login'] = user_recent_login_array
        user_dict['user_following'] = user_following_array
        user_dict['user_follower'] = user_follower_array

        return user_dict
