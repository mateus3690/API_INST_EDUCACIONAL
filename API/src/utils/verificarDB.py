import os.path

class DBexiste():

     def __init__(self, base):
         self.base = base

     def verificar(self):
          base = self.base
          if(os.path.isfile(f'{base}.db')):
               return True
          else:
               return False

