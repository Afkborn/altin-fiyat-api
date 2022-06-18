from flask_restful import Resource
from flask import request
from http import HTTPStatus

from ..AltinTracker import AltinTracker

class AltinRecipe(Resource):
    tracker = AltinTracker()
    def get(self):
        
        jsonAltinList = self.tracker.getAltinJson()
            
        if (len(jsonAltinList) == 0):
            return {
                "status": HTTPStatus.NOT_FOUND,
                'message': 'Altin bulunamadı'}
        
        return {
            "status": HTTPStatus.OK,
            "update_time" : self.tracker.last_get_time,
            'altinlar': jsonAltinList}