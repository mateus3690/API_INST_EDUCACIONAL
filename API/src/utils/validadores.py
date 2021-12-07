class ValidaCampo():

     def __init__(self, cpf='', rg=''):
         self.cpf = str(cpf).replace(' ', '')
         self.rg = str(rg).replace(' ', '')

     def analisaCPF(self):

          try:
               if len(self.cpf) == 11:
                    digito1, digito2  = 0

                    for numero in range(10): 

                         if numero <= 8:
                              digito1 += int(self.cpf[numero]) * (numero + 1)
                         digito2 += int(self.cpf[numero]) * (numero)

                         if numero == 8:
                              digito1 = digito1 % 11
                              if digito1 == 10:
                                   digito1 = 0
                         
                         elif numero == 9:
                              digito2 = digito2 % 11
                              if digito2 == 10:
                                   digito2 = 0



                    if str(digito1) == self.cpf[9] and str(digito2) == self.cpf[10]:
                         return True

          except ValueError:         
               return False
          
          return False

     def analisaRG(self):

          try:
               if len(self.rg) > 8 and len(self.rg) < 14:
                    int(self.rg)
                    return True

          except ValueError:
               return False

          return False
