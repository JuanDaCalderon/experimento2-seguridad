from flask_jwt_extended import JWTManager
from apiGateway import create_app
from flask_cors import CORS
from apiGateway import create_app
from flask_restful import Api
from .vistas import VistaLogin, VistaDarAcceso

app = create_app()
app_context = app.app_context()
app_context.push()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaLogin, '/login')
api.add_resource(VistaDarAcceso, '/darAcceso')

jwt = JWTManager(app)