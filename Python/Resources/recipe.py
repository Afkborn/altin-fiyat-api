from flask_restful import Resource
from flask import request
from http import HTTPStatus

from ..Database import Database

class AltinRecipe(Resource):
    db = Database()
    def get(self):
        altinList = self.db.getAltinlar()
        dictAltinList = []
        for altin in altinList:
            dictAltinList.append(dict(altin))
        if (len(dictAltinList) == 0):
            return {
                "status": HTTPStatus.NOT_FOUND,
                'message': 'Altin bulunamadı'}
        
        return {
            "status": HTTPStatus.OK,
            'altinlar': dictAltinList}