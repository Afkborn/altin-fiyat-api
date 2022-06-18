from playwright.sync_api import sync_playwright
from time import time

from Python.globalVar import *
from Python.Model.Altin import Altin
import json

class AltinTracker:
    PAGE = "https://www.altinkaynak.com/Altin/Kur/Guncel"
    altinList : list[Altin] = []
    last_get_time = 0
    
    def __init__(self) -> None:
        pass
    
    def getDetailFromTitle(self, title:str):
        #24 Ayar Saf Altın (saflık Derecesi 0.995) 1 GR
        #22 Ayar Altın  (Saflık Derecesi 0.916)
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
            self.last_get_time = time()
            return self.altinList
    
    def writeAltinJson(self,fileName:str) -> str:
        if (len(self.altinList) == 0):
            self.getAltinList()
        jsonObject = {}
        for altin in self.altinList:
            jsonObject[altin.getDataFlag()] = {"altinAdi": altin.getAltinAdi(),
                                               "aciklama": altin.getAciklama(),
                                               "gramaj": altin.getGramaj(),
                                               "saflik": altin.getSaflik(),
                                               "ayar": altin.getAyar(),
                                               "alisFiyati": altin.getAlisFiyati(),
                                               "satisFiyati": altin.getSatisFiyati(),
                                               "tarih": altin.getTarih()
                                               }
        with open(f"{fileName}.json", "w", encoding="utf8") as f:
            json.dump(jsonObject, f, indent=4, ensure_ascii=False)
            
    def getAltinJson(self):
        if (len(self.altinList) == 0):
            self.getAltinList()
        if (self.last_get_time + 600 < time()):
            self.getAltinList()
        jsonObject = {}
        for altin in self.altinList:
            jsonObject[altin.getDataFlag()] = {
                            "altinAdi": altin.getAltinAdi(),
                            "aciklama": altin.getAciklama(),
                            "gramaj": altin.getGramaj(),
                            "saflik": altin.getSaflik(),
                            "ayar": altin.getAyar(),
                            "alisFiyati": altin.getAlisFiyati(),
                            "satisFiyati": altin.getSatisFiyati(),
                            "tarih": altin.getTarih()}
        return jsonObject
            