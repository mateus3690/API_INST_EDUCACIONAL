import repackage
repackage.up()

from flask import Flask
from flask_restful import Api
from restMethod.restCursos import DirectCursos, DirectCursosPass
from restMethod.restAlunos import DirectAlunos, DirectAlunosPass
from restMethod.restProfessores import DirectProfessores, DirectProfessoresPass
from restMethod.restAuth import DirectAuth, DirectAuthPass
from restMethod.restLogin import DirectLogin, DirectLoginPass


app = Flask(__name__)
api = Api(app)

api.add_resource(DirectCursos, '/v1/cursos/<int:id>/' )
api.add_resource(DirectCursosPass, '/v1/cursos/' )

api.add_resource(DirectAlunos, '/v1/alunos/<int:cpf>/' )
api.add_resource(DirectAlunosPass, '/v1/alunos/' )

api.add_resource(DirectProfessores, '/v1/profess/<int:cpf>/' )
api.add_resource(DirectProfessoresPass, '/v1/profess/' )

api.add_resource(DirectAuth, '/v1/usuarios/<int:id>/' )
api.add_resource(DirectAuthPass, '/v1/usuarios/' )

api.add_resource(DirectLogin, '/v1/login/<string:email>/<string:senha>/')
api.add_resource(DirectLoginPass, '/v1/login/')

if __name__ == '__main__':
     app.run(debug=False, host="0.0.0.0")

     
