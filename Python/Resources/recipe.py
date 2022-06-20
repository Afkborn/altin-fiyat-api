from flask_restful import Resource
from flask import request
from http import HTTPStatus

from ..Database import Database

class AltinKaynakRecipe(Resource):
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
            'data': dictAltinList}
        
class HasAltinRecipe(Resource):
    db = Database()
    def get(self):
        hasAltinList = self.db.getHasAltinlar()
        dictHasAltinList = []   
        for hasAltin in hasAltinList:
            dictHasAltinList.append({
                "code" : hasAltin.getCode(),
                "alis" : hasAltin.getAlis(),
                "satis" : hasAltin.getSatis(),
                "tarih" : hasAltin.getTarih()
            })
        if (len(dictHasAltinList) == 0):
            return {
                "status": HTTPStatus.NOT_FOUND,
                'message': 'Altin bulunamadı'}
        return {
            "status": HTTPStatus.OK,
            "data": dictHasAltinList}