import repackage
repackage.up()

from utils.validadoresCampos import ValidaCampo
from config.tables import Alunos, Cursos
from config.auth import AuthSystem
from flask_restful import Resource
from flask import request
import sqlalchemy

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
@auth.verify_password
def verifySistem(login, password):
    return AuthSystem(login=login, password=password)


class DirectAlunos(Resource):
     
     def get(self, cpf):

          try:
               aluno = Alunos.query.filter_by(cpf=str(cpf)).first()
               response = {
                         'id': 		  aluno.id,	
                         'nome':          aluno.nome,
                         'nascimento':    aluno.nascimento,
                         'cpf':           aluno.cpf,
                         'rg':            aluno.rg,
                         'endereco':      aluno.endereco,
                         'mensalidade':   f"{aluno.mensalidade}",
                         'curso':         aluno.curso,
                         'id_curso':      aluno.id_curso
                    }

          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':f"O Aluno não existe nos registros"
               }


          return response
     
     def put(self, cpf):

          try:
               aluno = Alunos.query.filter_by(cpf=str(cpf)).first()
               dados = request.json

               analis1 = ValidaCampo(cpf=dados['cpf'])
               analis2 = ValidaCampo(rg=dados['rg'])

               if analis1.analisaCPF() == True and analis2.analisaRG() == True:
                                   
                    aluno.cpf = dados['cpf']
                    aluno.rg = dados['rg']
                    if 'nome' in dados:
                         aluno.nome = dados['nome']
                    
                    if 'nascimento' in dados:
                         aluno.nascimento = dados['nascimento']

                    if 'endereco' in dados:
                         aluno.endereco = dados['endereco']
                    
                    if 'curso' in dados:
                         curso = Cursos.query.filter_by(nome=dados['curso']).first()
                         aluno.curso = curso.nome
                         aluno.id_curso = curso.id
                         aluno.mensalidade = curso.mensalidade

                    aluno.save()

                    response = {
                              'id': 	    aluno.id,	
                              'nome':       aluno.nome,
                              'nascimento': aluno.nascimento,
                              'cpf':        aluno.cpf,
                              'rg':         aluno.rg,
                              'endereco':   aluno.endereco,
                              'mensalidade':f"{aluno.mensalidade}",
                              'curso':      aluno.curso
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

          except TypeError:
               response = {
                    'status':'Error',
                    'mensagem':"Null"
               }

          except sqlalchemy.exc.IntegrityError:
               response = {
                    'status':'Error',
                    'mensagem':'Aluno já esta registado no sistema!'
               }

          return response

     def delete(self, cpf):
          
          try:
               aluno = Alunos.query.filter_by(cpf=str(cpf)).first()
               nome = aluno.nome
               aluno.delete()
               response = {
                    'status':'Ok',
                    'mensagem':f'O aluno {nome} foi deletado dos registros'
               }

          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Por favor informe um aluno existente nos registros'
               }


          return response


class DirectAlunosPass(Resource):

     @auth.login_required
     def get(self):
          aluno = Alunos.query.all()
          response = [{
                    'id': 		  dados.id,	
                    'nome':          dados.nome,
                    'nascimento':    dados.nascimento,
                    'cpf':           dados.cpf,
                    'rg':            dados.rg,
                    'endereco':      dados.endereco,
                    'mensalidade':   f"{dados.mensalidade}",
                    'curso':         dados.curso,
                    'id_curso':      dados.id_curso        
          } for dados in aluno]
          
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

                    aluno = Alunos(nome = dados['nome'],
                                   nascimento = dados['nascimento'],
                                   cpf = dados['cpf'],
                                   rg = dados['rg'],
                                   endereco = dados['endereco'],
                                   mensalidade = curso.mensalidade,
                                   curso = curso.nome,
                                   id_curso  = curso.id,
                                   #tb_cursos = curso
                                   )
                    aluno.save()

                    response = {
                              "id": 	    aluno.id,	
                              "nome":       aluno.nome,
                              "nascimento": aluno.nascimento,
                              "cpf":        aluno.cpf,
                              "rg":         aluno.rg,
                              "endereco":   aluno.endereco,
                              "mensalidade":f"{aluno.mensalidade}",
                              "curso":      aluno.curso,
                              "id_curso":   aluno.id_curso
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
                    'mensagem':'Aluno já esta registado no sistema!'
               }
               
          return response
