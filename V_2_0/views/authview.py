
from flask_restful import Resource, reqparse
from flask import jsonify
from V_2_0.services.userservice import UserService
from V_2_0.services.authservice import AuthService
from . import resources, logger, api
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,set_access_cookies, set_refresh_cookies, unset_jwt_cookies, get_csrf_token)

#api = Api(resources)

parser = reqparse.RequestParser()

parser.add_argument('username', help = 'This field cannot be blank', required = False)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
	def post(self):
		data = parser.parse_args()
		if UserService.getUser(data['username']):
			return {'message': 'User {} already exists'. format(data['username'])}  


		user = {'username': data['username'], 'email': data['email'], 'password': UserService.generate_hash(data['password']), 'active': 0}
		if UserService.addUser(user):
			return {'message': 'User {} create success'. format(data['username'])}



	def get(self):
		return 'registration get'

class UserLogin(Resource):
	def post(self):
		data = parser.parse_args()
		username = data['username']
		logger.info('get User in authview for login:{}'.format(username))
		current_user = UserService.getUser(username)
		if not current_user:
			return {'message': 'User {} doesn\'t exist'.format(username)}

		if AuthService.verify_hash(data['password'], current_user.password):
			access_token = create_access_token(identity = username)
			refresh_token = create_refresh_token(identity = username)

			resp = jsonify({'message': 'Logged in as {}'.format(current_user.username), 'login':'true', 'username':'{}'.format(current_user.username), 'access_csrf': get_csrf_token(access_token), 'refresh_csrf': get_csrf_token(refresh_token)})
			
			logger.info('login massage:{}'.format(resp))

			logger.info('login access_token:{}'.format(access_token))
			logger.info('login refresh_token:{}'.format(refresh_token))
			set_access_cookies(resp, access_token)
			set_refresh_cookies(resp, refresh_token)
			logger.info('login success')

			return resp 

		else:
			logger.info('login success')
			return {'message': 'Wrong credentials'}




	def get(self):
		return 'login get'

class UserLoginbyEmail(Resource):
	def post(self):
		data = parser.parse_args()
		email = data['email']
		logger.info('get User in authview for login:{}'.format(email))
		current_user = UserService.getUserbyEmail(email)
		if not current_user:
			return {'message': 'User {} doesn\'t exist'.format(email)}

		if AuthService.verify_hash(data['password'], current_user.password):
			access_token = create_access_token(identity = email)
			refresh_token = create_refresh_token(identity = email)

			#resp = jsonify({'message': 'Logged in as {}'.format(current_user.username), 'login':'true', 'username':'{}'.format(current_user.username), 'access_csrf': get_csrf_token(access_token), 'refresh_csrf': get_csrf_token(refresh_token)})
			resp = jsonify({'message': 'Logged in as {}'.format(current_user.username), 'login':'true', 'username':'{}'.format(current_user.username), 'access_csrf': get_csrf_token(access_token), 'idToken': get_csrf_token(access_token), 'refresh_csrf': get_csrf_token(refresh_token), 'localId':'{}'.format(current_user.id), 'expiresIn': 60 })			
			logger.info('login massage:{}'.format(resp))

			logger.info('login access_token:{}'.format(access_token))
			logger.info('login refresh_token:{}'.format(refresh_token))
			set_access_cookies(resp, access_token)
			set_refresh_cookies(resp, refresh_token)
			logger.info('login success')

			return resp 

		else:
			logger.info('login success')
			return {'message': 'Wrong credentials'}




	def get(self):
		return 'login get'

class UserLogout(Resource):
#    def post(self):
#	    return 'logout post'
	@jwt_required
	def get(self):
		resp = jsonify({'logout': True})
		unset_jwt_cookies(resp)
		return resp


class TokenRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		logger.info(current_user)
		access_token = create_access_token(identity = current_user)
		resp = jsonify({'refresh': True, 'access_csrf': get_csrf_token(access_token)})
		set_access_cookies(resp, access_token)
		return resp

api.add_resource(UserRegistration, '/registration')

api.add_resource(UserLoginbyEmail, '/login')

api.add_resource(TokenRefresh, '/tokenflash')

api.add_resource(UserLogout, '/logout')

