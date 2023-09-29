from flask import request
from flask_jwt_extended import create_access_token, decode_token
from flask_restful import Resource
import hashlib
from ..modelos import db, Usuario
from datetime import datetime, timedelta


class VistaAutorizar(Resource):
    def post(self):
        usuarioName = request.json["usuario"] # NOMBRE DEL USUARIO EN EL CAMPO 'USUARIO'
        cryptedPassword = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest() # CONTRASEÑA DIGITADA POR EL USUARIO ENCRIPTADA
        usuarioExistente = Usuario.query.filter(Usuario.usuario == usuarioName).first() # BUSCA SI YA HAY UN USUARIO CON ESE NOMBRE
        idNewUser = len(Usuario.query.all()) + 1 # BUSCA TODOS LOS USUARIOS PARA SABER EL ID DEL NUEVO USUARIO SEGUN LA LONGITUD DEL ARRAY
        if usuarioExistente is None:  # SI EL USUARIO CON ESE NOMBRE NO FUE ENCONTRADO ENTONCES NO EXISTE Y LO CREA EN LA BASE DE DATOS
            today = datetime.now()
            expDate = timedelta(minutes=5)
            additional_claims = {"expDate": str(today + expDate)}
            token = create_access_token(identity=idNewUser, additional_claims=additional_claims, expires_delta=expDate)
            newUser = Usuario(usuario=usuarioName, password=cryptedPassword, token=token)
            db.session.add(newUser)
            db.session.commit()
            return {
                "id": newUser.id,
                "usuario": usuarioName,
                "token": token
            }
        else:  # EL USUARIO SI EXISTE
            usuarioExistenteConPassword = Usuario.query.filter(Usuario.usuario == usuarioName, Usuario.password == cryptedPassword).first() # BUSCA EL USUARIO BASADO TAMBIEN EN LA CONTRASEÑA YA SABIENDO QUE SI EXISTE
            if usuarioExistenteConPassword is None:
                return {"mensaje": "contraseña incorrecta"}, 404
            else:
                token = usuarioExistenteConPassword.token
                if token == "":
                    idNewUser = usuarioExistenteConPassword.id
                    today = datetime.now()
                    expDate = timedelta(minutes=5)
                    additional_claims = {"expDate": str(today + expDate)}
                    token = create_access_token(identity=idNewUser, additional_claims=additional_claims, expires_delta=expDate)
                    usuarioExistenteConPassword.token = token
                    db.session.commit()
                    return {
                            "id": idNewUser,
                            "usuario": usuarioExistenteConPassword.usuario,
                            "token": token
                        }
                else:              
                    dateFormat = "%Y-%m-%d %H:%M:%S"
                    tokenDecodedWithExpired = decode_token(encoded_token=token, allow_expired=True)
                    expDate = str(tokenDecodedWithExpired['expDate'])
                    hoyInDate = str(datetime.now())
                    cutHoyInDate = hoyInDate[:hoyInDate.rfind(".")]
                    cutExpInDate = expDate[:expDate.rfind(".")]
                    hoyInDateToCompare = datetime.strptime(cutHoyInDate, dateFormat)
                    ExpInDateToCompare = datetime.strptime(cutExpInDate, dateFormat)
                    if hoyInDateToCompare < ExpInDateToCompare:
                        return {
                            "mensaje": "Ya hay un token activo, solo puedes tener una sesión activa a la vez, por favor cierra sesión para generar un nuevo token"
                        }, 404
                    else:
                        return {
                            "mensaje": "el token ya expiro"
                        }, 404
                    
                
class VistaLogOut(Resource):
    def post(self):
        idUsuario = request.json["idUsuario"]
        usuarioExistente = Usuario.query.filter(Usuario.id == idUsuario).first() #BUSCA SI YA HAY UN USUARIO CON ESE ID   
        if usuarioExistente is None:
            return "No existen usuarios con ese id"
        else: # EL USUARIO SI EXISTE
            if usuarioExistente.token != "":    #EL USUARIO TIENE UN TOKEN EN LA TABLA, ES DECIR, TIENE SESION ACTIVA
                usuarioExistente.token = ""
                db.session.commit()
                return "La sesión ha sido cerrada"
            else:
                return "El usuario no tiene sesiones activas"
            
class VistaVerificarToken(Resource):
    def post(self):
        idUsuario = request.json["id"]
        token = request.json["token"]
        usuarioExistente = Usuario.query.filter(Usuario.id == idUsuario).first() # BUSCA EL USUARIO CON ESTE ID
        if usuarioExistente is None:
            return { "mensaje": "No hay usuario asociados a este id" }, 404
        else:
            usuarioExistenteConToken = Usuario.query.filter(Usuario.id == idUsuario, Usuario.token == token).first() # BUSCA EL USUARIO CON ESTE ID
            if usuarioExistenteConToken is None:
                return { "mensaje": "para este usuario, el token enviado ya no es valido" }, 404
            else:
                tokenFromUser = usuarioExistenteConToken.token
                dateFormat = "%Y-%m-%d %H:%M:%S"
                tokenDecodedWithExpired = decode_token(encoded_token=tokenFromUser, allow_expired=True)
                expDate = str(tokenDecodedWithExpired['expDate'])
                hoyInDate = str(datetime.now())
                cutHoyInDate = hoyInDate[:hoyInDate.rfind(".")]
                cutExpInDate = expDate[:expDate.rfind(".")]
                hoyInDateToCompare = datetime.strptime(cutHoyInDate, dateFormat)
                ExpInDateToCompare = datetime.strptime(cutExpInDate, dateFormat)
                if hoyInDateToCompare < ExpInDateToCompare:
                    return { "mensaje": "El token esta activo y es valido" }
                else:
                    return {
                        "mensaje": "el token ya expiro y es invalido"
                    }, 404
                