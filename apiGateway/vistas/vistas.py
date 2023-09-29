from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, get_csrf_token
import requests
from flask_restful import Resource


class VistaLogin(Resource):
    def post(self):
        data = request.get_json()
        autorizador = "http://localhost:5001/autorizar"
        respuesta = requests.post(autorizador, json=data)
        return respuesta.json()


class VistaDarAcceso(Resource):
    @jwt_required()
    def post(self):
        idTokenUsuario = get_jwt_identity()
        print("Aquí es token id", idTokenUsuario)
        tokenOriginalCompleto = request.headers.get('Authorization')
        tokenOriginal = tokenOriginalCompleto.split(' ')[1] if tokenOriginalCompleto else None
        print(tokenOriginal)

        autorizador = "http://localhost:5001/verificar"
        data = {
            "id": idTokenUsuario,
            "token": tokenOriginal
        }
        respuesta = requests.post(autorizador, json=data)

        if respuesta.status_code == 200:
            acceso = "http://localhost:5002/acceso"
            headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {tokenOriginal}"}
            respuestaAcceso = requests.get(acceso, json='', headers=headers)
            return respuestaAcceso.json()
        
        return {"Mensaje": "Error"}