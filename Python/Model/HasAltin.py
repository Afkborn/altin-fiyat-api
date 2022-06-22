class HasAltin:
    def __init__(self,
                 id : int = None,
                 code:str = None,
                 alis : float = None,
                 satis : float = None,
                 tarih : float = None,
                 aciklama : str = None,
                 ):
        self.__id = id
        self.__code = code
        self.__alis = float(alis)
        self.__satis = float(satis)
        self.__tarih = tarih
        self.__aciklama = aciklama
        
    def getID(self) -> int:
        return self.__id
    def getCode(self) -> str:
        return self.__code
    def getAlis(self) -> float:
        return self.__alis
    def getSatis(self) -> float:
        return self.__satis
    def getTarih(self) -> float:
        return self.__tarih
    def getAciklama(self):
        return self.__aciklama
    
    def setID(self, id : int) -> None:
        self.__id = id
        
    def __str__(self) -> str:
        return f"""{self.__id} {self.__code} {self.__alis} {self.__satis} {self.__tarih} {self.__aciklama}"""
    
    def __iter__(self):
        for key in self.__dict__:
            keyClear = key.replace("_HasAltin__","")
            yield keyClear, getattr(self, key)