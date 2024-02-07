import tkinter as tk

class OneCourseWindow(tk.Toplevel):
    def __init__(self, parent, courseId=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Kurs bearbeiten" if courseId else "Neuen Kurs hinzufügen")

        if courseId:
            # lastUsedItems aktualisieren
            parent.controller.addElementToLastUsedItems("course", courseId)

        # Eingabefelder für die neuen Kursdaten
        self.courseNameLabel = tk.Label(self, text="Kursname:")
        self.courseNameEntry = tk.Entry(self, width=30)

        self.startDateLabel = tk.Label(self, text="Startdatum:")
        self.startDateEntry = tk.Entry(self, width=30)

        # Knopf zum Hinzufügen oder Bearbeiten des Kurses
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        buttonText = "OK" if courseId else "Kurs hinzufügen"
        addButton = tk.Button(button_frame, text=buttonText, command=lambda: self.addOrEditCourse(parent, courseId))
        addButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)



        # Pack die Widgets
        self.courseNameLabel.pack(pady=5)
        self.courseNameEntry.pack(pady=5)

        self.startDateLabel.pack(pady=5)
        self.startDateEntry.pack(pady=5)

        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.addOrEditCourse(parent, courseId))
        self.focus_set()


        # Wenn courseId vorhanden ist, fülle die Eingabefelder vor
        if courseId:
            selectedCourse = parent.controller.readCourseById(courseId)
            self.courseNameEntry.insert(0, selectedCourse.courseName)
            self.startDateEntry.insert(0, selectedCourse.startDate)

    def addOrEditCourse(self, parent, courseId):
        try:
            # Hole die Daten aus den Eingabefeldern
            courseName = self.courseNameEntry.get()
            startDate = self.startDateEntry.get()

            if courseId:
                # Bearbeite den vorhandenen Kurs, wenn courseId vorhanden ist
                parent.controller.updateCourse(courseId, courseName, startDate)
            else:
                # Füge hier die Logik zum Hinzufügen des Kurses hinzu
                parent.controller.addCourse(courseName, startDate)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)
