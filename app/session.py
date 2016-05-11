# -​*- coding: utf-8 -*​-import os

from app import db as _DB
from app import constants as _Constants
from pb_sdk.paybook import Paybook as _Paybook

paybook = _Paybook(_Constants.API_KEY)

def signup(username,password):
	signed_up = 'Error'
	user = _DB.User(username,password)
	if not user.do_i_exist():
		id_user = paybook.signup(username)
		if id_user is not None:
			user.set_id_user(id_user)
			user.save()
			signed_up = True
	return signed_up

def login(username,password):
	token = 'Error'
	user = _DB.User(username,password)
	if user.login():
		id_user = user.get_id_user()
		token = paybook.login(id_user)
		user.set_token(token)
	return token
