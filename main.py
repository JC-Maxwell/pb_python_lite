# -​*- coding: utf-8 -*​-

import os
from json import dumps
import json
from flask import Flask
from flask import request
from app import session as _Session
from app import sync as _Sync

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/signup", methods=['POST'])
def signup():
	params = json.loads(request.data)
	username = params['username']
	password = params['password']
	signed_up = _Session.signup(username,password)
	return json.dumps({'signed_up':signed_up})

@app.route("/login", methods=['POST'])
def login():
	params = json.loads(request.data)
	username = params['username']
	password = params['password']
	token = _Session.login(username,password)
	return json.dumps({'token':token})

@app.route("/catalogs")
def catalogs():
	params = json.loads(request.data)
	token = params['token']
	catalogs = _Sync.catalogs(token)
	return json.dumps({'catalogs':catalogs})

@app.route("/credentials", methods=['POST'])
def credentials():
	params = json.loads(request.data)
	token = params['token']
	id_site = params['id_site']
	credentials_user = params['credentials_user']
	credentials_password = params['credentials_password']
	new_credentials = _Sync.credentials(token,id_site,credentials_user,credentials_password)
	return json.dumps({'credentials':new_credentials})

@app.route("/status")
def status():
	params = json.loads(request.data)
	token = params['token']
	id_site = params['id_site']
	status = _Sync.status(token,id_site)
	return json.dumps({'status':status})
	
@app.route("/accounts")
def accounts():
	params = json.loads(request.data)
	token = params['token']
	id_site = params['id_site']
	site_accounts = _Sync.accounts(token,id_site)
	return json.dumps({'accounts':site_accounts})

@app.route("/transactions")
def transactions():
	params = json.loads(request.data)
	token = params['token']
	id_account = params['id_account']
	account_transactions = _Sync.transactions(token,id_account)
	return json.dumps({'transactions':account_transactions})

if __name__ == "__main__":
	app.debug = True
	app.run()






