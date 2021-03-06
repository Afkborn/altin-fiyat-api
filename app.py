
# ..
# ..


from flask import Flask
from flask_restful import Api
from threading import Thread
from Python.Resources.recipe import  HasAltinlarRecipe, HasAltinRecipe, Status
from Python.AltinTracker import AltinTracker

app = Flask(__name__)
api =  Api(app)


api.add_resource(HasAltinlarRecipe, '/api/v2/altinlar')
api.add_resource(HasAltinRecipe,'/api/v2/altinlar/<string:code>')
# api.add_resource(Status,"/status")

myTracker = AltinTracker()
tracker = Thread(target=myTracker.setTracker)
tracker.start()



