# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import Flask, request, g, Blueprint, session, url_for, redirect, render_template, render_template_string
from flask_restx import Resource, Api, fields, marshal_with, reqparse, Namespace
import flask_wtf
from source.service.service_user import *
from source.utils.util_serializer import *
from source.settings import *

auth = Namespace('auth', description='Auth APIs')
users = []


@auth.route("/login", methods=["GET", "POST"])
def login():
    pass
    # if request.method == 'POST':
    #     session.pop('user_id', None)
    #     user_name = request.form['username']
    #     user_password = request.form['password']
    #     try:
    #         user = service_user_login(conf=config['default'], user_name=user_name, user_password=user_password)
    #     except ServiceError:
    #         return redirect(url_for('login'))
    #     session['user_id'] = user['user_id']
    #     return redirect(url_for('profile'))
    #
    # return render_template_string('login.html')
