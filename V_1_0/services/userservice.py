from . import logger
from models.users import UserModel
from passlib.hash import sha512_crypt

class UserService():

	def getUser(username):
		logger.info('get User in userservice:' + username)
		return UserModel.findUser(username)

	def getAllUser():
		return UserModel.findAllUser()

	def deleteUser(id):
		return UserModel.deleteUser(id)

	def modifyUser(user):
		return UserModel.modifyUser(user)

	def addUser(user):
		logger.info('add User in UserService:' + user['username'])
		return UserModel.addUser(user)

	def generate_hash(password):
		return sha512_crypt.encrypt(password)	