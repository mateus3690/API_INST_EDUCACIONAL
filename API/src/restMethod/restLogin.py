import repackage
repackage.up()

from config.tables import Login
from utils.validadoresCampos import ValidaCampo
from config.auth import AuthSystem
from flask_restful import Resource
from flask import request
import sqlalchemy
from flask_httpauth import HTTPBasicAuth
from config.auth import crypMD5, AuthSystem

auth = HTTPBasicAuth()
@auth.verify_password
def verifySistem(login, password):
    return AuthSystem(login=login, password=password)


class DirectLogin(Resource):
     
     
     def get(self, email, senha):

          try:
               login = Login.query.filter_by(email=email,
                                             senha= (crypMD5(senha) + 'TFHKKFJSTOJ8F')
                                            ).first()
               response = {
                    'id':         login.id,
                    'nome':       login.nome,
                    'nascimento': login.nascimento,
                    'cpf':        login.cpf,
                    'email':      login.email
               }

          except AttributeError:
               response = {
                    'status':'Error',
                         'mensagem':"Usuário não existe nos registros"
               }        

          return response
     
     def put(self, email, senha):

          try:
               login = Login.query.filter_by(email=email,
                                             senha= (crypMD5(senha) + 'TFHKKFJSTOJ8F')
                                            ).first()
               dados = request.json
               analiseCpf = ValidaCampo(cpf=dados['cpf'])
               analiseEmail = ValidaCampo(email=dados['email'])
               senha = len(senha) * '*'

               if analiseCpf.analisaCPF() == True and analiseEmail.analisaEmail() == True:

                    login.cpf = dados['cpf']
                    login.email = dados['email']

                    if 'nome' in dados:
                         login.nome = dados['nome']

                    if 'nascimento' in dados:
                         login.nascimento = dados['nascimento']                       
                    
                    if 'senha' in dados:                       
                         login.senha = crypMD5(dados['senha']) + 'TFHKKFJSTOJ8F'
                         senha = dados['senha']
                    login.save()

                    response = {
                         'id':         login.id,
                         "nome":       login.nome,
                         "nascimento": login.nascimento,
                         "cpf":        login.cpf,
                         "email":      login.email,
                         "senha":      senha
                    }

               elif analiseCpf.analisaCPF() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'CPF inválido!'
                    }

               elif analiseEmail.analisaEmail() == True:
                    response = {
                         'status':'Error',
                         'mensagem':'E-mail inválido!'
                    }

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }
          
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':"Login indefinido!"
               }
          
          except sqlalchemy.exc.IntegrityError:
               response = {
                    'status':'Error',
                    'mensagem':'Usuário já esta registado no sistema!'
               }
          
          return response

     def delete(self, email, senha):
          
          try:
               login = Login.query.filter_by(email=email,
                                             senha= (crypMD5(senha) + 'TFHKKFJSTOJ8F')
                                            ).first()
               nome = login.nome
               login.delete()
               response = {
                    'status':'Ok',
                    'mensagem':f'O usuario {nome} foi deletado dos registros'
               }
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Por favor informe um usuário existente nos registros'
               }
          
          return response


class DirectLoginPass(Resource):

     @auth.login_required
     def get(self):
          logins = Login.query.all()
          response = [{
                    'id':         dados.id,
                    'nome':       dados.nome,
                    'nascimento': dados.nascimento,
                    'cpf':        dados.cpf,
                    'email':      dados.email,         
          } for dados in logins]

          if response == []:
                response = {"mensagem":"Nenhum registro no momento"}
          
          return response
     
     def post(self):
          
          try:

               dados = request.json
               analiseCpf = ValidaCampo(cpf=dados['cpf'])
               analiseEmail = ValidaCampo(email=dados['email'])

               if analiseCpf.analisaCPF() == True and analiseEmail.analisaEmail() == True:
                    login = Login(nome          = dados['nome'],
                                  nascimento    = dados['nascimento'],
                                  cpf           = dados['cpf'],
                                  email         = dados['email'],
                                  senha         = (crypMD5(dados['senha']) + 'TFHKKFJSTOJ8F')
                              )

                    login.save()

                    response = {
                         'id':         login.id,
                         "nome":       login.nome,
                         "nascimento": login.nascimento,
                         "cpf":        login.cpf,
                         "email":      login.email,
                         "senha":      dados['senha']
                    }
               
               elif analiseCpf.analisaCPF() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'CPF inválido!'
                    }

               elif analiseEmail.analisaEmail() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'Email inválido!'
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
                    'mensagem':'Usuario já esta registado no sistema!'
               }

          return response
