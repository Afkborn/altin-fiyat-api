



class Altin:
    
    def __init__(self,
                 id : int = None,
                 dataFlag : str = None,
                 altinAdi : str = None,
                 aciklama : str = None,
                 gramaj : float = None,
                 saflik : float = None,
                 ayar : str = None,
                 alisFiyati : float = None,
                 satisFiyati : float = None,
                 tarih : float = None,
    ) -> None:
        if id is None:
            self.__id = None
        else:
            self.__id = id
        self.__dataFlag = dataFlag
        self.__altinAdi = altinAdi
        self.__aciklama = aciklama
        self.__gramaj = gramaj
        self.__saflik = saflik
        self.__ayar = ayar
        self.__alisFiyati = float(alisFiyati)
        self.__satisFiyati = float(satisFiyati)
        self.__tarih = tarih
        
    def getID(self) -> int:
        return self.__id
    def getDataFlag(self) -> str:
        return self.__dataFlag
    def getAltinAdi(self) -> str:
        return self.__altinAdi
    def getAciklama(self) -> str:
        return self.__aciklama
    def getGramaj(self) -> float:
        if (self.__gramaj is None):
            return 0
        return self.__gramaj
    def getSaflik(self) -> float:
        if (self.__saflik is None):
            return 0
        return self.__saflik
    def getAyar(self) -> str:
        return self.__ayar
    def getAlisFiyati(self) -> float:
        if (self.__alisFiyati is None):
            return 0
        return self.__alisFiyati
    def getSatisFiyati(self) -> float:
        if (self.__satisFiyati is None):
            return 0
        return self.__satisFiyati
    def getTarih(self) -> float:
        return self.__tarih
    
    
    def __str__(self) -> str:
        return f"{self.__id} {self.__dataFlag} {self.__altinAdi} {self.__aciklama} {self.__gramaj} {self.__saflik} {self.__ayar} {self.__alisFiyati} {self.__satisFiyati} {self.__tarih}"
    
    def __iter__(self):
        for key in self.__dict__:
            keyClear = key.replace("_Altin__","")
            yield keyClear, getattr(self, key)