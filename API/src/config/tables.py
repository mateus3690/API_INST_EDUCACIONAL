import repackage
repackage.up()

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from utils.verificarDB import DBexiste

base = 'BaseLocal'
engine = create_engine(f'sqlite:///{base}.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Cursos(Base):
    
     __tablename__ = 'tb_cursos'
     id = Column(Integer, primary_key=True, unique=True)
     nome = Column(String(80), unique=True)
     tempo_duracao = Column(Integer)
     descricao = Column(String(100))

     def __repr__(self):
         return f'<Curso {self.nome}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()


class  Alunos(Base):

     __tablename__ = 'tb_alunos'
     id = Column(Integer, primary_key=True, unique=True)
     nome = Column(String(50), index=True)
     nascimento = Column(String(10))
     cpf = Column(String(11), index=True, unique=True)
     rg = Column(String(16), unique=True)
     endereco =  Column(String(80))
     mensalidade = Column(NUMERIC(5,2))
     id_curso = Column(Integer, ForeignKey('tb_cursos.id'))
     curso = Column(String(80))
     #tb_cursos = relationship('Cursos')

     def __repr__(self):
         return f'<Aluno {self.nome}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()


class Professores(Base):

     __tablename__ = 'tb_professores'
     id = Column(Integer, primary_key=True, unique=True)
     nome = Column(String(50), index=True)
     nascimento = Column(String(10))
     cpf = Column(String(11), index=True, unique=True)
     rg = Column(String(16), unique=True)
     endereco =  Column(String(80))
     salario = Column(NUMERIC(5,2))
     materia = Column(String(50))    
     id_curso = Column(Integer, ForeignKey('tb_cursos.id'))
     curso = Column(String(80))
     #tb_cursos = relationship('Cursos')

     def __repr__(self):
         return f'<Professor {self.nome}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()


class Usuario(Base):
     
     __tablename__ = 'tb_usuario'
     id = Column(Integer, primary_key=True)
     login = Column(String(16), unique=True)
     senha = Column(String(16))
     tipo_usuario = Column(String(1), default='N')


     def __repr__(self):
         return f'<Usuario {self.usuario}>'
     
     def save(self):
          db_session.add(self)
          db_session.commit()
     
     def delete(self):
          db_session.delete(self)
          db_session.commit()


def init_db():
     Base.metadata.create_all(bind=engine)

#if DBexiste(base) == False:
init_db()
