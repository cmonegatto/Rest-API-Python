import json
import requests

URL = 'http://127.0.0.1:5000'

'''
#Testando API de GET HOTEIS
resposta_hoteis = requests.request('GET', URL + '/hoteis?cidade=Rio de Janeiro')
print (resposta_hoteis.status_code)
hoteis = resposta_hoteis.json()

print(hoteis['hoteis'])
#print(hoteis['hoteis'][0])
#print(len(hoteis['hoteis']))
print('------')

lista_hoteis = hoteis['hoteis']
for hotel in lista_hoteis:
	print(hotel['nome'])
'''

'''
# Testando uma 2 APIs do mercado livre

ML_URL = 'https://api.mercadolibre.com/sites'

lista_sites = requests.request('GET', ML_URL)
print(lista_sites.json())

print('-----------------')
ML_URL = 'https://api.mercadolibre.com/sites/MLB/categories'
lista_sites = requests.request('GET', ML_URL)
print(lista_sites.json())
'''

'''
# Utilizando metodo POST para criar usuario, com os argumentos Content-type
_endpoint = URL + '/cadastro'
_body = {
	'login': 'jose',
	'senha': 'abc123'
}

_headers = {
	'Content-Type': 'application/json'
}

_resposta = requests.request('POST', _endpoint, json=_body, headers=_headers)
print(_resposta.status_code)
print (_resposta.json())


'''



# Logando, gerando o token e passando para o POST para criação de um HOTEL
_endpoint = URL + '/login'
_body = {
	'login': 'ana',
	'senha': 'asdf'
}

_headers = {
	'Content-Type': 'application/json'
}

_resposta = requests.request('POST', _endpoint, json=_body, headers=_headers)
token = _resposta.json()


'''
# Criando um HOTEL PUT
_endpoint = URL + '/hoteis/pullman'
_body = {
    "nome": "Pullman Hotel",
    "estrelas": 4.8,
    "diaria": 780.00,
    "cidade": "Santos",
    "site_id": 2
}


_headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer ' + token['access_token']
}


_resposta = requests.request('POST', _endpoint, json=_body, headers=_headers)
print(_resposta.status_code)
print(_resposta.json())

'''

'''
# Criando um HOTEL PUT
_endpoint = URL + '/hoteis/test'
_body = {
    "nome": "TEST Hotel",
    "estrelas": 4.3,
    "diaria": 380.00,
    "cidade": "Pirituba",
    "site_id": 1
}


_headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer ' + token['access_token']
}


_resposta = requests.request('PUT', _endpoint, json=_body, headers=_headers)
print(_endpoint)
print(_headers)
print(_resposta.status_code)
#print(_resposta.json())
'''

'''
# Recuperando somente um HOTEL 
_endpoint = URL + '/hoteis/clau'
_body = {
    "nome": "TEST Hotel",
    "estrelas": 4.3,
    "diaria": 380.00,
    "cidade": "Pirituba",
    "site_id": 1
}


_headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer ' + token['access_token']
}


_resposta = requests.request('GET', _endpoint)
print(_resposta.status_code)
print(_resposta.json())
'''

'''
# DELETANDO um HOTEL
_endpoint = URL + '/hoteis/test'
_body = {
    "nome": "TEST Hotel",
    "estrelas": 4.3,
    "diaria": 380.00,
    "cidade": "Pirituba",
    "site_id": 1
}


_headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer ' + token['access_token']
}


_resposta = requests.request('DELETE', _endpoint, json=_body, headers=_headers)
print(_resposta.json())

'''

'''
# Criando um HOTEL PUT
_endpoint = URL + '/usuarios/3'

_resposta = requests.request('GET', _endpoint)
print(_resposta.json())
'''

# DELETANDO um HOTEL PUT
_endpoint = URL + '/usuarios/3'

_headers = {
	'Content-Type': 'application/json',
	'Authorization': 'Bearer ' + token['access_token']
}

_resposta = requests.request('DELETE', _endpoint, headers=_headers)
print(_resposta.json())

