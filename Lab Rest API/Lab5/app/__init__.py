from flask import Flask
from flask_restful import Api
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    api = Api(app)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger = Swagger(app, config=swagger_config, template={
        "info": {
            "title": "Flask Library API",
            "description": "API бібліотеки з використанням Flask-RESTful та Flasgger",
            "version": "1.0.0"
        }
    })

    from app.resources import BookList, BookResource
    api.add_resource(BookList, '/books')
    api.add_resource(BookResource, '/books/<string:book_id>')

    return app