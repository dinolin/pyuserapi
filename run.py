from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import Config
import logging
from flask_jwt_extended import JWTManager

handler = logging.FileHandler('flask.log', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
db = SQLAlchemy()
app =  Flask(__name__)

#def getlogger():
#	return app.logger

@app.before_first_request
def create_tables():
    db.create_all()
#    db.session.commit()

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	if request.method == 'OPTIONS':
		response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
		headers = request.headers.get('Access-Control-Request-Headers')
		if headers:
			response.headers['Access-Control-Allow-Headers'] = headers
	return response

def create_app(config_name):
	api = Api(app)
	app.config.from_object(Config)
	jwt = JWTManager(app)
	app.logger.addHandler(handler)
	app.logger.info('App Start')
	
	app.logger.info('DB Init')
	db = SQLAlchemy(app)
	db.init_app(app)
	
	app.logger.info('Blueprint Init')
	#from V_1_0.views import resources as api_1_0_blueprint
	from V_2_0.views import resources as api_2_0_blueprint
	#app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
	app.register_blueprint(api_2_0_blueprint, url_prefix='/api/v2.0')

	return app


def getApp():
	return app
