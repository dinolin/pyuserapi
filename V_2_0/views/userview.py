from flask_restful import Resource, reqparse
from flask import jsonify
from . import resources, logger, api
from V_2_0.services.userservice import UserService
from V_2_0.services.fakeservice import FakeService
from V_2_0.viewmodels.userschema import UserSchema, RoleSchema
from flask_jwt_extended import jwt_required


parser = reqparse.RequestParser()

parser.add_argument('id', help = 'This field cannot be blank', required = False)
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = False)
parser.add_argument('password', help = 'This field cannot be blank', required = False)
parser.add_argument('age', help = 'This field cannot be blank', required = False)
parser.add_argument('country', help = 'This field cannot be blank', required = False)
parser.add_argument('hobbies', help = 'This field cannot be blank', required = False)
parser.add_argument('role', help = 'This field cannot be blank', required = False)

class GetUser(Resource):
#    def post(self):
#	    return 'registration post'
	@jwt_required
	def get(self, username):
		logger.info('Get User in view:' + username)
		user = UserService.getUser(username)

		if not user:
			return {'message': 'User {} doesn\'t exist'.format(username)}

		userview = UserSchema()
		return jsonify({'user': userview.dump(user)})

class GetUserbyId(Resource):
#    def post(self):
#	    return 'registration post'
	@jwt_required
	def get(self, id):
		logger.info('Get User in view:' + id)
		user = UserService.getUserbyId(id)

		if not user:
			return {'message': 'User {} doesn\'t exist'.format(id)}

		userview = UserSchema()
		return jsonify({'user': userview.dump(user)})

class GetAllUser(Resource):
	@jwt_required
	def post(self):
		users = UserService.getAllUser()
		usersview = UserSchema(many = True)
		return jsonify({'users': usersview.dump(users)})


class AddUser(Resource):
	#@jwt_required
	def post(self):
		data = parser.parse_args()
		logger.info(data)
		if UserService.getUser(data['username']):
			return {'message': 'User {} already exists'. format(data['username'])}  


		user = {'username': data['username'], 'email': data['email'], 'password': UserService.generate_hash(data['password']), 'age': data['age'], 'country': data['country'], 'hobbies': data['hobbies'],'active': 0, 'roles': data['role']}
		logger.info(user)
		
		if UserService.addUser(user):
			return {'message': 'User {} create success'. format(data['username'])}

class GetAllEmployee(Resource):
	@jwt_required
	def post(self):
		return FakeService.getFakeEmployee()
		
class DeleteUser(Resource):

	@jwt_required
	def delete(self):
		data = parser.parse_args()
		#id = ''

		#if UserService.getUser(data['username']):
		#	id = 
		#else:
		#	return {'message': 'User {} is not exists'. format(data['username'])}  

		if UserService.deleteUser(data['id']):
			return {'message': 'User {} deleted '. format(data['username'])}
		else:
			return {'message': 'User {} delete fail '. format(data['username'])}

api.add_resource(AddUser, '/adduser')

api.add_resource(GetUser, '/getuser', '/getuser/<username>')

api.add_resource(GetUserbyId, '/getuserbyid', '/getuserbyid/<id>')

api.add_resource(GetAllUser, '/getalluser')

api.add_resource(DeleteUser, '/deleteuser')

api.add_resource(GetAllEmployee, '/getallemployee')

