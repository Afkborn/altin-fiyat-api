from flask_restful import Resource
from flask import request
from http import HTTPStatus

from ..Database import Database
from ..AltinTracker import AltinTracker

    
class HasAltinlarRecipe(Resource):
    db = Database()
    def get(self):
        hasAltinList = self.db.getHasAltinlar()
        dictHasAltinList = []   
        for hasAltin in hasAltinList:
            dictHasAltinList.append({
                "code" : hasAltin.getCode(),
                "alis" : hasAltin.getAlis(),
                "satis" : hasAltin.getSatis(),
                "tarih" : hasAltin.getTarih(),
                "aciklama" : hasAltin.getAciklama(),
                'alis_dir' : hasAltin.getAlisDir(),
                'satis_dir' : hasAltin.getSatisDir(),
                "dusuk" : hasAltin.getDusuk(),
                "yuksek" : hasAltin.getYuksek(),
                "kapanis" : hasAltin.getKapanis()
            })
        if (len(dictHasAltinList) == 0):
            return {
                "status": HTTPStatus.NOT_FOUND,
                'message': 'Altin bulunamadı'}
        return {
            "status": HTTPStatus.OK,
            
            "data": dictHasAltinList}

class HasAltinRecipe(Resource):
    db = Database()
    tracker = AltinTracker()
    gecmisZamanliVeri = tracker.getAllAlisSatis()
    def get(self,code):
        dictAltin = []
        hasAltin = self.db.getHasAltin(code=code)
        if hasAltin == None:
            return {
                "status": HTTPStatus.NOT_FOUND,
                'message': 'Değerli bulunamadı'}
        dictAltin.append({
                "code" : hasAltin.getCode(),
                "alis" : hasAltin.getAlis(),
                "satis" : hasAltin.getSatis(),
                "tarih" : hasAltin.getTarih(),
                "aciklama" : hasAltin.getAciklama(),
                'alis_dir' : hasAltin.getAlisDir(),
                'satis_dir' : hasAltin.getSatisDir(),
                "dusuk" : hasAltin.getDusuk(),
                "yuksek" : hasAltin.getYuksek(),
                "kapanis" : hasAltin.getKapanis()
        })
        return {
            "status": HTTPStatus.OK,
            'data': dictAltin}
        
    def post(self,code):
        data = request.args
        try:
            allData = data["all"]
            if (allData == 1 or allData == "1"):
                allData = True
            else:
                allData = False
        except:
            allData = False
        if (allData):
            # en_dusuk, en_yuksek, data, t1, t2, code = self.tracker.getAllAlisSatisWithCode_fromDB(code)
            for index, (*_, dataCode) in enumerate(self.gecmisZamanliVeri):
                if (code == dataCode):
                    en_dusuk, en_yuksek, data, t1, t2, code = self.gecmisZamanliVeri[index]
        else:
            try:
                t1 = data["t1"]
                t2 = data["t2"]
            except:
                return {
                    "status": HTTPStatus.BAD_REQUEST,
                    'message': 'Tarih bilgisi gerekli (t1,t2) gerekli'}
            en_dusuk, en_yuksek, data = self.tracker.getAlisSatisWithCodeDateByGun(code,t1,t2)
        if (en_dusuk == None or en_yuksek == None or data == None):
                return {
                    "status": HTTPStatus.BAD_REQUEST,
                    'message': 'Veri Yok'}
        return {
            "status" : HTTPStatus.OK,
            "code" : code,
            "tarih_baslangic" : t1,
            "tarih_bitis" : t2,
            "en_dusuk" : en_dusuk,
            "en_yuksek" : en_yuksek,
            "alis_satis_gunler" : data
        }
        
class Status(Resource):
    def get(self):
        return {
            "status": HTTPStatus.OK
        }