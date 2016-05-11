# -​*- coding: utf-8 -*​-

import requests
from json import dumps

# P A Y B O O K    C O N S T A N T S 

PAYBOOK_LINK = 'https://sync.paybook.com/v1/'

# S E S S I O N S

class Paybook():

	def __init__(self,api_key):
		self.api_key = api_key

	def signup(self,username):
		id_user = None
		conn = requests.post(PAYBOOK_LINK + 'users', data = {"api_key":self.api_key, "name":username})
		if conn.status_code == 200:
			id_user = conn.json()['response']['id_user']
		return id_user

	def login(self,id_user):
		token = None
		conn = requests.post(PAYBOOK_LINK + 'sessions', data = {"api_key": self.api_key, "id_user": id_user})
		if conn.status_code == 200:
			token = conn.json()['response']['token']		
		return token

	# C R E D E N T I A L S   A N D    S T A T U S

	def catalogs(self,token):
		catalogs = []
		conn = requests.get(PAYBOOK_LINK + 'catalogues/sites', params = {"token":token})
		if conn.status_code == 200:
			catalogs = conn.json()['response']
		return catalogs

	def credentials(self,token,id_site,id_user,credentials_user,credentials_password):
		new_credentials = None
		data = {
			'api_key' : self.api_key,
			'token' : token,
			'id_site' : id_site,
			'id_user' : id_user,
			'credentials' : {
				'rfc' : credentials_user,
				'password' : credentials_password
			}
		}#End of data
		print data
		conn = requests.post(PAYBOOK_LINK + 'credentials', data = dumps(data))
		if conn.status_code == 200:
			new_credentials = conn.json()['response']
		return new_credentials
			
	def status(self,token,id_site,status):
		site_status = None
		headers = {'Content-type' : 'application/json'}		
		data = {
			'token' : token,
			'id_site' : id_site
		}# End of data					
		conn = requests.get(status,headers=headers, data = dumps(data))
		if conn.status_code == 200:
			site_status = conn.json()['response']
		return site_status
		
	# A C C O U N T S   A N D    T R A N S A C T I O N S

	def accounts(self,token,id_site):
		site_accounts = None
		data = {
			'token' : token,
			'id_site' : id_site
		}# End of data
		conn = requests.get(PAYBOOK_LINK + 'accounts', params = data)	
		print conn.json()
		if conn.status_code == 200:
			site_accounts = conn.json()['response']
		return site_accounts

	def transactions(self,token,id_account):
		account_transactions = None
		data = {}
		data['token'] = token
		data['id_account'] = id_account		
		conn = requests.get(PAYBOOK_LINK + 'transactions', params = data)
		if conn.status_code == 200:
			account_transactions = conn.json()['response']
		return account_transactions
