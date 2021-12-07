import repackage
repackage.up()

from utils.validadores import ValidaCampo
from config.tables import Professores, Cursos
from config.auth import AuthSystem, AuthUser
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

class DirectProfessores(Resource):
     
     def get(self, id):

          try:
               professor = Professores.query.filter_by(id=id).first()
               response = {
                         'id': 		  professor.id,	
                         'nome':          professor.nome,
                         'nascimento':    professor.nascimento,
                         'cpf':           professor.cpf,
                         'rg':            professor.rg,
                         'endereco':      professor.endereco,
                         'salario':       f"{professor.salario}",
                         'materia':       professor.materia,
                         'curso':         professor.curso,
                         'id_curso':      professor.id_curso    
                    }

          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':f"O professor não existe nos registros"
               }


          return response
     
     def put(self, id):

          try: 
               professor = Professores.query.filter_by(id=id).first()
               dados = request.json
               
               analis1 = ValidaCampo(cpf=dados['cpf'])
               analis2 = ValidaCampo(rg=dados['rg'])

               if analis1.analisaCPF() == True and analis2.analisaRG() == True:

                    professor.cpf = dados['cpf']
                    professor.rg = dados['rg']

                    if 'nome' in dados:
                         professor.nome = dados['nome']
                    
                    if 'nascimento' in dados:
                         professor.nascimento = dados['nascimento']

                    if 'endereco' in dados:
                         professor.endereco = dados['endereco']
                    
                    if 'salario' in dados:
                         professor.salario = dados['salario']
                    
                    if 'materia' in dados:
                         professor.materia = dados['materia']
                    
                    if 'curso' in dados:
                         curso = Cursos.query.filter_by(nome=dados['curso']).first()
                         professor.curso = curso.nome
                         professor.id_curso = curso.id

                    response = {
                              "id": 		  professor.id,	
                              "nome":          professor.nome,
                              "nascimento":    professor.nascimento,
                              "cpf":           professor.cpf,
                              "rg":            professor.rg,
                              "endereco":      professor.endereco,
                              "salario":       f"{professor.salario}",
                              "materia":       professor.materia,
                              "curso":         professor.curso,
                              "id_curso":      professor.id_curso        
                         }
                   
                    professor.save()


               elif analis1.analisaCPF() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'CPF inválido!'
                    }

               elif analis2.analisaRG() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'RG inválido!'
                    }
                    
          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }

          return response

     def delete(self, id):
          
          try:
               professor = Professores.query.filter_by(id=id).first()
               nome = professor.nome
               professor.delete()
               response = {
                    'status':'Ok',
                    'mensagem':f'O professor {nome} foi deletado dos registros'
               }

          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Por favor informe um professor existente nos registros'
               }


          return response


class DirectProfessoresPass(Resource):

     def get(self):
          professor = Professores.query.all()
          response = [{
                    'id': 		  dados.id,	
                    'nome':          dados.nome,
                    'nascimento':    dados.nascimento,
                    'cpf':           dados.cpf,
                    'rg':            dados.rg,
                    'endereco':      dados.endereco,
                    'salario':       f"{dados.salario}",
                    'materia':       dados.materia,
                    'curso':         dados.curso,
                    'id_curso':      dados.id_curso        
          } for dados in professor]
          
          if response == []:
                response = {"mensagem":"Nenhum registro no momento"}

          return response
     
     def post(self):
          
          try:
               dados = request.json
               curso = Cursos.query.filter_by(nome=dados['curso']).first()

               analis1 = ValidaCampo(cpf=dados['cpf'])
               analis2  = ValidaCampo(rg=dados['rg'])

               if analis1.analisaCPF() == True and analis2.analisaRG() == True:


                    professor = Professores(nome = dados['nome'],
                                             nascimento = dados['nascimento'],
                                             cpf = dados['cpf'],
                                             rg = dados['rg'],
                                             endereco = dados['endereco'],
                                             salario = dados['salario'],
                                             materia = dados['materia'],
                                             curso = curso.nome,
                                             id_curso  = curso.id,
                                             #tb_cursos = curso
                                        )
                    professor.save()

                    response = {
                         'id': 		  professor.id,	
                         'nome':          professor.nome,
                         'nascimento':    professor.nascimento,
                         'cpf':           professor.cpf,
                         'rg':            professor.rg,
                         'endereco':      professor.endereco,
                         'salario':       f"{professor.salario}",
                         'materia':       professor.materia,
                         'curso':         professor.curso,
                         'id_curso':      professor.id_curso        
                    }

               elif analis1.analisaCPF() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'CPF inválido!'
                    }

               elif analis2.analisaRG() == False:
                    response = {
                         'status':'Error',
                         'mensagem':'RG inválido!'
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
          
          except AttributeError:

               response = {
                    'status':'Error',
                    'mensagem':'Dados inconsistente'
               }

          except sqlalchemy.exc.IntegrityError:
               response = {
                    'status':'Error',
                    'mensagem':'professor já esta registado no sistema!'
               }
               
          return response
