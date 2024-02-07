import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class OneAssignmentWindow(tk.Toplevel):
    def __init__(self, parent, assignment=None, student=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Studentische Arbeit bearbeiten" if assignment else "Neue studentische Arbeit hinzufügen")

        # Eingabefelder für die neuen Daten
        self.generalFrame = tk.Frame(self)
        self.generalFrame.pack(pady=10, anchor=tk.W)

        self.typeLabel = tk.Label(self.generalFrame, text="Art der Arbeit:")
        self.typeLabel.grid(row=0, column=0)
        # Dropdown-Menü für den Typ der Arbeit
        assignment_types = ["Bachelorarbeit", "Projektarbeit 1", "Projektarbeit 2"]
        self.assignmentTypeVar = tk.StringVar(self)
        self.assignmentTypeVar.set(assignment_types[0])  # Standardwert
        self.typeDropdown = ttk.Combobox(self.generalFrame, textvariable=self.assignmentTypeVar, values=assignment_types)
        self.typeDropdown.grid(row=0, column=1, pady=10)

        self.topicLabel = tk.Label(self.generalFrame, text="Thema:")
        self.topicEntry = tk.Entry(self.generalFrame, width=50)
        self.topicLabel.grid(row=1, column=0)
        self.topicEntry.grid(row=1, column=1)

        # Erstelle ein LabelFrame für eine bessere Anzeige der Studentendaten
        studentlabelFrame = ttk.LabelFrame(self, text="Studentendaten", padding=10)
        studentlabelFrame.pack(padx=10, pady=10)

        # Anzeige der Studentendaten im LabelFrame
        tk.Label(studentlabelFrame, text="Vorname:").grid(row=0, column=0)
        tk.Label(studentlabelFrame, text="Nachname").grid(row=0, column=1)
        self.studentFirstNameEntry = tk.Entry(studentlabelFrame, width=30)
        self.studentFirstNameEntry.grid(row=1, column= 0)
        self.studentLastNameEntry = tk.Entry(studentlabelFrame, width=30)
        self.studentLastNameEntry.grid(row=1, column= 1)

        # Erstelle ein LabelFrame für eine bessere Anzeige der Gutachterdaten
        lecturerlabelFrame = ttk.LabelFrame(self, text="Gutachterdaten", padding=10)
        lecturerlabelFrame.pack(padx=10, pady=10)

        # Anzeige der lecturerdaten im LabelFrame
        tk.Label(lecturerlabelFrame, text="Vorname:").grid(row=0, column=0)
        tk.Label(lecturerlabelFrame, text="Nachname").grid(row=0, column=1)
        self.lecturerFirstNameEntry = tk.Entry(lecturerlabelFrame, width=30)
        self.lecturerFirstNameEntry.grid(row=1, column= 0)
        self.lecturerLastNameEntry = tk.Entry(lecturerlabelFrame, width=30)
        self.lecturerLastNameEntry.grid(row=1, column= 1)

        self.miscFrame = tk.Frame(self)
        self.miscFrame.pack(pady=10)
        self.gradeLabel = tk.Label(self.miscFrame, text="Note:")
        self.gradeLabel.grid(row=0, column=0)
        self.gradeEntry = tk.Entry(self.miscFrame, width=30)
        self.gradeEntry.grid(row=0, column=1)

        self.dateLabel = tk.Label(self.miscFrame, text="Datum:")
        self.dateLabel.grid(row=1, column=0)
        self.dateEntry = tk.Entry(self.miscFrame, width=30)
        self.dateEntry.grid(row=2, column=0)

        self.timeLabel = tk.Label(self.miscFrame, text="Uhrzeit:")
        self.timeLabel.grid(row=1, column=1)
        self.timeEntry = tk.Entry(self.miscFrame, width=30)
        self.timeEntry.grid(row=2, column=1)

        # Knopf zum Hinzufügen oder Bearbeiten der Arbeit
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        buttonText = "OK" if assignment else "Arbeit hinzufügen"
        addButton = tk.Button(button_frame, text=buttonText, command=lambda: self.addOrEditAssignment(parent, assignment))
        addButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.addOrEditAssignment(parent, assignment))
        self.focus_set()

        # Wenn Assignment vorhanden ist, fülle die Eingabefelder vor
        if assignment:
            if not student:
                # Studenten ermitteln
                student = parent.controller.readStudentById(assignment.studentId)
            
            # Gutachter ermitteln                          
            lecturer = parent.controller.readLecturerById(assignment.lecturerId)

            self.typeDropdown.set(assignment.type)
            self.topicEntry.insert(0, assignment.topic)
            self.studentFirstNameEntry.insert(0, student.firstName)
            self.studentLastNameEntry.insert(0, student.lastName)
            self.lecturerFirstNameEntry.insert(0, lecturer.firstName)
            self.lecturerLastNameEntry.insert(0, lecturer.lastName)
            self.gradeEntry.insert(0, assignment.grade)
            self.dateEntry.insert(0, assignment.date)
            self.timeEntry.insert(0, assignment.time)
        else:
            # ggf.wurde ein Student mitgegeben, dann koennen wir diese Felder fuellen
            if student:
                self.studentFirstNameEntry.insert(0, student.firstName)
                self.studentLastNameEntry.insert(0, student.lastName)


    def addOrEditAssignment(self, parent, assignment):
        try:
            # Hole die Daten aus den Eingabefeldern
            assignmentType = self.typeDropdown.get()
            assignmentTopic = self.topicEntry.get()
            assignmentGrade = float(self.gradeEntry.get().replace(",",".")) if self.gradeEntry.get() else None
            assignmentStudentFirstName = self.studentFirstNameEntry.get()
            assignmentStudentLastName = self.studentLastNameEntry.get()
            assignmentLecturerFirstName = self.lecturerFirstNameEntry.get()
            assignmentLecturerLastName = self.lecturerLastNameEntry.get()
            assignmentDate = self.dateEntry.get()
            assignmentTime = self.timeEntry.get()

            # Ermittele StudentId und LecturerId
            student = parent.controller.readStudentByName(assignmentStudentLastName, assignmentStudentFirstName)
            if not student:
                messagebox.showerror("Student nicht gefunden", f"Student {assignmentStudentFirstName} {assignmentLecturerLastName} ist nicht in der Datenbank.")
                return
            
            lecturer = parent.controller.readLecturerByName(assignmentLecturerLastName, assignmentLecturerFirstName)
            if not lecturer:
                messagebox.showerror("Gutachter nicht gefunden", f"Gutachter {assignmentLecturerFirstName} {assignmentLecturerLastName} ist nicht in der Datenbank.")
                return


            if assignment:
                # Bearbeite die vorhandene Arbeit, wenn assignment vorhanden ist
                parent.controller.updateAssignment(
                    assignment.assignmentId,
                    student.studentId,
                    lecturer.lecturerId,
                    assignmentType,
                    assignmentTopic,
                    assignmentGrade,
                    assignmentDate,
                    assignmentTime
                )
            else:
                # Füge hier die Logik zum Hinzufügen der Arbeit hinzu
                parent.controller.addAssignment(
                    student.studentId,
                    lecturer.lecturerId,
                    assignmentType,
                    assignmentTopic,
                    assignmentGrade,
                    assignmentDate,
                    assignmentTime
                )

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()
        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

            
