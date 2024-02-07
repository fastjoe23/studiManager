import tkinter as tk
from tkinter import ttk, font


class ConfirmationDialogDeleteAssignment(tk.Toplevel):
    def __init__(self, parent, assignment, callback, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Bestätigung")


        self.label = tk.Label(self, text=f"Möchten Sie die {assignment.type}:")
        self.label.pack(pady=10)
        self.label = tk.Label(self, text=assignment.topic, font=font.Font(family="Arial", size=14, weight="bold"))
        self.label.pack(pady=10)
        # Anzeige der Studentendaten
        # Erstelle ein Label_frame für eine bessere Anzeige
        label_frame = ttk.Labelframe(self, text="Studentendaten")
        label_frame.pack(padx=10, pady=10)


        # zugehoerigen Studenten lesen
        student = self.master.master.controller.read_student_by_id(assignment.student_id)

        # Anzeige der Studentendaten im Label_frame
        tk.Label(label_frame, text=f"Vorname: {student.first_name}").pack(anchor="w")
        tk.Label(label_frame, text=f"Nachname: {student.last_name}").pack(anchor="w")

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
