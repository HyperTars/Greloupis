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

class AddressDetail(db.EmbeddedDocument):
    street1 = db.StringField(max_length=100)
    street2 = db.StringField(max_length=100)
    city = db.StringField(max_length=50)
    state = db.StringField(max_length=50)
    country = db.StringField(max_length=50)
    zip = db.StringField(max_length=20)
    

class UserDetail(db.EmbeddedDocument):
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    phone = db.StringField(max_length=50, required=True, unique=True)
    address = db.EmbeddedDocumentField('AddressDetail')


class Thumbnail(db.EmbeddedDocument):
    thumbnail_uri = db.StringField(max_length=200, required=True)
    thumbnail_type = db.StringField(max_length=50, required=True)


class LoginDetail(db.EmbeddedDocument):
    login_ip = db.StringField(max_length=50, required=True)
    login_time = db.DateTimeField()


class User(db.Document):
    _id = db.StringField()
    user_email = db.StringField(max_length=50, required=True, unique=True)
    user_name = db.StringField(max_length=60, required=True, unique=True)
    user_password = db.StringField(max_length=200, required=True)
    user_detail = db.EmbeddedDocumentField(UserDetail, required=True)
    user_status = db.StringField(max_length=50, required=True)
    user_thumbnail = db.EmbeddedDocumentField('Thumbnail', required=True)
    user_reg_date = db.DateTimeField(required=True)
    user_recent_login = db.ListField(db.EmbeddedDocumentField('LoginDetail'))
    user_following = db.ListField(db.StringField)
    user_follower = db.ListField(db.StringField)
    
    meta = {'collection': 'user'}

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
