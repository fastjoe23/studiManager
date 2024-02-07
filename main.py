import tkinter as tk

from studentModel import Assignments, Model, Person, Student, Lecturer, Course, Enrollments
from studentController import StudentController
from views.welcomeFrame import WelcomeFrame
from views.personsFrame import PersonsFrame
from views.onePersonFrame import OnePersonWindow
from views.studentsFrame import StudentsFrame
from views.oneStudentFrame import OneStudentWindow
from views.lecturersFrame import LecturersFrame
from views.oneLecturerFrame import OneLecturerWindow
from views.coursesFrame import CoursesFrame
from views.oneCourseFrame import OneCourseWindow
from views.enrollmentsFrame import EnrollmentsFrame
from views.courseManagementFrame import CourseManagementFrame
from views.assignmentsFrame import AssignmentsFrame
from views.emailSettingsFrame import EmailSettingsWindow

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("DHBW Studenten Verwaltung")

        # Setze die Größe des Hauptfensters (Breite x Höhe)
        self.geometry("1200x600")

        # model definieren
        self.model = Model()
        # Controller definieren
        self.controller = StudentController(self.model)

        

        # Menü erstellen
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        courses_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Kurse", menu=courses_menu)
        courses_menu.add_command(label="Alle Kurse anzeigen", command=self.showAllCourses)
        courses_menu.add_command(label="Neuen Kurs anlegen", command=self.createNewCourse)

        students_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Studenten", menu=students_menu)
        students_menu.add_command(label="Alle Studenten anzeigen", command=self.showAllStudents)
        students_menu.add_command(label="Neuen Student anlegen", command=self.createNewStudent)

        lecturers_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dozenten/Gutachter", menu=lecturers_menu)
        lecturers_menu.add_command(label="Alle Dozenten/Gutachter anzeigen", command=self.showAllLecturers)
        lecturers_menu.add_command(label="Neuen Dozent/Gutachter anlegen", command=self.createNewLecturer)

        persons_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datenbestände", menu=persons_menu)
        persons_menu.add_command(label="Alle Personen anzeigen", command=self.showAllPersons)
        persons_menu.add_command(label="Neue Person anlegen", command=self.createNewPerson)
        persons_menu.add_command(label="Einschreibungen anzeigen", command=self.showAllEnrollments)
        persons_menu.add_command(label="Stud. Arbeiten anzeigen", command=self.showAllAssignments)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sonstiges", menu=settings_menu)
        settings_menu.add_command(label="Email Einstellungen", command=self.showSettings)



        # Hauptframe erstellen
        self.mainFrame = WelcomeFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def showMainFrame(self):
        self.mainFrame.destroy()
        self.mainFrame = WelcomeFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def showAllCourses(self):
        # hole alle Kurse aus der Datenbank
        self.courses = Course()
        # Ersetze den aktuellen Frame durch den Kurse-Frame
        self.mainFrame.destroy()
        self.mainFrame = CoursesFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def createNewCourse(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Kurses
        addPersonWindow = OneCourseWindow(self)
        addPersonWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addPersonWindow.wait_window()

    def showAllPersons(self):
        # hole alle Personen aus der Datenbank
        self.persons = Person()
        # Ersetze den aktuellen Frame durch den Personen-Frame
        self.mainFrame.destroy()
        self.mainFrame = PersonsFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def createNewPerson(self):
        # Öffne das Fenster zum Hinzufügen einer neuen Person
        addPersonWindow = OnePersonWindow(self)
        addPersonWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addPersonWindow.wait_window()

    def showAllStudents(self):
        # hole alle Studenten aus der Datenbank
        self.students = Student()
        # Ersetze den aktuellen Frame durch den Studenten-Frame 
        self.mainFrame.destroy()
        # Hier kommt der entsprechende Frame für die Anzeige der Studenten
        self.mainFrame = StudentsFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def createNewStudent(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Studenten
        addPersonWindow = OneStudentWindow(self)
        addPersonWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addPersonWindow.wait_window()
    
    def showAllLecturers(self):
        # hole alle Dozenten aus der Datenbank
        self.lecturers = Lecturer()
        # Ersetze den aktuellen Frame durch den Dozenten-Frame 
        self.mainFrame.destroy()
        # Hier kommt der entsprechende Frame für die Anzeige der Dozenten
        self.mainFrame = LecturersFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def createNewLecturer(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Dozenten
        addPersonWindow = OneLecturerWindow(self)
        addPersonWindow.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        addPersonWindow.wait_window()

    def showAllEnrollments(self):
        # hole alle Kurse aus der Datenbank
        self.enrollments = Enrollments()
        # Ersetze den aktuellen Frame durch den Kurse-Frame
        self.mainFrame.destroy()
        self.mainFrame = EnrollmentsFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def showAllAssignments(self):
        # hole alle Kurse aus der Datenbank
        self.assignments = Assignments()
        # Ersetze den aktuellen Frame durch den Kurse-Frame
        self.mainFrame.destroy()
        self.mainFrame = AssignmentsFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

    def showSettings(self):
        # Öffne das Einstellungen Fenster
        addSettingsWindow = EmailSettingsWindow(self)
        addSettingsWindow.grab_set()
        addSettingsWindow.wait_window()


    def switchToCourseManagement(self,courseId):
              # Zum Beispiel, einen neuen Frame erstellen und den alten ersetzen
        self.mainFrame.destroy()  # Zerstöre das alte Frame
        self.mainFrame = CourseManagementFrame(self, courseId)  # Setze das neue Frame
        self.mainFrame.pack(fill=tk.BOTH, expand=True)    


if __name__ == "__main__":
    app = MainApplication()

    photo = tk.PhotoImage(file = 'DHBW_Icon.png')
    app.wm_iconphoto(True, photo)
    app.mainloop()
