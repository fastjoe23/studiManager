import base64
import tkinter as tk
from tkinter import ttk
from config import Config

class EmailSettingsWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)

        self.title("Einstellungen")
        # Config Zugriff
        self.config = Config()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        labels = ["SmtpServer", "SmtpPort", "Username", "Passwort"]
        self.entry_vars = {label: tk.StringVar() for label in labels}

        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=7,padx=5)
            ttk.Entry(frame, textvariable=self.entry_vars[label], width=40).grid(row=i, column=1, sticky=(tk.W, tk.E), padx=10, pady=7)

        buttonFrame = ttk.Frame(self, padding="10")
        buttonFrame.grid(row=1, column=0, columnspan=2)
        ttk.Button(buttonFrame, text="Speichern", command=self.save_settings).pack(side=tk.LEFT)
        ttk.Button(buttonFrame, text="Abbrechen", command=self.destroy).pack(side=tk.LEFT, padx=20)

        # Lade vorhandene Einstellungen, falls vorhanden
        self.load_settings()     

    def load_settings(self):
        for label, var in self.entry_vars.items():
            if label == "SmtpServer":
                value = self.config.smtpServer
            elif label == "SmtpPort":
                value = self.config.smtpPort
            elif label == "Username":
                value = self.config.smtpUsername
            elif label == "Passwort":
                value = self.config.smtpPassword
            else:
                print("This should never happen.")                        

            var.set(value)
            #ggf. Eingabefelder vorbelegen
            var.trace_add("write", lambda name, index, mode, var=var, entry=self.entry_vars[label]: entry.set(var.get()))

    def save_settings(self):
            # Daten aus Eingabefeldern in die config-Attribute schreiben
        for label, var in self.entry_vars.items():
            if label == "SmtpServer":
                self.config.smtpServer = var.get()
            elif label == "SmtpPort":
                self.config.smtpPort = var.get()
            elif label == "Username":
                self.config.smtpUsername = var.get()
            elif label == "Passwort":
                self.config.smtpPassword = var.get()
            else:
                print("This should never happen.")

        self.config.saveConfig()
        self.destroy()
        