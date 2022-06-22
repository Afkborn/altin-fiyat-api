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
    TIME_INTERVAL_HASALTIN = 300 # kaç saniyede bir kontrol edileceği
    TIME_INTERVAL_ALTINKAYNAK = 6000
    WHILE_TIME_INTERVAL = 10
    
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
    
    def getAltinFromHasAltin(self) -> list[HasAltin]:
        hasAltinlar = []
        response = requests.post(self.PAGE_HASALTIN, headers=self.HEADERS_HASALTIN, data=self.DATA_HASALTIN)
        responseJson =  response.json()
        data = responseJson['data']

        altin_tip = [
                    ('USDTRY',"Dolar/TL"), ('ALTIN',"Has Altın"), ('OMRUSD',"Umman Riyali/Dolar"),
                    ('USDPURE',"Pure Amerikan Doları"), ('EURTRY',"Euro/TL"), ('ONS',"Ons Altın"),
                    ('USDRUB',"Dolar/Ruble"), ('EURUSD',"Euro/Dolar"), ('USDKG',"1 Kilo Altın (USD)"),
                    ('USDBGN',"Dolar/Bulgar Levası"), ('EURKG',"1 Kilo Altın (Euro)"), ('JPYTRY',"Japon Yeni/TL"),
                    ('AEDUSD',"Birleşik Arap Emirlikleri Dirhemi/Dolar"), ('AYAR14',"14 Ayar Altın"), ('GBPTRY',"İngiliz Sterlini/TL"),
                    ('KWDUSD',"Kuveyt Dinarı/Dolar"), ('AYAR22',"22 Ayar Altın"), ('DKKTRY',"Danimarka Kronu/TL"),
                    ('USDILS',"Dolar/İsrail Şekeli"), ('SEKTRY',"İsveç Kronu/TL"), ('USDMAD',"Dolar/Fas Dirhemi"),
                    ('KULCEALTIN',"Külçe Altın"), ('NOKTRY',"Norveç Kronu/TL"), ('USDQAR',"Dolar/Katar Riyali"),
                    ('XAUXAG',"Altın Spot/Gümüş Spot"), ('CEYREK_YENI',"Çeyrek Altın (Yeni)"), ('CHFTRY',"İsviçre Frangı/TL"),
                    ('JODUSD',"Ürdün Dinarı/Dolar"), ('CEYREK_ESKI',"Çeyrek Altın (Eski)"), ('AUDTRY',"Avustralya Doları/TL"),
                    ('JODTRY',"Ürdün Dinarı/TL"), ('CADTRY',"Kanada Doları/TL"), ('YARIM_YENI',"Yarım Altın (Yeni)"),
                    ('OMRTRY',"Umman Riyali/TL"), ('SARTRY',"Suudi Arabistan Riyali/TL"), ('USDCHF',"Dolar/İsviçre Frangı"),
                    ('YARIM_ESKI',"Yarım Altın (Eski)"), ('AUDUSD',"Avustralya Doları/Dolar"), ('TEK_YENI',"Tam Altın (Yeni)"),
                    ('RUBTRY',"Ruble/TL"), ('USDCAD',"Dolar/Kanada Doları"), ('TEK_ESKI',"Tam Altın (Eski)"),
                    ('BGNTRY',"Bulgar Levası/TL"), ('USDDKK',"Dolar/Danimarka Kronu"), ('ATA_YENI',"Ata Altın (Yeni)"),
                    ('AEDTRY',"Birleşik Arap Emirlikleri Dirhemi/TL"), ('USDSAR',"Dolar/Suudi Arabistan Riyali"), ('ATA_ESKI',"Ata Altın (Eski)"),
                    ('QARTRY',"Katar Riyali/TL"), ('USDSEK',"Dolar/İsveç Kronu"), ('ATA5_YENI',"5 Ata Altın (Yeni) "),
                    ('CNYTRY',"Çin Yuanı/TL"), ('USDJPY',"Dolar/Japon Yeni"), ('ATA5_ESKI',"5 Ata Altın (Eski)"),
                    ('USDNOK',"Dolar/Norveç Kronu"), ('GREMESE_YENI',"Gremese Altın (Yeni)"), ('GBPUSD',"İngiliz Sterlini/Dolar"),
                    ('GREMESE_ESKI',"Gremese Altın (Eski)"), ('GUMUSTRY',"Gümüş"), ('KWDTRY',"Kuveyt Dinari/TL"),
                    ('ILSTRY',"İsrail Şekeli/TL"), ('XAGUSD',"Gümüş Spot/Dolar"), ('GUMUSUSD',"Gümüş/Dolar"),
                    ('MADTRY',"Fas Dirhemi/TL"), ('XPTUSD',"Platin Spot/Dolar"), ('XPDUSD',"Paladyum Spot/Dolar"),
                    ('PLATIN',"Platin/Dolar"), ('PALADYUM',"Paladyum/Dolar")]
        for altin, aciklama in altin_tip:
            myAltin = data[altin]
            
            tarih = myAltin["tarih"] 
            date_obj = datetime.datetime.strptime(tarih, '%d-%m-%Y %H:%M:%S')
            myHasAltin = HasAltin(code=myAltin['code'],alis=myAltin['alis'],satis=myAltin['satis'],tarih=date_obj.timestamp(),aciklama=aciklama)
            hasAltinlar.append(myHasAltin)
        return hasAltinlar
        
    
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
                
