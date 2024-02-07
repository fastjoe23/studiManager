import tkinter as tk
from tkinter import ttk

class ConfirmationDialogDeleteEnrollment(tk.Toplevel):
    def __init__(self, parent, enrollment, callback, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Bestätigung")

        self.label = tk.Label(self, text=f"Möchten Sie den Studenten:")
        self.label.pack(pady=10)
        # Anzeige der Studentendaten
        # Erstelle ein LabelFrame für eine bessere Anzeige
        labelFrame = ttk.LabelFrame(self, text="Studentendaten")
        labelFrame.pack(padx=10, pady=10)

        # zugehoerigen Kurs lesen
        course = self.master.master.controller.readCourseById(enrollment.courseId)
        # zugehoerigen Studenten lesen
        student = self.master.master.controller.readStudentById(enrollment.studentId)

        # Anzeige der Studentendaten im LabelFrame
        tk.Label(labelFrame, text=f"Vorname: {student.firstName}").pack(anchor="w")
        tk.Label(labelFrame, text=f"Nachname: {student.lastName}").pack(anchor="w")

        self.label = tk.Label(self, text=f"wirklich aus dem Kurs {course.courseName} löschen?")
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
