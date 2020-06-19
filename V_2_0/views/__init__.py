# coding:utf-8
from flask import Blueprint
from flask_restful import Api
import os,glob
from importlib import import_module
#import logging
import run


resources = Blueprint('api', __name__)
logger = run.getApp().logger
logger.info('Set logger in view')

api = Api(resources)

modules = []
files = glob.glob('./'+__name__.replace('.', '/')+'/*view.py')
for filename in files:
    module_name,ext = os.path.splitext(os.path.basename(filename))
    #print(module_name)
    module = import_module(__name__ +'.'+ module_name, __name__)
    from . import module