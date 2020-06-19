from passlib.hash import sha512_crypt
from models.users import UserModel
from models.roles import RoleModel
from . import logger

class AuthService():

	def login(username):
		logger.info('get User in AuthService for login:' + username)
		return UserModel.findUser(username)

	def registration():
		return UserModel.findAllUser()

	def logout():
		return UserModel.deleteUser()

	def flashToken(user):
		return UserModel.modifyUser(user)

	def getToken(user):
		return UserModel.addUser(user)

	def verify_hash(password, hash):
		return sha512_crypt.verify(password, hash)

