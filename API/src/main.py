import repackage
repackage.up()

from flask import Flask
from flask_restful import Api
from restMethod.restCursos import DirectCursos, DirectCursosPass
from restMethod.restAlunos import DirectAlunos, DirectAlunosPass
from restMethod.restProfessores import DirectProfessores, DirectProfessoresPass
from restMethod.restAuth import DirectAuth, DirectAuthPass

app = Flask(__name__)
api = Api(app)

api.add_resource(DirectCursos, '/cursos/<int:id>/' )
api.add_resource(DirectCursosPass, '/cursos/' )

api.add_resource(DirectAlunos, '/alunos/<int:id>/' )
api.add_resource(DirectAlunosPass, '/alunos/' )

api.add_resource(DirectProfessores, '/profess/<int:id>/' )#DirectAuthPass
api.add_resource(DirectProfessoresPass, '/profess/' )

api.add_resource(DirectAuth, '/usuarios/<int:id>/' )
api.add_resource(DirectAuthPass, '/usuarios/' )


if __name__ == '__main__':
     app.run(debug=True)

     