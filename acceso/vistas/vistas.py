from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
import hashlib
from ..modelos import db, Menu, MenuSchema

menu_schema =MenuSchema()
class VistaAcceso(Resource):
    jwt_required()
    def get(self):
        menus = Menu.query.all()
        return [menu_schema.dump(menu) for menu in menus]

        
