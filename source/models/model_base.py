#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mongoengine-0.20.0

from flask_mongoengine import MongoEngine

db = MongoEngine()


class Thumbnail(db.EmbeddedDocument):
    thumbnail_uri = db.StringField(max_length=200, required=True, default="")
    thumbnail_type = db.StringField(max_length=50, required=True, default="default")