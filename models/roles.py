from . import db, logger


class RoleModel(db.Model): 
	__tablename__ = 'roles'

	id = db.Column(db.Integer(), primary_key=True)

	name = db.Column(db.String(80), unique=True)

	description = db.Column(db.String(255))

	@classmethod
	def findRole(cls, id):
		return cls.query.filter_by(id = id).first()

	@classmethod
	def findAllRole(self):
		return RoleModel.query.all()

	@classmethod
	def addRole(role):
		new_role = UserModel(
			name = role['name'],
			description = role['description']
			) 
		try:
			new_role.save_to_db()
			return True
		except:
			return False

	@classmethod
	def deleteRole(id):
		return True

	@classmethod
	def modifyRole(role):
		return True

	def save_to_db(self):
		db.session.add(self)

		db.session.commit()

