import base64
import sqlite3

class Config:
    def __init__(self):
        # Konstante Werte
        self.appName = "DHBW Student Management System"
        self.version = "0.1"
        self.dataBaseName = "studiManagerDatabase.db"
        self.dataBaseVersion = "0.1"
        # Werte für Email-Versand aus DB holen
        self.connectToDatabase()
        self.smtpServer = self.getSmtpServer()
        self.smtpPort = self.getSmtpPort()
        self.smtpUsername = self.getSmtpUsername()
        self.smtpPassword = self.getSmtpPassword()

    def connectToDatabase(self):
        self.conn = sqlite3.connect(self.dataBaseName)
        self.cursor = self.conn.cursor()

    def getSmtpServer(self):
        retValue = self.getAttributeFromDB("SmtpServer")
        return self._decode(retValue)

    def getSmtpPort(self):
        return self._decode(self.getAttributeFromDB("SmtpPort"))
    
    def getSmtpUsername(self):
        return self._decode(self.getAttributeFromDB("SmtpUsername"))
    
    def getSmtpPassword(self):
        return self._decode(self.getAttributeFromDB("SmtpPassword"))
    
    def setSmtpServer(self):
        self.saveAttributeToDB("SmtpServer", self._encode(self.smtpServer))

    def setSmtpPort(self):
        self.saveAttributeToDB("SmtpPort", self._encode(self.smtpPort))
    
    def setSmtpUsername(self):
        self.saveAttributeToDB("SmtpUsername", self._encode(self.smtpUsername))
    
    def setSmtpPassword(self):
        self.saveAttributeToDB("SmtpPassword", self._encode(self.smtpPassword))

    def _encode(self, value):
        if value:
            return base64.b64encode(value.encode()).decode()
        else:
            return None
    
    def _decode(self, value):
        if value:
            return base64.b64decode(value.encode()).decode()
        else:
            return None

    def saveConfig(self):
        self.setSmtpServer()
        self.setSmtpPort()
        self.setSmtpUsername()
        self.setSmtpPassword()

    def getAttributeFromDB(self, attribute):
        # Daten aus der Datenbank abfragen
        self.cursor.execute('SELECT value FROM config WHERE attribute = ?', (attribute,))

        # Ergebnis abrufen
        result = self.cursor.fetchone()

        # Verbindung schließen
        return result[0] if result else None
    
    def saveAttributeToDB(self, attribute, value):
        if value:
            self.cursor.execute('''
                INSERT OR IGNORE INTO config (attribute, value)
                VALUES (?, ?)
            ''', (attribute, str(value)))

            self.cursor.execute('''
                UPDATE config
                SET value = ?
                WHERE attribute = ?
            ''', (str(value), attribute))

            # Transaktion bestätigen und Verbindung schließen
            self.conn.commit()

    
    def __del__(self):
        self.conn.close()
    

