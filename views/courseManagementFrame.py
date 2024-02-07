import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from views.allStudentsWindow import AllStudentsWindow
from views.generateAssignmentListWindow import GenerateAssignmentListWindow
from views.generateCourseListWindow import GenerateCourseListWindow
from views.oneStudentFrame import OneStudentWindow
from views.sendMailFrame import SendMailWindow
from views.createEvaluationPDFFrame import CreateEvaluationPDFWindow


class CourseManagementFrame(tk.Frame):
    def __init__(self, parent, courseId, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        course = self.master.controller.readCourseById(courseId)

        # lastUsedItems aktualisieren
        self.master.controller.addElementToLastUsedItems("course", courseId)


        # Linker Teil für Aktionen
        actionsFrame = tk.Frame(self)
        actionsFrame.pack(side=tk.LEFT, padx=10, pady=10)

        courseNamelabel = tk.Label(actionsFrame, text=course.courseName, font=font.Font(family="Arial", size=16, weight="bold"))
        courseNamelabel.pack(pady=50)

       # Setzen Sie eine einheitliche Breite für alle Buttons
        button_width = 25

        addStudentButton = tk.Button(actionsFrame, text="Student zu Kurs hinzufügen", command=lambda: self.addStudentToCourse(parent, courseId), width=button_width)
        addStudentButton.pack(pady=5)

        sendMailButton = tk.Button(actionsFrame, text="Kurs Mail versenden", command=lambda: self.sendCourseMail(courseId), width=button_width)
        sendMailButton.pack(pady=5)

        createEvaluationPDFsButton = tk.Button(actionsFrame, text="Begutachtungsformulare erstellen", command=lambda: self.createEvaluationPDFs(courseId), width=button_width)
        createEvaluationPDFsButton.pack(pady=5)

        labelHelpers = tk.Label(actionsFrame,text="Hilfsfunktionen",fg="grey")
        labelHelpers.pack(pady=20)

        importListButton = tk.Button(actionsFrame, text="Kurs aus Liste einlesen", command=lambda: self.importCourseFromList(courseId), width=button_width)
        importListButton.pack(pady=5)

        importAssignmentListButton = tk.Button(actionsFrame, text="Arbeiten aus Liste einlesen", command= self.importAssignmentsFromList, width=button_width)
        importAssignmentListButton.pack(pady=5)

        generateListButton = tk.Button(actionsFrame, text="Kursliste aus Mail generieren", command=lambda: self.generateCourseList(courseId), width=button_width)
        generateListButton.pack(pady=5)

        generateAssignmentListButton = tk.Button(actionsFrame, text="Blanko Arbeiten Liste generieren", command=lambda: self.generateAssignmentList(courseId), width=button_width)
        generateAssignmentListButton.pack(pady=5)

        closeCourseButton = tk.Button(actionsFrame, text="Kurs verlassen", command=self.closeCourseManagement, width=button_width)
        closeCourseButton.pack(pady=25)        

        # Rechter Teil für Liste der eingeschriebenen Studenten
        studentsFrame = tk.Frame(self)
        studentsFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabelle für die Anzeige der eingeschriebenen Studenten erstellen
        self.tree = ttk.Treeview(studentsFrame, columns=("ID", "Vorname", "Nachname", "E-Mail"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Vorname", text="Vorname")
        self.tree.heading("Nachname", text="Nachname")
        self.tree.heading("E-Mail", text="E-Mail")


        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(studentsFrame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", lambda event, courseId=courseId: self.onDoubleClick(event, courseId))

        # Lade die Liste der eingeschriebenen Studenten
        self.loadEnrolledStudents(courseId)

    def onDoubleClick(self, event, courseId):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.updateSelectedStudent(courseId)

    def addStudentToCourse(self, parent, courseId):
        # Logik zum Hinzufügen eines Studenten zum Kurs
         # Öffne das Fenster zum Hinzufügen eines Studenten
        addStudentWindow = AllStudentsWindow(self,courseId)
        addStudentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addStudentWindow.wait_window()

        self.loadEnrolledStudents(courseId)

    def sendCourseMail(self, courseId):
        # Öffnet das Fenster zum Versenden einer Mail an den Kurs
        addSendWindow = SendMailWindow(self, courseId)
        addSendWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addSendWindow.wait_window()

    def createEvaluationPDFs(self, courseId):
        # Öffnet das Fenster zum Erstellen der Begutachtungsformulare für den Kurs
        addCreatePDFWindow = CreateEvaluationPDFWindow(self, courseId)
        addCreatePDFWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addCreatePDFWindow.wait_window()

    def importCourseFromList(self, courseId):
        # Öffne einen Dateidialog, um die CSV-Datei auszuwählen
        csvPath = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV Dateien", "*.csv")])

        # Überprüfe, ob eine Datei ausgewählt wurde
        if csvPath:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                self.master.controller.importStudentsFromCsvIntoCourse(csvPath, courseId)
            except Exception as e:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Importieren", str(e))

        self.loadEnrolledStudents(courseId)

    def generateCourseList(self, courseId):
        # Öffne das Fenster um eine Liste aus Plain-Text zu erzeugen
        addGenerateWindow = GenerateCourseListWindow(self, courseId)
        addGenerateWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addGenerateWindow.wait_window()

    def importAssignmentsFromList(self):
        # Öffne einen Dateidialog, um die CSV-Datei auszuwählen
        csvPath = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV Dateien", "*.csv")])

        # Überprüfe, ob eine Datei ausgewählt wurde
        if csvPath:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                importedAssignments = self.master.controller.importAssignmentsFromCsvIntoCourse(csvPath)
                messagebox.showinfo("Import", f"Es wurden {len(importedAssignments)} Arbeiten erfolgreich importiert.")

            except Exception as e:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Importieren", str(e))

    def generateAssignmentList(self, courseId):
        # erstellt eine csv-Datei in welche die Studenten, ihre Arbeiten und die Gutachter eingetragen werden können
        # Öffne das Fenster um eine Liste aus Plain-Text zu erzeugen
        addGenerateWindow = GenerateAssignmentListWindow(self, courseId)
        addGenerateWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addGenerateWindow.wait_window()

    def closeCourseManagement(self):
        self.master.showMainFrame()

    def loadEnrolledStudents(self,courseId):
        # Lade die Liste der eingeschriebenen Studenten für den aktuellen Kurs
        enrolledStudents = self.master.controller.readAllStudentsByCourseId(courseId)

        # Lösche die Tabelle
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Baue die Tabelle neu auf
        for student in enrolledStudents:
            self.tree.insert("", tk.END, values=(student.studentId, student.firstName, student.lastName, student.email))

    def updateSelectedStudent(self, courseId):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selectedItem = self.tree.selection()

        if not selectedItem:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        studentId = self.tree.item(selectedItem, "values")[0]

        student = self.master.controller.readStudentById(studentId)

        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Studenten
        addStudentWindow = OneStudentWindow(self.master, student)
        addStudentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addStudentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        
        self.loadEnrolledStudents(courseId)