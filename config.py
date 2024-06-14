import base64
import sqlite3


class Config:
    def __init__(self):
        # Konstante Werte
        self.app_name = "DHBW Student Management System"
        self.version = "0.1"
        self.data_base_name = "studiManagerDatabase.db"
        self.data_base_version = "0.1"
        # Logging
        self.log_level = "DEBUG"
        self.log_format = "%(asctime)s - %(levelname)s - %(module)s -  %(message)s"
        self.log_file_path = "./logs/"
        self.log_file_name = "main.log"
        # Werte für Email-Versand aus DB holen
        self.connect_to_database()
        self.smtp_server = self.get_smtp_server()
        self.smtp_port = self.get_smtp_port()
        self.smtp_username = self.get_smtp_username()
        self.smtp_password = self.get_smtp_password()

    def connect_to_database(self):
        self.conn = sqlite3.connect(self.data_base_name)
        self.cursor = self.conn.cursor()

    def get_smtp_server(self):
        ret_value = self.get_attribute_from_db("SmtpServer")
        return self._decode(ret_value)

    def get_smtp_port(self):
        return self._decode(self.get_attribute_from_db("SmtpPort"))

    def get_smtp_username(self):
        return self._decode(self.get_attribute_from_db("SmtpUsername"))

    def get_smtp_password(self):
        return self._decode(self.get_attribute_from_db("SmtpPassword"))

    def set_smtp_server(self):
        self.save_attribute_to_db("SmtpServer", self._encode(self.smtp_server))

    def set_smtp_port(self):
        self.save_attribute_to_db("SmtpPort", self._encode(self.smtp_port))

    def set_smtp_username(self):
        self.save_attribute_to_db("SmtpUsername", self._encode(self.smtp_username))

    def set_smtp_password(self):
        self.save_attribute_to_db("SmtpPassword", self._encode(self.smtp_password))

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

    def save_config(self):
        self.set_smtp_server()
        self.set_smtp_port()
        self.set_smtp_username()
        self.set_smtp_password()

    def get_attribute_from_db(self, attribute):
        # Daten aus der Datenbank abfragen
        self.cursor.execute(
            "SELECT value FROM config WHERE attribute = ?", (attribute,)
        )

        # Ergebnis abrufen
        result = self.cursor.fetchone()

        # Verbindung schließen
        return result[0] if result else None

    def save_attribute_to_db(self, attribute, value):
        if value:
            self.cursor.execute(
                """
                INSERT OR IGNORE INTO config (attribute, value)
                VALUES (?, ?)
            """,
                (attribute, str(value)),
            )

            self.cursor.execute(
                """
                UPDATE config
                SET value = ?
                WHERE attribute = ?
            """,
                (str(value), attribute),
            )

            # Transaktion bestätigen und Verbindung schließen
            self.conn.commit()

    def __del__(self):
        self.conn.close()
