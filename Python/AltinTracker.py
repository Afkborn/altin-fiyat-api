from playwright.sync_api import sync_playwright
from time import sleep, time

from Python.globalVar import *
from Python.Model.HasAltin import HasAltin
from Python.Database import Database
import requests
import datetime
from Python.PyTime import *

class AltinTracker:
    PAGE_HASALTIN = "https://haremaltin.com/dashboard/ajax/doviz"
    HEADERS_HASALTIN = {
    'Accept': '*/*',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=kvugtp2q0sbkialh160ipm583a',
    'Origin': 'https://haremaltin.com',
    'Referer': 'https://haremaltin.com/canli-piyasalar/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }
    DATA_HASALTIN = {'dil_kodu': 'tr'}
    last_get_time_hasaltin = 0
    TIME_INTERVAL_HASALTIN = 20 # kaç saniyede bir kontrol edileceği
    WHILE_TIME_INTERVAL = 5
    HAS_ALTIN_TRACK = True
    def __init__(self) -> None:
        self.db = Database()

    
    def getHasAltinFromJson(self, myAltin, aciklama):
        dir = myAltin["dir"]
        alis_dir = dir["alis_dir"]
        if (alis_dir == "down"):
            alis_dir = -1
        elif (alis_dir == "up"):
            alis_dir = 1
        else:
            alis_dir = 0
        satis_dir = dir["satis_dir"]
        if (satis_dir == "down"):
            satis_dir = -1
        elif (satis_dir == "up"):
            satis_dir = 1
        else:
            satis_dir = 0

        dusuk = myAltin["dusuk"]
        yuksek = myAltin["yuksek"]
        kapanis = myAltin["kapanis"]
        tarih = myAltin["tarih"] 
        date_obj = datetime.datetime.strptime(tarih, '%d-%m-%Y %H:%M:%S')
        return HasAltin(code=myAltin['code'],alis=myAltin['alis'],satis=myAltin['satis'],tarih=date_obj.timestamp(),aciklama=aciklama,alis_dir=alis_dir,satis_dir=satis_dir,dusuk=dusuk,yuksek=yuksek,kapanis=kapanis)
    
    def getAltinFromHasAltin(self) -> list[HasAltin]:
        hasAltinlar = []
        response = requests.post(self.PAGE_HASALTIN, headers=self.HEADERS_HASALTIN, data=self.DATA_HASALTIN)
        responseJson =  response.json()
        data = responseJson['data']
        for altin, aciklama in altin_tip:
            myAltin = data[altin]
            myHasAltin = self.getHasAltinFromJson(myAltin, aciklama)
            hasAltinlar.append(myHasAltin)
        return hasAltinlar
        
    
    def getAlisSatisWithCodeDateByGun(self, code : str, baslangic:str, bitis:str):
        
        PAGE_HASALTIN_HISTORY = "https://haremaltin.com/ajax/cur/history"
        DATA_HASALTIN = {f"kod" : {code}, 
                        "tarih1" : {baslangic},  #"2012-09-10"
                        "tarih2" : {bitis},  #"2012-09-15"
                        "interval" : "gun",
                        'dil_kodu': "tr"
                        }
        response = requests.post(PAGE_HASALTIN_HISTORY, headers=self.HEADERS_HASALTIN, data=DATA_HASALTIN)
        responseJson = response.json()
        error = responseJson["error"]
        
        if (error != False):
            print("API ERROR")
            return None, None, None
        if (not "data" in responseJson):
            print("DATA ERROR")
            return None, None, None
        gunler_list = []
        data = responseJson["data"]
        meta = responseJson["meta"]
        gunler_arası_en_yuksek = float(meta["yuksek"])
        gunler_arası_en_dusuk = float(meta["dusuk"])
        for gun in data:
            alis = gun["alis"]
            satis = gun["satis"]
            kayit_tarihi = gun["kayit_tarihi"]
            #'2012-09-10 23:29:32' does not match format '%d-%m-%Y %H:%M:%S'
            dateObj = datetime.datetime.strptime(kayit_tarihi, '%Y-%m-%d %H:%M:%S') 
            # self.db.addHasAltinFiyat(hasAltinID=hasAltin.getID(), hasAltinAlis=alis, hasAltinSatis=satis, hasAltinTarih=dateObj.timestamp())
            gunler_list.append({
                "alis" : float(alis),
                "satis" : float(satis),
                "tarih" : dateObj.timestamp()
            })
        return gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list
    
    def getBaslangicWithCode(self, code: str):
        try:
            allTarih = baslangic_tarihi[code]
            return allTarih.split(" ")[0]
        except KeyError:
            return None

    
    def getAllAlisSatisWithCode_fromDB(self, code:str):
        hasAltin = self.db.getHasAltin(code=code)
        baslangic = self.db.getBaslangicTarihHasAltinFiyat_withID(hasAltinID=hasAltin.getID())
        bitis = self.db.getBitisTarihHasAltinFiyat_withID(hasAltinID=hasAltin.getID())
        baslangic = get_time_from_unix(baslangic)
        bitis = get_time_from_unix(bitis)
        gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list = self.db.getAllHasAltinFiyat_withID(hasAltinID=hasAltin.getID())        
        return gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list, baslangic,bitis, code
    
    def getAllAlisSatis(self):
        returnList = []
        for code in baslangic_tarihi.keys():
            gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list, baslangic,bitis, code = self.getAllAlisSatisWithCode_fromDB(code=code)
            returnList.append([gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list, baslangic,bitis,code])
        return returnList
            

    def getAllAlisSatisWithCode_fromWeb(self, code : str):
        baslangic = self.getBaslangicWithCode(code)
        bitis = get_last_date()
        en_dusuk, en_yuksek, data  = self.getAlisSatisWithCodeDateByGun(code,baslangic,bitis)
        return  en_dusuk, en_yuksek, data, baslangic, bitis

        
    
    def setTracker(self):
        while True:
            if (self.last_get_time_hasaltin + self.TIME_INTERVAL_HASALTIN < time() and self.HAS_ALTIN_TRACK):
                print(f" {get_time_command()} Has Altın listesi yenileniyor...")
                altinList = self.getAltinFromHasAltin()
                for altin in altinList:
                    self.db.addHasAltin(altin)
                print(f" {get_time_command()} Has Altın listesi yenilendi.") 
                self.last_get_time_hasaltin = time()
            sleep(self.WHILE_TIME_INTERVAL)
                
