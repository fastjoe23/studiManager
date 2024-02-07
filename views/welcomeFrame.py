import tkinter as tk
from config import Config
from views.oneStudentFrame import OneStudentWindow


class WelcomeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Daten organisieren
        # Versionsnummer aus config holen:
        configs = Config()
        versionNumber = configs.version

        # schauen ob es in der Datenbank schon lastUsedItems gibt
        recentlyUsedCourses = parent.controller.readLastUsedItemByType("course")
        recentlyUsedStudents = parent.controller.readLastUsedItemByType("student")

        buttonWidth = 30
        buttonHeigth=6
        # Erster Teil: Willkommenstext
        welcome_frame = tk.Frame(self)
        welcome_label = tk.Label(welcome_frame, text=f"Willkommen im StudiManager DHBW Version: {versionNumber}")
        welcome_label.pack(pady=10)
        welcome_frame.grid(row=0, column=0, columnspan=3)

        # Zweiter Teil: Anzeige der zuletzt verwendeten Kurse und Studenten
        recent_frame = tk.Frame(self)

        # Anzeige der Kurse
        recentCoursesFrame = tk.Frame(recent_frame)
        recent_Courses_label = tk.Label(recentCoursesFrame, text="Zuletzt verwendete Kurse:")
        recent_Courses_label.pack(pady=10)
      
        if recentlyUsedCourses is not None:
            for entry in reversed(recentlyUsedCourses.elements):
                course = parent.controller.readCourseById(entry)
                recentCourseButton = tk.Button(recentCoursesFrame, text=course.courseName, command=lambda courseId=entry: self.callCourseManagement(str(courseId)), width=buttonWidth, height=buttonHeigth)
                recentCourseButton.pack(side= tk.LEFT, fill=tk.X, padx=10,pady=10)             
        else:
            # Ausgegraute Knöpfe ohne Funktion anzeigen
            dummyButton = tk.Button(recentCoursesFrame, text="Kurs 1", state=tk.DISABLED, width=buttonWidth, height=buttonHeigth)
            dummyButton.pack(side=tk.LEFT, fill=tk.X, padx=10,pady=10)

            dummyButton = tk.Button(recentCoursesFrame, text="Kurs 2", state=tk.DISABLED, width=buttonWidth, height=buttonHeigth)
            dummyButton.pack(side=tk.LEFT, fill=tk.X, padx=10,pady=10)

            dummyButton = tk.Button(recentCoursesFrame, text="Kurs 3", state=tk.DISABLED, width=buttonWidth, height=buttonHeigth)
            dummyButton.pack(side=tk.LEFT, fill=tk.X, padx=10,pady=10)
        
        recentCoursesFrame.grid(row=0,column=0, columnspan=3)

        # Anzeige der Studenten
        recentStudentsFrame = tk.Frame(recent_frame)
        recent_Students_label = tk.Label(recentStudentsFrame, text="Zuletzt verwendete Studenten:")
        recent_Students_label.pack(pady=10)
      
        if recentlyUsedStudents is not None:
            for entry in reversed(recentlyUsedStudents.elements):
                student = parent.controller.readStudentById(entry)
                recentStudentButton = tk.Button(recentStudentsFrame, text=student.lastName, command=lambda: self.callOneStudentView(student), width=buttonWidth, height=buttonHeigth)
                recentStudentButton.pack(side=tk.LEFT, padx=10)
        else:
            # Ausgegraute Knöpfe ohne Funktion anzeigen
            dummyButton = tk.Button(recentStudentsFrame, text="Student 1", state=tk.DISABLED, width=buttonWidth, height=buttonHeigth)
            dummyButton.pack(side=tk.LEFT, padx=10)

            dummyButton = tk.Button(recentStudentsFrame, text="Student 2", state=tk.DISABLED, width=buttonWidth, height=buttonHeigth)
            dummyButton.pack(side=tk.LEFT, padx=10)

            dummyButton = tk.Button(recentStudentsFrame, text="Student 3", state=tk.DISABLED, width=buttonWidth, height=buttonHeigth)
            dummyButton.pack(side=tk.LEFT, padx=10)
        
        recentStudentsFrame.grid(row=1, column=0, columnspan=3)

        recent_frame.grid(row=1, column=0, columnspan=3, rowspan=8)

        # Dritter Teil: Knöpfe
        button_frame = tk.Frame(self)

        dummyButton = tk.Button(button_frame, text="Alle Kurse", command=self.show_all_courses)
        dummyButton.grid(row=0, column=0, padx=5)

        dummyButton = tk.Button(button_frame, text="Alle Studenten", command=self.show_all_students)
        dummyButton.grid(row=0, column=1, padx=5)

        dummyButton = tk.Button(button_frame, text="Alle Dozenten", command=self.showAllLecturers)
        dummyButton.grid(row=0, column=2, padx=5)

        button_frame.grid(row=9, column=0, columnspan=3, rowspan=8)

        # Gleichmäßige Größe für alle Zeilen und Spalten
        for i in range(10):  # Anzahl der Zeilen
            self.grid_rowconfigure(i, weight=1, uniform="row_uniform")

        for j in range(3):  # Anzahl der Spalten
            self.grid_columnconfigure(j, weight=1, uniform="col_uniform")


    def show_all_courses(self):
        self.master.showAllCourses()
        

    def show_all_students(self):
        self.master.showAllStudents()
        

    def showAllLecturers(self):
        self.master.showAllLecturers()

    def callCourseManagement(self, courseId):
        self.master.switchToCourseManagement(courseId)

    def callOneStudentView(self, student):
        addStudentWindow = OneStudentWindow(self.master, student)
        addStudentWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addStudentWindow.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
