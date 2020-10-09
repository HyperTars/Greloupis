#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

import datetime, hashlib, urllib
from flask_mongoengine import MongoEngine
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer

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


class Thumbnail(db.EmbeddedDocument):
    thumbnail_uri = db.StringField(max_length=200, required=True, default="")
    thumbnail_type = db.StringField(max_length=50, required=True, default="default")


class LoginDetail(db.EmbeddedDocument):
    login_ip = db.StringField(max_length=50, required=True)
    login_time = db.DateTimeField()


class User(db.Document):
    _id = db.StringField()
    user_email = db.StringField(max_length=50, required=True, unique=True)
    user_name = db.StringField(max_length=60, required=True, unique=True)
    user_password = db.StringField(max_length=200, required=True)
    user_detail = db.EmbeddedDocumentField('UserDetail', required=True)
    user_status = db.StringField(max_length=50, required=True)
    user_thumbnail = db.EmbeddedDocumentField('Thumbnail', required=True)
    user_reg_date = db.DateTimeField(required=True)
    user_recent_login = db.ListField(db.EmbeddedDocumentField('LoginDetail'))
    user_following = db.ListField(db.StringField())
    user_follower = db.ListField(db.StringField())

    meta = {'collection': 'user'}

    # to_json() is also supported
    
    def to_dict(self):
        user_dict = {}
        user_detail_dict = {}
        user_thumbnail_dict = {}
        user_recent_login_array = []
        user_following_array = []
        user_follower_array = []

        user_detail_dict['user_first_name'] = self.user_detail.first_name or None
        user_detail_dict['user_last_name'] = self.user_detail.last_name or None
        user_detail_dict['user_phone'] = self.user_detail.phone or None
        user_detail_dict['user_street1'] = self.user_detail.street1 or None
        user_detail_dict['user_street2'] = self.user_detail.street2 or None
        user_detail_dict['user_city'] = self.user_detail.city or None
        user_detail_dict['user_state'] = self.user_detail.state or None
        user_detail_dict['user_country'] = self.user_detail.country or None
        user_detail_dict['user_zip'] = self.user_detail.zip or None

        user_thumbnail_dict['user_thumbnail_uri'] = self.user_thumbnail.thumbnail_uri or None
        user_thumbnail_dict['user_thumbnail_type'] = self.user_thumbnail.thumbnail_type or None

        for login in self.user_recent_login:
            temp_login_detail = {}
            temp_login_detail['login_ip'] = login.login_ip
            temp_login_detail['login_time'] = login.login_time
            user_recent_login_array.append(temp_login_detail)
        
        for following in self.user_following:
            user_following_array.append(following)

        for follower in self.user_follower:
            user_follower_array.append(follower)

        user_dict['user_id'] = str(self._id)
        user_dict['user_email'] = self.user_email
        user_dict['user_name'] = self.user_name
        user_dict['user_password'] = self.user_password 
        user_dict['user_detail'] = user_detail_dict
        user_dict['user_status'] = self.user_status
        user_dict['user_thumbnail'] = user_thumbnail_dict
        user_dict['user_reg_date'] = self.user_reg_date
        user_dict['user_recent_login'] = user_recent_login_array
        user_dict['user_following'] = user_following_array
        user_dict['user_follower'] = user_follower_array
        return user_dict

    @property
    def password(self):
        raise AttributeError('Password is not allowed to read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self, expiration=3600):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'confirm':self.username})

    def confirm_email(self, token, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.username:
            return False
        self.is_email_confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'reset': self.username})

    @staticmethod
    def reset_password(token, new_password):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except:
            return False

        try:
            user = User.objects.get(username=data.get('reset'))
        except Exception:
            return False

        user.password = new_password
        user.save()
        return True

    def get_id(self):
        try:
            # return unicode(self.username)
            return self.username

        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def __unicode__(self):
        return self.username
