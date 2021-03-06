import sqlite3 as sql
from Python.Model.HasAltin import HasAltin


    
CREATE_TABLE_HAS_ALTIN = f"""CREATE TABLE IF NOT EXISTS hasAltin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    alis REAL,
    satis REAL,
    tarih REAL,
    aciklama TEXT,
    alis_dir INTEGER,
    satis_dir INTEGER,
    dusuk REAL,
    yuksek REAL,
    kapanis REAL
    );
    """
    
    
CREATE_TABLE_HAS_ALTIN_FIYAT = f"""CREATE TABLE IF NOT EXISTS hasAltinFiyat (
    hasAltinID INTEGER,
    alis REAL,
    satis REAL,
    tarih REAL
    );
    """


class Database():
    dbName = "database.db"
    dbLoc = fr"db/{dbName}"
    
    def __init__(self) -> None:
        self.createDB()
    
    def createDB(self):
        self.openDB()        
        self.im.execute(CREATE_TABLE_HAS_ALTIN)
        self.im.execute(CREATE_TABLE_HAS_ALTIN_FIYAT)
        
        self.db.commit()
        self.db.close()
    
    def openDB(self):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()

    def addHasAltin(self, hasAltin :HasAltin):
        self.openDB()
        dbHasAltin = self.getHasAltin(hasAltin.getCode())
        if (dbHasAltin is not None):
            #bu codea sahip altın varsa  fiyat ekle ve bunun fiyatını güncelle
            self.addHasAltinFiyat(dbHasAltin.getID(), hasAltin.getAlis(), hasAltin.getSatis(), hasAltin.getTarih())
            self.updateHasAltin(dbHasAltin.getID(),
                                hasAltin.getAlis(),
                                hasAltin.getSatis(),
                                hasAltin.getTarih(),
                                aciklama=hasAltin.getAciklama(),
                                alis_dir=hasAltin.getAlisDir(),
                                satis_dir=hasAltin.getSatisDir(),
                                dusuk=hasAltin.getDusuk(),
                                yuksek=hasAltin.getYuksek(),
                                kapanis=hasAltin.getKapanis(),
                                )
            return dbHasAltin.getID()
        KEY = f"code, alis, satis, tarih, aciklama, alis_dir, satis_dir, dusuk, yuksek, kapanis"
        VALUES = f"""
        '{hasAltin.getCode()}',
        '{hasAltin.getAlis()}',
        '{hasAltin.getSatis()}',
        '{hasAltin.getTarih()}',
        '{hasAltin.getAciklama()}',
        '{hasAltin.getAlisDir()}',
        '{hasAltin.getSatisDir()}',
        '{hasAltin.getDusuk()}',
        '{hasAltin.getYuksek()}',
        '{hasAltin.getKapanis()}'
        """
        self.im.execute(f"INSERT INTO hasAltin ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        last_insert_id = self.im.lastrowid
        hasAltin.setID(last_insert_id)
        self.db.close()
        self.addHasAltinFiyat(hasAltin.getID(), hasAltin.getAlis(), hasAltin.getSatis(), hasAltin.getTarih())
        
    def getHasAltin(self, code:str):
        self.openDB()
        self.im.execute(f"SELECT * FROM hasAltin WHERE code = '{code}'")
        result = self.im.fetchone()
        if result == None:
            return None
        id, code, alis, satis, tarih, aciklama, alis_dir, satis_dir, dusuk, yuksek, kapanis = result
        return HasAltin(id, code, alis, satis, tarih,aciklama, alis_dir,satis_dir,dusuk, yuksek, kapanis)
    
    def addHasAltinFiyat(self, hasAltinID:int, hasAltinAlis:float, hasAltinSatis:float, hasAltinTarih:float):
        _, alis, satis, _ = self.getLastHasAltinFiyat(hasAltinID=hasAltinID)
        if (alis != None and satis != None):
            if (float(alis) == hasAltinAlis and float(satis) == hasAltinSatis):
                #print(f"zaten var vazgeçtim. {alis} {hasAltinAlis}  {satis} {hasAltinSatis}")
                return None
        self.openDB()
        KEY = f"hasAltinID, alis, satis, tarih"
        VALUES = f"""
        '{hasAltinID}',
        '{hasAltinAlis}',
        '{hasAltinSatis}',
        '{hasAltinTarih}'
        """
        self.im.execute(f"INSERT INTO hasAltinFiyat ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        self.db.close()
    
    def getLastHasAltinFiyat(self, hasAltinID:int):
        self.openDB()
        try:
            self.im.execute(f"SELECT * FROM hasAltinFiyat WHERE hasAltinID = {hasAltinID} ORDER BY tarih DESC")
            result = self.im.fetchone()
            if result == None:
                return None, None,None,None
            hasAltinID, alis, satis, tarih = result
            self.db.close()
            return hasAltinID, alis,satis,tarih
        except:
            return None, None, None, None
         
    def updateHasAltin(self, hasAltinID:int, hasAltinAlis:float, hasAltinSatis:float, hasAltinTarih:float, aciklama:str, alis_dir : int, satis_dir : int, dusuk : float, yuksek : float, kapanis : float):
        self.openDB()
        self.im.execute(f"""UPDATE hasAltin SET alis = {hasAltinAlis},
                                                satis = {hasAltinSatis},
                                                tarih = {hasAltinTarih},
                                                aciklama = '{aciklama}',
                                                alis_dir = {alis_dir},
                                                satis_dir = {satis_dir},
                                                dusuk = {dusuk},
                                                yuksek = {yuksek},
                                                kapanis = {kapanis}
                            WHERE id = {hasAltinID};""")
        self.db.commit()
        self.db.close()
        
    def getHasAltinlar(self) -> list[HasAltin]:
        self.openDB()
        self.im.execute("SELECT * FROM hasAltin")
        hasAltinlar = []
        for hasAltin in self.im.fetchall():
            id, code, alis, satis, tarih, aciklama, alis_dir, satis_dir, dusuk, yuksek, kapanis = hasAltin
            myHasAltin = HasAltin(id, code, alis, satis, tarih, aciklama,alis_dir,satis_dir, dusuk, yuksek, kapanis)
            hasAltinlar.append(myHasAltin)
        return hasAltinlar
    
    def getLowestSatisHasAltinFiyat_withID(self, hasAltinID:int):
        self.openDB()
        self.im.execute(f"SELECT satis FROM hasAltinFiyat WHERE hasAltinID = {hasAltinID} ORDER BY satis ASC LIMIT 1")
        result = self.im.fetchone()
        if result == None:
            return None
        return result[0]
        
    def getHighestSatisHasAltinFiyat_withID(self, hasAltinID:int):
        self.openDB()
        self.im.execute(f"SELECT satis FROM hasAltinFiyat WHERE hasAltinID = {hasAltinID} ORDER BY satis DESC LIMIT 1")
        result = self.im.fetchone()
        if result == None:
            return None
        return result[0]
    
    def getBaslangicTarihHasAltinFiyat_withID(self, hasAltinID:int):
        self.openDB()
        self.im.execute(f"SELECT tarih FROM hasAltinFiyat WHERE hasAltinID = {hasAltinID} ORDER BY tarih ASC LIMIT 1")
        result = self.im.fetchone()
        if result == None:
            return None
        return result[0]
    
    def getBitisTarihHasAltinFiyat_withID(self,hasAltinID:int):
        self.openDB()
        self.im.execute(f"SELECT tarih FROM hasAltinFiyat WHERE hasAltinID = {hasAltinID} ORDER BY satis DESC LIMIT 1")
        result = self.im.fetchone()
        if result == None:
            return None
        return result[0]
    
    def getAllHasAltinFiyat_withID(self, hasAltinID:int):
        self.openDB()
        gunler_list = []
        self.im.execute(f"SELECT * FROM hasAltinFiyat WHERE hasAltinID = {hasAltinID} ORDER BY tarih ASC")
        result = self.im.fetchall()
        if result == None:
            return None, None,None,None
        gunler_arası_en_yuksek = self.getHighestSatisHasAltinFiyat_withID(hasAltinID)
        gunler_arası_en_dusuk = self.getLowestSatisHasAltinFiyat_withID(hasAltinID)
        for gun in result:
            _, alis, satis, tarih = gun
            gunler_list.append({
                "alis" : alis,
                "satis" : satis,
                "tarih" : tarih
            })
        self.db.close()
        return gunler_arası_en_dusuk,gunler_arası_en_yuksek,gunler_list


    
