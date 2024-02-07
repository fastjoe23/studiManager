import re
import tkinter as tk
from tkinter import scrolledtext, filedialog

class GenerateCourseListWindow(tk.Toplevel):
    def __init__(self, parent, courseId, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Mail Parser")

        # Erklärungstext mit Zeilenumbrüchen
        explanationText = "Kopieren Sie in das folgende Textfeld den Block mit den Email-Abkürzungen\n und den Namen aus einer Test-Mail, welche Sie an den studentischen Verteiler \n 'stud-verteiler+KURS@lehre.dhbw-stuttgart.de' \n gesendet haben.\n  Bspw:\n    wi1234 (Doe, John)\n    wi2345 (Austen, Jane)"
        explanationLabel = tk.Label(self, text=explanationText)
        explanationLabel.pack(padx=10, pady=10)

        # Großes Textfeld mit Scrollbar
        self.textArea = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.textArea.pack(padx=10, pady=10)

        explanationText2 = "Wenn Sie auf den Knopf drücken, wird der Text interpretiert\n und eine Liste für das Einlesen des Kurses erzeugt."
        explanationLabel2 = tk.Label(self,text=explanationText2)
        explanationLabel2.pack(padx=10, pady=10)

        # Button zum Auswählen des Speicherorts
        selectPathButton = tk.Button(self, text="Speicherort auswählen", command=self.selectSavePath)
        selectPathButton.pack(pady=5)

        # Eingabefeld für Dateipfad
        self.savePathEntry = tk.Entry(self, width=40)
        self.savePathEntry.pack(pady=5)

        # Button zum Parsen
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        parseButton = tk.Button(button_frame, text="Parse", command=lambda: self.parseText(courseId))
        parseButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)


    def selectSavePath(self):
        # Funktion zum Auswählen des Speicherorts
        savePath = filedialog.askdirectory()
        if savePath:
            self.savePathEntry.delete(0, tk.END)
            self.savePathEntry.insert(tk.END, savePath)



    def parseText(self, courseId):
        # Funktion zum Parsen des Textes hier implementieren
        textContent = self.textArea.get("1.0", tk.END)
        parsedData = self.master.master.controller.parseFunction(textContent)

        # Kursinfos beschaffen
        course = self.master.master.controller.readCourseById(courseId)
        
        # Ergebnis speichern
        savePath = self.savePathEntry.get()
        self.master.master.controller.saveListToFile(parsedData, savePath, "Kursliste", course.courseName)

        # Schließe das Fenster nach Parsen und Speichern
        self.destroy()

    