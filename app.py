
from flask import Flask
from flask_restful import Api
from Python.Resources.recipe import AltinRecipe
app = Flask(__name__)
api =  Api(app)


api.add_resource(AltinRecipe, '/api/v1/altinlar')
