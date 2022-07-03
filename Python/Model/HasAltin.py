class HasAltin:
    def __init__(self,
                 id : int = None,
                 code:str = None,
                 alis : float = None,
                 satis : float = None,
                 tarih : float = None,
                 aciklama : str = None,
                 alis_dir : int = 0,
                 satis_dir : int = 0,
                 dusuk : float = None,
                 yuksek : float = None,
                 kapanis : float = None,
                 ):
        self.__id = id
        self.__code = code
        self.__alis = float(alis)
        self.__satis = float(satis)
        self.__tarih = tarih
        self.__aciklama = aciklama
        self.__alis_dir = alis_dir
        self.__satis_dir = satis_dir
        self.__dusuk = dusuk
        self.__yuksek = yuksek
        self.__kapanis = kapanis
        
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
    def getAlisDir(self):
        return self.__alis_dir
    def getSatisDir(self):
        return self.__satis_dir
    def getDusuk(self):
        return self.__dusuk
    def getYuksek(self):
        return self.__yuksek
    def getKapanis(self):
        return self.__kapanis
    def getBaslangicTarihi(self):
        return self.__baslangicTarihi
    
    def setID(self, id : int) -> None:
        self.__id = id
        
    def __str__(self) -> str:
        return f"""{self.__id} {self.__code} {self.__alis} {self.__satis} {self.__tarih} {self.__aciklama}"""
    
    def __iter__(self):
        for key in self.__dict__:
            keyClear = key.replace("_HasAltin__","")
            yield keyClear, getattr(self, key)