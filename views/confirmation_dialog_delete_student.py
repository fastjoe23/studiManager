import tkinter as tk
from tkinter import ttk

class ConfirmationDialogDeleteStudent(tk.Toplevel):
    def __init__(self, parent, student, callback, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Bestätigung")

        self.label = tk.Label(self, text=f"Möchten Sie den Student :")
        self.label.pack(pady=10)
        # Anzeige der Studentendaten
        # Erstelle ein Label_frame für eine bessere Anzeige
        label_frame = ttk.Labelframe(self, text="Studentendaten")
        label_frame.pack(padx=10, pady=10)

        # Anzeige der Studentendaten im Label_frame
        tk.Label(label_frame, text=f"ID: {student.student_id}").pack(anchor="w")
        tk.Label(label_frame, text=f"Vorname: {student.first_name}").pack(anchor="w")
        tk.Label(label_frame, text=f"Nachname: {student.last_name}").pack(anchor="w")
        tk.Label(label_frame, text=f"E-Mail: {student.email}").pack(anchor="w")
        tk.Label(label_frame, text=f"Firma: {student.company}").pack(anchor="w")
        tk.Label(label_frame, text=f"Mat.-Nr.: {student.mat_number}").pack(anchor="w")
        
        self.label = tk.Label(self, text=f"wirklich löschen?")
        self.label.pack(pady=10)

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
