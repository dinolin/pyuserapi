from flask_sqlalchemy import SQLAlchemy
import logging
import run
import os,glob
from importlib import import_module

logger = run.getApp().logger
logger.info('Set logger models')

#db = SQLAlchemy()

db = run.db

modules = []
files = glob.glob('./'+__name__.replace('.', '/')+'/*s.py')
for filename in files:
    module_name,ext = os.path.splitext(os.path.basename(filename))
    logger.info('models module load:' + module_name)
    module = import_module(__name__ +'.'+ module_name, __name__)
    
    from . import module