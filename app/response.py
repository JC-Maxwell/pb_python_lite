# -​*- coding: utf-8 -*​-import os

from flask import json
from flask import make_response

class Error(Exception):

	http_code = ''
	content = ''

	def __init__(self,content,code):
		self.http_code = code
		self.content = content

	def get_json(self):
		error_json = self.content
		return json.dumps(error_json)

	def get_response(self):
		return make_response(self.get_json(),self.http_code)

class Success(Exception):

	http_code = 200
	content = ''

	def __init__(self,content):
		self.content = content

	def get_json(self):
		success_json = self.content
		return json.dumps(success_json)

	def get_type(self):
		return _Pauli_Constants.RESPONSE_TYPES['SUCCESS']
	
	def get_response(self):
		return make_response(self.get_json(),self.http_code)

def internal_server_error(e):
	print 'Wops! Internal Server Error :('
	print e
	return Error('Internal Server Error',500).get_response()

