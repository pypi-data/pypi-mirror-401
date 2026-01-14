from flask import Flask
from flask_restful import Api
from app.config import Config
from app.extensions import db, jwt, mail, cache
from app.models import User
from app.controllers.auth_controller import RegisterResource, LoginResource
from app.controllers.cache_example_controller import TimeResource, ClearCacheResource
from app.controllers.task_controller import TriggerEmailTaskResource, TriggerAsyncJobResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    
    api = Api(app)
    
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(TimeResource, '/api/cache/time')
    api.add_resource(ClearCacheResource, '/api/cache/clear')
    api.add_resource(TriggerEmailTaskResource, '/api/tasks/email')
    api.add_resource(TriggerAsyncJobResource, '/api/tasks/async')
    
    with app.app_context():
        db.create_all()
    
    return app
