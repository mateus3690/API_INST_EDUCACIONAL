from re import A
import repackage
repackage.up()

from config.tables import Cursos
from config.auth import AuthSystem
from flask_restful import Resource
from flask import request
import sqlalchemy
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
@auth.verify_password
def verifySistem(login, password):
    return AuthSystem(login=login, password=password)


class DirectCursos(Resource):
     
     def get(self, id):

          try:
               curso = Cursos.query.filter_by(id=id).first()
               response = {
                    'id':           curso.id,
                    'nome':         curso.nome,
                    'tempo_duracao':curso.tempo_duracao,
                    'descricao':    curso.descricao,
                    'mensalidade':  f'{str(curso.mensalidade)}'
               }

          except AttributeError:
               response = {
                    'status':'Error',
                         'mensagem':f"Curso não existe nos registros"
               }
          

          return response
     
     @auth.login_required
     def put(self, id):

          try:
               curso = Cursos.query.filter_by(id=id).first()
               dados = request.json
               
               if 'tempo_duracao' in dados:
                    curso.tempo_duracao = dados['tempo_duracao']
               
               if 'descricao' in dados:
                    curso.descricao = dados['descricao']
               
               if 'mensalidade' in dados:
                    curso.mensalidade = dados['mensalidade']

               curso.save()

               response = {
                    'id':           curso.id,
                    'nome':         curso.nome,
                    'tempo_duracao':curso.tempo_duracao,
                    'descricao':    curso.descricao,
                    'mensalidade':  f'{str(curso.mensalidade)}'
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
               curso = Cursos.query.filter_by(id=id).first()
               nome = curso.nome
               curso.delete()
               response = {
                    'status':'Ok',
                    'mensagem':f'O curso {nome} foi deletado dos registros'
               }
          except AttributeError:
               response = {
                    'status':'Error',
                    'mensagem':'Por favor informe um curso existente nos registros'
               }
          
          return response


class DirectCursosPass(Resource):

     def get(self):
          cursos = Cursos.query.all()
          response = [{
                    'id':           dados.id,
                    'nome':         dados.nome,
                    'tempo_duracao':dados.tempo_duracao,
                    'descricao':    dados.descricao,
                    'mensalidade':  f'{str(dados.mensalidade)}'        
          } for dados in cursos]

          if response == []:
                response = {"mensagem":"Nenhum registro no momento"}
          
          return response

     @auth.login_required
     def post(self):
          
          try:

               dados = request.json
               curso = Cursos(nome = dados['nome'],
                              tempo_duracao = dados['tempo_duracao'],
                              descricao = dados['descricao'],
                              mensalidade = dados['mensalidade']
                         )

               curso.save()

               response = {
                    'id':           curso.id,
                    'nome':         curso.nome,
                    'tempo_duracao':curso.tempo_duracao,
                    'descricao':    curso.descricao,
                    'mensalidade':  f'{str(curso.mensalidade)}'
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
