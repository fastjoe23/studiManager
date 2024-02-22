import tkinter as tk
from tkinter import ttk

class ConfirmationDialogDeleteNote(tk.Toplevel):
    def __init__(self, parent, note, callback, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Bestätigung")

        self.label = tk.Label(self, text="Möchten Sie die Notiz wirklich löschen?")
        self.label.pack(pady=10)

        # Anzeige der Notizendaten im Label_frame
        note_info_frame = ttk.Labelframe(self, text="Notizendaten")
        note_info_frame.pack(padx=10, pady=10)

        # Anzeige der Notizendaten im Label_frame
        tk.Label(note_info_frame, text=f"ID: {note.note_id}").pack(anchor="w")
        tk.Label(note_info_frame, text=f"Titel: {note.note_title}").pack(anchor="w")
        tk.Label(note_info_frame, text=f"Erstelldatum: {note.creation_date}").pack(anchor="w")
        tk.Label(note_info_frame, text=f"Letzte Änderung: {note.last_modification_date}").pack(anchor="w")

        # Frame für die Buttons erstellen
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Knöpfe zum Bestätigen oder Abbrechen hinzufügen
        confirm_button = tk.Button(button_frame, text="Ja", command=lambda: self.confirm_delete(callback))
        confirm_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Nein", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def confirm_delete(self, callback):
        # Ruft die Bestätigungsfunktion auf und schließt das Dialogfenster
        callback()
        self.destroy()
