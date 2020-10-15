#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

from flask_mongoengine import MongoEngine

db = MongoEngine()


# User Models
class UserDetail(db.EmbeddedDocument):
    user_first_name = db.StringField(max_length=50, default="")
    user_last_name = db.StringField(max_length=50, default="")
    user_phone = db.StringField(max_length=50, default="")
    user_street1 = db.StringField(max_length=100, default="")
    user_street2 = db.StringField(max_length=100, default="")
    user_city = db.StringField(max_length=50, default="")
    user_state = db.StringField(max_length=50, default="")
    user_country = db.StringField(max_length=50, default="")
    user_zip = db.StringField(max_length=20, default="")


class UserLogin(db.EmbeddedDocument):
    user_login_ip = db.StringField(max_length=50, default="0.0.0.0", required=True)
    user_login_time = db.DateTimeField()


class User(db.Document):
    _id = db.StringField()
    user_email = db.StringField(max_length=50, required=True, unique=True)
    user_name = db.StringField(max_length=60, required=True, unique=True)
    user_password = db.StringField(max_length=512, required=True, default="")
    user_detail = db.EmbeddedDocumentField('UserDetail', required=True)
    user_status = db.StringField(max_length=50, required=True, default="public")
    user_thumbnail = db.StringField(max_length=200, required=True, default="")
    user_reg_date = db.DateTimeField()
    user_login = db.ListField(db.EmbeddedDocumentField('UserLogin'))
    user_following = db.ListField(db.StringField())
    user_follower = db.ListField(db.StringField())

    def to_dict(self):
        user_dict = {}
        user_detail_dict = {}
        user_login_array = []
        user_following_array = []
        user_follower_array = []

        user_detail_dict['user_first_name'] = self.user_detail.user_first_name or ""
        user_detail_dict['user_last_name'] = self.user_detail.user_last_name or ""
        user_detail_dict['user_phone'] = self.user_detail.user_phone or ""
        user_detail_dict['user_street1'] = self.user_detail.user_street1 or ""
        user_detail_dict['user_street2'] = self.user_detail.user_street2 or ""
        user_detail_dict['user_city'] = self.user_detail.user_city or ""
        user_detail_dict['user_state'] = self.user_detail.user_state or ""
        user_detail_dict['user_country'] = self.user_detail.user_country or ""
        user_detail_dict['user_zip'] = self.user_detail.user_zip or ""

        for login in self.user_login:
            temp_login = {'user_login_ip': login.user_login_ip, 'login_time': login.user_login_time}
            user_login_array.append(temp_login)

        for following in self.user_following:
            user_following_array.append(following)

        for follower in self.user_follower:
            user_follower_array.append(follower)

        user_dict['user_id'] = str(self._id)
        user_dict['user_email'] = self.user_email
        user_dict['user_name'] = self.user_name
        user_dict['user_detail'] = user_detail_dict
        user_dict['user_status'] = self.user_status or ""
        user_dict['user_thumbnail'] = self.user_thumbnail or ""
        user_dict['user_reg_date'] = self.user_reg_date or None
        user_dict['user_login'] = user_login_array
        user_dict['user_following'] = user_following_array
        user_dict['user_follower'] = user_follower_array

        return user_dict
