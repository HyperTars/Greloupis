import logging.config

import os
from flask import Flask, Blueprint
from source_rest_plus import settings
from source_rest_plus.api.blog.endpoints.posts import ns as blog_posts_namespace
from source_rest_plus.api.blog.endpoints.categories import ns as blog_categories_namespace
from source_rest_plus.api.online_video_platform.endpoints.user import ns as online_video_platform_user_namespace
from source_rest_plus.api.restplus import api
from source_rest_plus.database import db

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPX_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTX_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTX_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    api.add_namespace(blog_categories_namespace)
    api.add_namespace(online_video_platform_user_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
