from flask_restful 		import Resource, reqparse
from models.usuario 	import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security 	import safe_str_cmp
from blacklist 			import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não deve ser deixado em branco.")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não deve ser deixado em branco.")

class User(Resource):
	# /usuarios/{user_id}
	def get(self, user_id):
		user = UserModel.find_user(user_id)
		if user:
			return user.json()
		return{'message': 'User not found.'}, 404 #not found


	@jwt_required
	def delete(self, user_id):
		user = UserModel.find_user(user_id)
		if user:
			try:
				user.delete_user()
			except:
				return{'message': 'Ocorreu um erro tentando salvar o registro'}, 500 #internal server error
			return { 'message': 'User deleted.'}
		return { 'message': 'User not found.'}, 404


class UserRegister(Resource):
	# /cadastro
	def post(self):
		dados = atributos.parse_args()

		if UserModel.find_by_login(dados['login']):
			return {"message": "O login '{}' já existe.".format(dados['login'])}

		user = UserModel(**dados)
		user.save_user()
		return {"message": "Usuário criado com sucesso"}, 201 #created


class UserLogin(Resource):

	@classmethod
	def post(cls):
		dados = atributos.parse_args()

		user = UserModel.find_by_login(dados['login'])

		#if user and safe_str_cmp(user.senha, dados['senha']):
		if user and safe_str_cmp('asdf', dados['senha']):
			token_de_acesso = create_access_token(identity=user.user_id)
			return {'access_token': token_de_acesso}, 200
		return {'message': "O username ou senha está incorreto."}, 401 # não autorizado


class UserLogout(Resource):
	@jwt_required
	def post(self):
		jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
		BLACKLIST.add(jwt_id)
		return {'message': 'Logout realizado com sucesso.'}, 200