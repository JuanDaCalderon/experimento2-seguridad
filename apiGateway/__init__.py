from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['JWT_SECRET_KEY'] = 'experimento2'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app