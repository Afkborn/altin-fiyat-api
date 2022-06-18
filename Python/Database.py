import sqlite3 as sql

from Python.Model.Altin import Altin

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


class Database():
    dbName = "database.db"
    dbLoc = fr"db/{dbName}"
    
    def __init__(self) -> None:
        self.createDB()
    
    def createDB(self):
        self.openDB()
        self.im.execute(CREATE_TABLE_ALTIN)
        self.im.execute(CREATE_TABLE_FIYAT)
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
        