import tkinter as tk
from tkinter import ttk, filedialog

class GenerateAssignmentListWindow(tk.Toplevel):
    def __init__(self, parent, courseId, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Mail Parser")

        # Erklärungstext mit Zeilenumbrüchen
        explanationText = "Wählen Sie den Typ der Arbeit aus und geben Sie einen Speicherort an:"
        explanationLabel = tk.Label(self, text=explanationText)
        explanationLabel.pack(padx=10, pady=10)

        # Dropdown-Menü für den Typ der Arbeit
        assignment_types = ["Bachelorarbeit", "Projektarbeit 1", "Projektarbeit 2"]
        self.assignmentTypeVar = tk.StringVar(self)
        self.assignmentTypeVar.set(assignment_types[0])  # Standardwert
        self.typeDropdown = ttk.Combobox(self, textvariable=self.assignmentTypeVar, values=assignment_types)
        self.typeDropdown.pack(pady=10)

        # Button für die Speicherortauswahl
        browseButton = tk.Button(self, text="Speicherort auswählen", command=self.selectOutputDirectory)
        browseButton.pack(pady=10)

        # Eingabefeld für Dateipfad
        self.savePathEntry = tk.Entry(self, width=40)
        self.savePathEntry.pack(pady=5)

        # Button zum Parsen
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        parseButton = tk.Button(button_frame, text="Liste generieren", command=lambda: self.generateList(courseId))
        parseButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def selectOutputDirectory(self):
        savePath = filedialog.askdirectory()
        if savePath:
            self.savePathEntry.delete(0, tk.END)
            self.savePathEntry.insert(tk.END, savePath)

    def generateList(self, courseId):
        # csv-Liste erzeugen
        # Typ der Liste ermitteln
        type = self.typeDropdown.get()
        if type:
            csvData = self.master.master.controller.generateAssignmentList(type, courseId)

            # Kursinfos beschaffen
            course = self.master.master.controller.readCourseById(courseId)

            # Ergebnis speichern
            savePath = self.savePathEntry.get()
            if savePath:
                self.master.master.controller.saveListToFile(csvData, savePath, type, course.courseName)

        # Schließe das Fenster nach Generierung und Speichern
        self.destroy()

