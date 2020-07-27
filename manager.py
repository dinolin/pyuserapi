import os
from run import db, create_app
#from run import db, getApp
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from passlib.hash import sha512_crypt
from models.roles import RoleModel 
from models.users import UserModel, roles_users


app = create_app(os.getenv('FLASK_CONFIG') or 'default') 
#app=getApp()
manager = Manager(app) 
migrate = Migrate(app, db) 

def make_shell_context(): 
    return dict(app=app, db=db, User=User) 
    
manager.add_command("shell", Shell(make_context=make_shell_context)) 
manager.add_command('db', MigrateCommand) 

@manager.command 
def deploy(): 
    """Run deployment tasks.""" 
    from flask_migrate import init, migrate, upgrade 
    from models.users import UserModel 

    # migrate database to latest revision
    try:init()
    except:pass
    migrate()
    upgrade() 

@manager.command
def dropall():
    db.drop_all()
    print("all tables dropped! remember to delete directory: migrations")

@manager.command
def initrole():
    db.session.add(RoleModel(name="superuser"))
    db.session.add(RoleModel(name="admin"))
    db.session.add(RoleModel(name="editor"))
    db.session.add(RoleModel(name="author"))
    db.session.add(RoleModel(name="user"))
    pwd = os.getenv('FLASK_ADMIN_PWD') or input("Pls input Flask admin pwd:")
    db.session.add(UserModel(username="admin", email="admin@dino.com", password=UserModel.generate_hash(pwd), active=True))
    db.session.commit()
    ins=roles_users.insert().values(user_id="1", role_id="1")
    db.session.execute(ins)
    db.session.commit()
    print ("Roles added!")

if __name__ == '__main__': 
	manager.run() 
