from . import db, logger
from models.roles import RoleModel
from passlib.hash import sha512_crypt
import json


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(120), unique = True, nullable = False)

    email = db.Column(db.String(120), unique = True, nullable = False)

    password = db.Column(db.String(255), nullable = False)

    age = db.Column(db.Integer)

    country = db.Column(db.String(255))

    hobbies = db.Column(db.String(255))

    active = db.Column(db.Boolean())

    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('RoleModel', secondary = roles_users, backref = db.backref('users', lazy = 'dynamic'))

    @classmethod
    def findUser(cls, username):
        logger.info('get User in models:' + username)
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def findUserbyEmail(cls, email):
        logger.info('get User in models:' + email)
        return cls.query.filter_by(email = email).first()

    @classmethod
    def findUserbyId(cls, id):
        logger.info('get User in models:' + id)
        return cls.query.filter_by(id = id).first()


    @classmethod
    def findAllUser(cls):
        return UserModel.query.all()
        #def user_to_json(x):

        #    return {
        #        'id': x.id,
        #        'username': x.username,
        #        'email': x.email,
        #        'password': x.password,
        #        'active': x.active,
        #        'confirmed_at': x.confirmed_at,
        #        'roles': [{list(map(lambda y: role_to_json(y), x.roles))}]
        #    }

        #def role_to_json(x):
        #    return {
        #        'id': x.id,
        #        'name': x.name,
        #        'description': x.description
        #    }
         
        #return {'users': list(map(lambda x: user_to_json(x), UserModel.query.all()))}
        #return dict(UserModel.query.all())

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()

            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}

        except:
            return {'message': 'Something went wrong'}
        
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)
    
    @classmethod
    def addUser(cls, user):
        user_roles = RoleModel.findRole(id = 5)
        new_user = UserModel(
            username = user['username'],
            email = user['email'],
            password = user['password'],
            age = user['age'],
            country = user['country'],
            hobbies = user['hobbies'],
            active = user['active'],
            roles = [user_roles]
            )        

        try:
            new_user.save_to_db()
            #access_token = create_access_token(identity = data['username'])
            #refresh_token = create_refresh_token(identity = data['username'])

            return True
        except:
            return False

    @classmethod
    def deleteUser(cls, id):
        
        try:
            delete_user = cls.query.filter_by(id = id).first()
            delete_user.roles.clear()
            db.session.delete(delete_user)

            db.session.commit()

            return True

        except  Exception as e:
            logger.info(e)

            return False

    @classmethod
    def modifyUser(user):
        return True

    @staticmethod
    def generate_hash(password):
        return sha512_crypt.encrypt(password)


    def save_to_db(self):

        db.session.add(self)

        db.session.commit()

