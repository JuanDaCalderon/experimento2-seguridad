from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import requests
from flask_restful import Resource


class VistaLogin(Resource):
    def post(self):
        data = request.get_json()
        autorizador = "http://localhost:5001/autorizar"
        respuesta = requests.post(autorizador, json=data)
        return respuesta.json()


class VistaDarAcceso(Resource):
    """@jwt_required()
    def post(self):
        idTokenUsuario = get_jwt_identity()
        print("Aquí es token id", idTokenUsuario)
        tokenUsuario = get_jwt()
        print("Aquí es usuario token", tokenUsuario)"""

    @jwt_required()
    def post(self):
        data = request.get_json()
        autorizador = "http://localhost:5002/acceso"
        headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {data}"}
        respuesta = requests.get(autorizador, headers=headers)
        return respuesta.json()
    
        """print(tokenUsuario)
        autorizador = "http://localhost:5000/acceso"
        respuestaToken = requests.post(autorizador, json={"usuario": idTokenUsuario})

        if respuestaToken.status_code == 200:
            acceso = "/acceso"
            headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {idTokenUsuario}"}
            respuestaAcceso = requests.get(acceso, headers=headers)

            return respuestaAcceso
        
        return {"tokenid": idTokenUsuario, "tokenUser": tokenUsuario}
            

        #Pregunta al autorizador si el token es valido y si es valido consume url acceso"""