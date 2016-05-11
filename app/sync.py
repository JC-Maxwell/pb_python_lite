# -​*- coding: utf-8 -*​-import os

from pb_sdk.paybook import Paybook as _Paybook
from app import db as _DB
from app import constants as _Constants

paybook = _Paybook(_Constants.API_KEY)

def catalogs(token):
	catalogs = paybook.catalogs(token)
	return catalogs

def credentials(token,id_site,credentials_user,credentials_password):
	user = _DB.User(token)
	id_user = user.get_id_user()
	new_credentials = paybook.credentials(token,id_site,id_user,credentials_user,credentials_password)
	ws = new_credentials['ws']
	status = new_credentials['status']
	twofa = new_credentials['twofa']
	id_credential = new_credentials['id_credential']
	credentials = _DB.Credentials(id_user,id_site,ws,status,twofa,id_credential)
	if not credentials.do_i_exist():
		credentials.save()
	return new_credentials

def status(token,id_site):
	user = _DB.User(token)
	id_user = user.get_id_user()
	credentials = _DB.Credentials(id_user,id_site)
	# twofa = credentials.get_twofa()
	url_status = credentials.get_status()
	site_status = paybook.status(token,id_site,url_status)#instead of twofa
	return site_status

def accounts(token,id_site):
	site_accounts = paybook.accounts(token,id_site)
	return site_accounts

def transactions(token,id_account):
	account_transactions = paybook.transactions(token,id_account)
	return account_transactions
	