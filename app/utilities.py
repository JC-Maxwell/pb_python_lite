# -​*- coding: utf-8 -*​-

import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name):
	file_name = name + '.log'
	complete_file_name = './' + file_name
	logging_level = logging.DEBUG
	formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(module)s - %(funcName)s:%(lineno)d - %(message)s','%Y-%m-%d %H:%M:%S')
	formatter = logging.Formatter('%(message)s')		
	logging_handler = TimedRotatingFileHandler(complete_file_name, when='midnight')
	logging_handler.setFormatter(formatter)
	logger = logging.getLogger(name)
	logger.setLevel(logging_level)		
	logger.addHandler(logging_handler)
	return logger