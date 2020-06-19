

mysql_db_username = 'root'

mysql_db_password = ''

mysql_db_name = 'BucketList'

mysql_db_hostname = 'localhost'

class Config():
    DEBUG = True
    PORT = 5001
    HOST = "127.0.0.1"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "SOME SECRET"
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ mysql_db_name +'.db'
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username, DB_PASS=mysql_db_password, DB_ADDR=mysql_db_hostname, DB_NAME=mysql_db_name)
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username, DB_PASS=mysql_db_password, DB_ADDR=mysql_db_hostname, DB_NAME=mysql_db_name)