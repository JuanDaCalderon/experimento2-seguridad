from acceso import create_app
from .modelos import db
from flask_restful import Api
from flask_cors import CORS
from .vistas import VistaAcceso
from flask_jwt_extended import JWTManager

app = create_app()
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaAcceso, '/acceso')
jwt = JWTManager(app)