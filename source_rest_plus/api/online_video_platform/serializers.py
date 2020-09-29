from flask_restx import fields
from source_rest_plus.api.restplus import api

user = api.model('User post', {
    'user_name': fields.String(required=True, description='userName'),
    'first_name': fields.String(required=True, description='firstName'),
    'last_name': fields.String(required=True, description='lastName'),
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password'),
    'phone': fields.String(required=True, description='phone'),
    'user_status': fields.String(required=True, description='userStatus'),
})

user_login = api.model('User login', {
    'user_name': fields.String(required=True, description='userName'),
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password'),
})
