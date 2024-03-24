# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, abort
from flask import request

from lista.models.usuario_model import UsuarioModel
from lista.schemas.usuario_schema import UsuarioSchema

class UsuarioResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("nome",
                        type=str,
                        required=True,
                        help="O nome do Usuario não pode estar em branco."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="O email do Usuario não pode estar em branco."
                        )
    def get(self,nome):
        json = ''
        try:
            usuario = UsuarioModel.encontrar_pelo_nome(nome)
            print(usuario)
            if usuario:
                schema = UsuarioSchema(exclude=['listas'])
                json = schema.dump(usuario)
            else:
                return {"message":"Usuario {} não existe".format(nome)},404
        except Exception as e:
            print(e)
            return {"message","Erro na requisição".format(nome)},500

        return json,200

    def post(self):
        try:
            data = UsuarioResource.parser.parse_args()
            if not data:
                return {"message": "Requisição sem JSON"}, 400

            if UsuarioModel.encontrar_pelo_nome(data['nome']):
                return {"message": "Usuário ja existe"}, 400
            else:
                usuario = UsuarioModel(data['nome'], data['email'])
                usuario.adicionar()
                usuario = UsuarioModel.encontrar_pelo_nome(data['nome'])

                user_schema = UsuarioSchema(exclude=['listas'])
                json = user_schema.dump(usuario)
                return json, 201

        except Exception as ex:
            print(ex)
            return {"message": "erro"}, 500

    def put(self):
        json = ''
        return json, 201
        
class UsuariosResource(Resource):
    def get(self):
        json = ""
        try:
            usuarios = UsuarioModel.listar()
            schema = UsuarioSchema(many=True,exclude=['listas'])
            json = schema.dump(usuarios)
        except Exception as e:
            print(e)
            return {"message": "Aconteceu um erro tentando retornar a lista de usuarios."}, 500
        return json, 200