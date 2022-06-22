import sqlite3 as sql

from Python.Model.Altin import Altin
from Python.Model.HasAltin import HasAltin

CREATE_TABLE_ALTIN = f"""CREATE TABLE IF NOT EXISTS altin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataFlag TEXT,
    altinAdi TEXT,
    aciklama TEXT,
    gramaj REAL,
    saflik REAL,
    ayar TEXT,
    alisFiyati REAL,
    satisFiyati REAL,
    tarih REAL
    );"""

CREATE_TABLE_FIYAT = f"""CREATE TABLE IF NOT EXISTS fiyat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    altinID INTEGER,
    alisFiyati REAL,
    satisFiyati REAL,
    tarih REAL
    );"""
    
    
CREATE_TABLE_HAS_ALTIN = f"""CREATE TABLE IF NOT EXISTS hasAltin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    alis REAL,
    satis REAL,
    tarih REAL,
    aciklama TEXT
    );
    """
    
    
CREATE_TABLE_HAS_ALTIN_FIYAT = f"""CREATE TABLE IF NOT EXISTS hasAltinFiyat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        self.im.execute(CREATE_TABLE_ALTIN)
        self.im.execute(CREATE_TABLE_FIYAT)
        
        self.im.execute(CREATE_TABLE_HAS_ALTIN)
        self.im.execute(CREATE_TABLE_HAS_ALTIN_FIYAT)
        
        self.db.commit()
        self.db.close()
    
    def openDB(self):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
    
    def addAltin(self, altin : Altin) -> None:
        self.openDB()
        dbAltin = self.getAltin(altin.getAltinAdi())
        if (dbAltin is not None):
            self.updateAltin(dbAltin.getID(), altin.getAlisFiyati(), altin.getSatisFiyati(), altin.getTarih())
            return dbAltin.getID()
        KEY = f"dataFlag, altinAdi, aciklama, gramaj, saflik, ayar, alisFiyati, satisFiyati, tarih"
        VALUES = f"""
        '{altin.getDataFlag()}',
        '{altin.getAltinAdi()}',
        '{altin.getAciklama()}',
        '{altin.getGramaj()}',
        '{altin.getSaflik()}',
        '{altin.getAyar()}',
        '{altin.getAlisFiyati()}',
        '{altin.getSatisFiyati()}',
        '{altin.getTarih()}'
        """
        self.im.execute(f"INSERT INTO altin ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        last_insert_id = self.im.lastrowid
        altin.setID(last_insert_id)
        self.db.close()
        self.addFiyat(altin.getID(), altin.getAlisFiyati(), altin.getSatisFiyati(), altin.getTarih()) 
        
    def getAltin(self, altinAdi : str) -> Altin:
        self.openDB()
        self.im.execute(f"SELECT * FROM altin WHERE altinAdi = '{altinAdi}'")
        result = self.im.fetchone()
        if result == None:
            return None
        id, dataFlag, altinAdi, aciklama, gramaj, saflik, ayar, alisFiyati, satisFiyati, tarih = result
        return Altin(id, dataFlag, altinAdi, aciklama, gramaj, saflik, ayar, alisFiyati, satisFiyati, tarih)
    
    def getAltinlar(self) -> list[Altin]:
        self.openDB()
        self.im.execute("SELECT * FROM altin")
        result = self.im.fetchall()
        altinlar = []
        for altin in result:
            id, dataFlag, altinAdi, aciklama, gramaj, saflik, ayar, alisFiyati, satisFiyati, tarih = altin
            altinlar.append(Altin(id, dataFlag, altinAdi, aciklama, gramaj, saflik, ayar, alisFiyati, satisFiyati, tarih))
        return altinlar

    def addFiyat(self, altinID : int, alisFiyati : float, satisFiyati : float, tarih : float) -> None:
        self.openDB()
        KEY = f"altinID, alisFiyati, satisFiyati, tarih"
        VALUES = f"""
        '{altinID}',
        '{alisFiyati}',
        '{satisFiyati}',
        '{tarih}'
        """
        self.im.execute(f"INSERT INTO fiyat ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        self.db.close()
    
    def updateAltin(self, altinID : int, alisFiyati : float, satisFiyati : float, tarih : float) -> None:
        self.openDB()
        self.im.execute(f"UPDATE altin SET alisFiyati = {alisFiyati}, satisFiyati = {satisFiyati}, tarih = {tarih} WHERE id = {altinID};")
        self.db.commit()
        self.db.close()
    
    def addHasAltin(self, hasAltin :HasAltin):
        self.openDB()
        dbHasAltin = self.getHasAltin(hasAltin.getCode())
        if (dbHasAltin is not None):
            #bu codea sahip altın varsa  fiyat ekle ve bunun fiyatını güncelle
            self.addHasAltinFiyat(dbHasAltin.getID(), hasAltin.getAlis(), hasAltin.getSatis(), hasAltin.getTarih())
            self.updateHasAltin(dbHasAltin.getID(), hasAltin.getAlis(), hasAltin.getSatis(), hasAltin.getTarih(), aciklama=hasAltin.getAciklama())
            return dbHasAltin.getID()
        KEY = f"code, alis, satis, tarih, aciklama"
        VALUES = f"""
        '{hasAltin.getCode()}',
        '{hasAltin.getAlis()}',
        '{hasAltin.getSatis()}',
        '{hasAltin.getTarih()}',
        '{hasAltin.getAciklama()}'
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
        id, code, alis, satis, tarih, aciklama = result
        return HasAltin(id, code, alis, satis, tarih,aciklama)
    
    def addHasAltinFiyat(self, hasAltinID:int, hasAltinAlis:float, hasAltinSatis:float, hasAltinTarih:float):
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
        
    def updateHasAltin(self, hasAltinID:int, hasAltinAlis:float, hasAltinSatis:float, hasAltinTarih:float, aciklama:str):
        self.openDB()
        self.im.execute(f"UPDATE hasAltin SET alis = {hasAltinAlis}, satis = {hasAltinSatis}, tarih = {hasAltinTarih}, aciklama = '{aciklama}' WHERE id = {hasAltinID};")
        self.db.commit()
        self.db.close()
        
    def getHasAltinlar(self) -> list[HasAltin]:
        self.openDB()
        self.im.execute("SELECT * FROM hasAltin")
        hasAltinlar = []
        for hasAltin in self.im.fetchall():
            id, code, alis, satis, tarih, aciklama = hasAltin
            hasAltinlar.append(HasAltin(id, code, alis, satis, tarih, aciklama))
        return hasAltinlar
    
