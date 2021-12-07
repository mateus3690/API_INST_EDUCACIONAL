import repackage
repackage.up()

from config.tables import Usuario
from config.auth import crypMD5, AuthSystem, AuthUser
from flask_restful import Resource
from flask import request
import sqlalchemy
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
@auth.verify_password
def verifySistem(login, password):
    return AuthSystem(login=login, password=password)

auth2 = HTTPBasicAuth()
@auth2.verify_password
def verifyUser(login, password):
    return AuthUser(login=login, password=password)

class DirectAuth(Resource):
     
     def get(self, id):

          try:
               user = Usuario.query.filter_by(id=id).first()
               if user.login == str('ADMINISTRADOR').lower():
                    response = {
                         'Status':'Falta de permissão',
                         'aviso':"Usuário Confindêncial",
                    }
               else:
                    response = {
                         'id':    user.id,
                         'login': user.login
                    }

          except AttributeError:
               response = {
                    'status':'Error',
                         'mensagem':f"Usuario não existe nos registros"
               }

          return response
     
     def put(self, id):

          try:
               user = Usuario.query.filter_by(id=id).first()
               dados = request.json

               if user.login != str('ADMINISTRADOR').lower:
                    if 'login' in dados:
                         user.login = dados['login']
                    
                    if 'senha' in dados:
                         user.senha = dados['senha']

                    user.save()

                    response = {
                         'id':   user.id,
                         'nome': user.login
                    }

               else:
                    response = {
                         'Status':'Falta de permissão',
                         'aviso':"Usuário Confindêncial",
                    }

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }
          

          return response

     @auth.login_required
     def delete(self, id):
          
          try:
               user = Usuario.query.filter_by(id=id).first()
               login = user.login

               if login != str('ADMINISTRADOR').lower:
                    user.delete()
                    response = {
                         'status':'Ok',
                         'mensagem':f'O usuário {login} foi deletado dos registros'
                    }
               
               else:
                    response = {
                         'Status':'Falta de permissão',
                         'aviso':"Usuário Confindêncial",
                    }

          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Por favor informe um usuário existente nos registros'
               }
          
          return response


class DirectAuthPass(Resource):

     @auth.login_required
     def get(self):
          users = Usuario.query.all()
          response = [{
                    'id':           dados.id,
                    'nome':         dados.login    
          } for dados in users
               if dados.login!= str('ADMINISTRADOR').lower()]

          if response == []:
                response = {"mensagem":"Nenhum registro no momento"}
          
          return response
     
     def post(self):
          
          try:

               dados = request.json
               existe = Usuario.query.filter_by(tipo_usuario=dados['tipo_usuario']).first()
               tipo_user = 'N'

               if dados['tipo_usuario'] == "A" and existe.tipo_usuario != "A":
                    tipo_user = dados['tipo_usuario']

               user = Usuario(login = dados['login'],
                              senha = (crypMD5(dados['senha']) + 'TFHKKFJSTOJ8F'),
                              tipo_usuario = tipo_user)

               user.save()

               response = {
                    'id':user.id,
                    'login':user.login,
                    'senha':dados['senha'],
                    'tipo_usuario':user.tipo_usuario
               }

          except KeyError:
               response = {
                    'status':'Error',
                    'mensagem':'Falta informação no registro'
               }
          
          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':'Null'
               }
          
          except sqlalchemy.exc.IntegrityError:
               response = {
                    'status':'Error',
                    'mensagem':'Curso já esta registado no sistema!'
               }

          return response
