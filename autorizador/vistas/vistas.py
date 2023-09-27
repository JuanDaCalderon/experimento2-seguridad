from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
import hashlib
from ..modelos import db, Usuario


class VistaAutorizar(Resource):
    def post(self):
        usuarioName = request.json["usuario"] #NOMBRE DEL USUARIO EN EL CAMPO 'USUARIO'
        cryptedPassword = hashlib.md5(request.json["password"].encode('utf-8')).hexdigest() #CONTRASEÑA DIGITADA POR EL USUARIO ENCRIPTADA
        usuarioExistente = Usuario.query.filter(Usuario.usuario == usuarioName).first() #BUSCA SI YA HAY UN USUARIO CON ESE NOMBRE
        idNewUser = len(Usuario.query.all()) + 1 #BUSCA TODOS LOS USUARIOS PARA SABER EL ID DEL NUEVO USUARIO SEGUN LA LONGITUD DEL ARRAY
        if usuarioExistente is None: #SI EL USUARIO CON ESE NOMBRE NO FUE ENCONTRADO ENTONCES NO EXISTE Y LO CREA EN LA BASE DE DATOS
            token = create_access_token(identity=idNewUser)
            newUser = Usuario(usuario=usuarioName, password=cryptedPassword, token=token)
            db.session.add(newUser)
            db.session.commit()
            return {
                "id": newUser.id,
                "usuario": usuarioName,
                "token": token
            }
        else: #EL USUARIO SI EXISTE
            usuarioExistenteConPassword = Usuario.query.filter(Usuario.usuario == usuarioName, Usuario.password == cryptedPassword).first() #BUSCA EL USUARIO BASADO TAMBIEN EN LA CONTRASEÑA YA SABIENDO QUE SI EXISTE
            if usuarioExistenteConPassword is None:
                return {"mensaje": "contraseña incorrecta" }, 404
            else:
                token = usuarioExistenteConPassword.token
                return {"mensaje": "Inicio de sesión exitoso", "token": token, "id": usuarioExistenteConPassword.id}

        
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
                return "Borrado " + usuarioExistente.token
            else:
                return "El usuario no tiene sesiones activas"