from flask import Flask
from .api.v1.views.users_view import version1 as v1
from .api.v1.views.question_views import version1 as qu
from .api.v1.views.answer_views import version1 as an
from instance.config import app_config


def create_app(config_name="development"):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
 
    app.register_blueprint(v1)
    app.register_blueprint(qu)
    app.register_blueprint(an)


    return app