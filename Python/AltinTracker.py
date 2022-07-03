from playwright.sync_api import sync_playwright
from time import sleep, time

from Python.globalVar import *
from Python.Model.Altin import Altin
from Python.Model.HasAltin import HasAltin
from Python.Database import Database
import requests
import datetime
from Python.PyTime import *

class AltinTracker:
    PAGE = "https://www.altinkaynak.com/Altin/Kur/Guncel"
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
    altinList : list[Altin] = []
    last_get_time_altinkaynak = 0
    last_get_time_hasaltin = 0
    TIME_INTERVAL_HASALTIN = 20 # kaç saniyede bir kontrol edileceği
    TIME_INTERVAL_ALTINKAYNAK = 6000
    WHILE_TIME_INTERVAL = 5
    
    ALTIN_KAYNAK_TRACK = False
    HAS_ALTIN_TRACK = True
    def __init__(self) -> None:
        self.db = Database()
    
    def getDetailFromTitle(self, title:str):
        title = title.lower()
        if "ayar" in title:
            ayar = title[:2]
        else:
            ayar = None
        if "gr" in title:
            *_, gramajStr, _ = title.split(" ")
            gramaj = float(gramajStr)
        else:
            gramaj = None
        if "saflık derecesi" in title:
            ilk_parentez = title.find("(")
            son_parentez = title.find(")")
            saflıkDerecesiStr = title[ilk_parentez+1:son_parentez]
            saflıkDerecesi = float(saflıkDerecesiStr.replace("saflık derecesi", ""))
        else:
            saflıkDerecesi = None
        return ayar, gramaj, saflıkDerecesi

    def getAltinList(self) -> list[Altin]:
        self.altinList.clear()
        with sync_playwright() as p:
            
            browser = p.chromium.launch()
            
            page = browser.new_page()
            
            page.goto(self.PAGE)
            #wait until class row 2 loaded
            page.wait_for_selector("div[class='row2']")
            padding = page.query_selector("div[class='padding']")
            
            # lastUpdate = padding.query_selector("div[class='lastUpdateContent']")
            # self.lastUpdateDate = lastUpdate.query_selector("span[class='date']").inner_text()
            # self.lastUpdateTime = lastUpdate.query_selector("i[class='time']").inner_text()
            # print(f"Last update: {self.lastUpdateDate} {self.lastUpdateTime}")
    
            parekendeTable = padding.query_selector("table[class='table']")
            tr_list = parekendeTable.query_selector_all("tr")
            for tr in tr_list:
                if (tr.get_attribute("class").startswith("graph")):
                    continue
                title = ""
                allTD = tr.query_selector_all("td")
                for td in allTD:
                    try:
                        title = td.get_attribute("oldtitle").strip()
                        break
                    except:
                        continue
                trDataFlag = tr.get_attribute("data-flag")
                altinAdi = dataFlag[trDataFlag]
                giseAlisStr = tr.query_selector(f"td[id='td{trDataFlag}Buy']").inner_text()
                giseSatisStr = tr.query_selector(f"td[id='td{trDataFlag}Sell']").inner_text()
                ayar, gramaj, saflikDerecesi = self.getDetailFromTitle(title)
                myAltin = Altin(dataFlag=trDataFlag,altinAdi=altinAdi,aciklama=title,gramaj=gramaj,saflik=saflikDerecesi,ayar=ayar,alisFiyati=giseAlisStr,satisFiyati=giseSatisStr,tarih=time())
                self.altinList.append(myAltin)
            browser.close()
            self.last_get_time_altinkaynak = time()
            return self.altinList
    
    
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
        gunler_arası_en_yuksek = meta["yuksek"]
        gunler_arası_en_dusuk = meta["dusuk"]
        for gun in data:
            alis = gun["alis"]
            satis = gun["satis"]
            kayit_tarihi = gun["kayit_tarihi"]
            #'2012-09-10 23:29:32' does not match format '%d-%m-%Y %H:%M:%S'
            dateObj = datetime.datetime.strptime(kayit_tarihi, '%Y-%m-%d %H:%M:%S') 
            gunler_list.append({
                "alis" : alis,
                "satis" : satis,
                "tarih" : dateObj.timestamp()
            })
        return gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list
    
    def getBaslangicWithCode(self, code: str):
        try:
            allTarih = baslangic_tarihi[code]
            return allTarih.split(" ")[0]
        except KeyError:
            return None

    
    def getAllAlisSatisWtihCode(self, code:str):
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
                
                
            if (self.last_get_time_altinkaynak + self.TIME_INTERVAL_ALTINKAYNAK < time() and self.ALTIN_KAYNAK_TRACK):
                print(f" {get_time_command()} Altın Kaynak listesi yenileniyor...")
                altinList = self.getAltinList()
                for altin in altinList:
                    altinID = self.db.addAltin(altin)
                    if (altinID is not None):
                        self.db.addFiyat(altinID, altin.getAlisFiyati(), altin.getSatisFiyati(), time()) 
                print(f" {get_time_command()} Altın Kaynak listesi yenilendi.")
                self.last_get_time_altinkaynak = time()

            sleep(self.WHILE_TIME_INTERVAL)
                
