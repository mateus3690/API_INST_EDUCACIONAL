import repackage
repackage.up()

from config.tables import Usuario
from hashlib import md5


def crypMD5(senha):

     crypt = md5(senha.encode())
     return crypt.hexdigest()


def AuthSystem(login, password):

     if not (login, password):
          return False
     
     return Usuario.query.filter_by(login = login,
                                   senha = (crypMD5(password) + 'TFHKKFJSTOJ8F'),
                                   tipo_usuario='A').first()

def AuthUser(login, password):

     if not (login, password):
          return False

     return Usuario.query.filter_by(login = login,
                                        senha = (crypMD5(password) + 'TFHKKFJSTOJ8F'), 
                                        tipo_usuario='N').first()
 
                                        