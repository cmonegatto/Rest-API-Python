from flask_restful 		import Resource, reqparse
from models.hotel 		import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros 	import normalize_path_params, consulta_sem_cidade, consulta_com_cidade

#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

#
class Hoteis(Resource):
	def get(self):
		connection = sqlite3.connect('banco.db')
		cursor = connection.cursor()

		dados = path_params.parse_args()
		print(dados)
		dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
		print (dados_validos)

		parametros = normalize_path_params(**dados_validos)
		
		if not parametros.get('cidade'):
			tupla = tuple([parametros[chave] for chave in parametros])
			resultado = cursor.execute(consulta_sem_cidade, tupla)
		else:
			tupla = tuple([parametros[chave] for chave in parametros])
			resultado = cursor.execute(consulta_com_cidade, tupla)
		
		#print (parametros)

		hoteis = []
		for linha in resultado:
			hoteis.append({
				'hotel_id': linha[0],
				'nome': linha[1],
				'estrelas': linha[2],
				'diaria': linha[3],
				'cidade': linha[4],
				'site_id': linha[5]
				})

		return{'hoteis': hoteis}


class Hotel(Resource):

	argumentos = reqparse.RequestParser()
	argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' deve ser preenchido")
	argumentos.add_argument('estrelas', type=float, required=True, help="O campo 'estrelas' deve ser preenchido")
	argumentos.add_argument('diaria')
	argumentos.add_argument('cidade')
	argumentos.add_argument('site_id', type=int, required=True, help="Todo hotel precisa estar linkado com o site")


	def get(self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			return hotel.json()
		return{'message': 'Hotal not found.'}, 404 #not found


	@jwt_required
	def post(self, hotel_id):

		if HotelModel.find_hotel(hotel_id):
			return {"message": "Hotel id '{}'already exists.".format(hotel_id)}, 400

		dados = Hotel.argumentos.parse_args()
		hotel = HotelModel(hotel_id, **dados)

		if not SiteModel.find_by_id(dados.get['site_id']):
			return {'message': 'Hotel precisa estar associaddo a um site_id valido'}, 400


		try:
			hotel.save_hotel()
		except:
			return{'message': 'Ocorreu um erro tentando salvar o registro'}, 500 #internal server error
		return hotel.json()

	@jwt_required
	def put(self, hotel_id):
		dados = Hotel.argumentos.parse_args()
		hotel_encontrado = HotelModel.find_hotel(hotel_id)

		if hotel_encontrado:
			hotel_encontrado.update_hotel(**dados)
			hotel_encontrado.save_hotel()
			return hotel_encontrado.json(), 200 # ok
		hotel = HotelModel(hotel_id, **dados)

		try:
			hotel.save_hotel()
		except:
			return{'message': 'Ocorreu um erro tentando salvar o registro'}, 500 #internal server error
		return hotel.json(), 201 #created
	
	@jwt_required
	def delete(self, hotel_id):
		hotel = HotelModel.find_hotel(hotel_id)
		if hotel:
			try:
				hotel.delete_hotel()
			except:
				return{'message': 'Ocorreu um erro tentando salvar o registro'}, 500 #internal server error
			return { 'message': 'Hotel deleted.'}
		return { 'message': 'Hotel not found.'}, 404

