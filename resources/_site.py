from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
	def get(self):
		return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
	def get(self, url):
		site = SiteModel.find_site(url)
		if site:
			return site.json()
		return {'message': 'Sitge not found.'}, 404 #not found

	def post(self, url):
		if SiteModel.find_site(url):
			return {"message": "The site '{}' already exists."}, 400 #bad request
		site = SiteModel(url)
		try:
			site.save_site()
		except:
			return {"message": "Ocorreu um erro interno criando um novo site."}, 500
		return site.json()

	def delete(self, url):
		site = SiteModel.find_site()
		if site:
			site.delete_site()
			return{'message': 'Site deletado.'}
		return{'message': 'Site não encontrado.'}, 404

