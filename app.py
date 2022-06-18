
from flask import Flask
from flask_restful import Api

from threading import Thread

from Python.Resources.recipe import AltinRecipe
from Python.AltinTracker import AltinTracker

app = Flask(__name__)
api =  Api(app)
api.add_resource(AltinRecipe, '/api/v1/altinlar')

myTracker = AltinTracker()
tracker = Thread(target=myTracker.setTracker)
tracker.start()



