import tkinter as tk
from tkinter import ttk

class ConfirmationDialogDeleteLecturer(tk.Toplevel):
    def __init__(self, parent, lecturer, callback, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Bestätigung")

        self.label = tk.Label(self, text=f"Möchten Sie den Dozent löschen:")
        self.label.pack(pady=10)
        # Anzeige der Dozentendaten
        # Erstelle ein LabelFrame für eine bessere Anzeige
        labelFrame = ttk.LabelFrame(self, text="Dozentendaten")
        labelFrame.pack(padx=10, pady=10)

        # Anzeige der Dozentendaten im LabelFrame
        tk.Label(labelFrame, text=f"ID: {lecturer.lecturerId}").pack(anchor="w")
        tk.Label(labelFrame, text=f"Vorname: {lecturer.firstName}").pack(anchor="w")
        tk.Label(labelFrame, text=f"Nachname: {lecturer.lastName}").pack(anchor="w")
        tk.Label(labelFrame, text=f"E-Mail: {lecturer.email}").pack(anchor="w")
        tk.Label(labelFrame, text=f"Firma: {lecturer.company}").pack(anchor="w")
        
        self.label = tk.Label(self, text=f"wirklich löschen?")
        self.label.pack(pady=10)

        # Frame für die Buttons erstellen
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Knöpfe zum Bestätigen oder Abbrechen hinzufügen
        confirm_button = tk.Button(button_frame, text="Ja", command=lambda: self.confirmDelete(callback))
        confirm_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Nein", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def confirmDelete(self, callback):
        # Ruft die Bestätigungsfunktion auf und schließt das Dialogfenster
        callback()
        self.destroy()
