import tkinter as tk

from studi_manager_model import Assignments, Model, Person, Student, Lecturer, Course, Enrollments
from studi_manager_controller import StudentManagerController
from views.welcome_frame import WelcomeFrame
from views.persons_frame import PersonsFrame
from views.one_person_frame import OnePersonWindow
from views.students_frame import StudentsFrame
from views.one_student_frame import OneStudentWindow
from views.lecturers_frame import LecturersFrame
from views.one_lecturer_frame import OneLecturerWindow
from views.courses_frame import CoursesFrame
from views.one_course_frame import OneCourseWindow
from views.enrollments_frame import EnrollmentsFrame
from views.course_management_frame import CourseManagementFrame
from views.assignments_frame import AssignmentsFrame
from views.email_settings_frame import EmailSettingsWindow

class Main_application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("DHBW Studenten Verwaltung")

        # Setze die Größe des Hauptfensters (Breite x Höhe)
        self.geometry("1200x600")

        # model definieren
        self.model = Model()
        # Controller definieren
        self.controller = StudentManagerController(self.model)

        # Menü erstellen
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        courses_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Kurse", menu=courses_menu)
        courses_menu.add_command(label="Alle Kurse anzeigen", command=self.show_all_courses)
        courses_menu.add_command(label="Neuen Kurs anlegen", command=self.create_new_course)

        students_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Studenten", menu=students_menu)
        students_menu.add_command(label="Alle Studenten anzeigen", command=self.show_all_students)
        students_menu.add_command(label="Neuen Student anlegen", command=self.create_new_student)

        lecturers_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dozenten/Gutachter", menu=lecturers_menu)
        lecturers_menu.add_command(label="Alle Dozenten/Gutachter anzeigen", command=self.show_all_lecturers)
        lecturers_menu.add_command(label="Neuen Dozent/Gutachter anlegen", command=self.create_new_lecturer)

        persons_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datenbestände", menu=persons_menu)
        persons_menu.add_command(label="Alle Personen anzeigen", command=self.show_all_persons)
        persons_menu.add_command(label="Neue Person anlegen", command=self.create_new_person)
        persons_menu.add_command(label="Einschreibungen anzeigen", command=self.show_all_enrollments)
        persons_menu.add_command(label="Stud. Arbeiten anzeigen", command=self.show_all_assignments)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sonstiges", menu=settings_menu)
        settings_menu.add_command(label="Email Einstellungen", command=self.show_settings)



        # Hauptframe erstellen
        self.main_frame = WelcomeFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_frame(self):
        self.main_frame.destroy()
        self.main_frame = WelcomeFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_all_courses(self):
        # hole alle Kurse aus der Datenbank
        self.courses = Course()
        # Ersetze den aktuellen Frame durch den Kurse-Frame
        self.main_frame.destroy()
        self.main_frame = CoursesFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_course(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Kurses
        add_person_window = OneCourseWindow(self)
        add_person_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_person_window.wait_window()

    def show_all_persons(self):
        # hole alle Personen aus der Datenbank
        self.persons = Person()
        # Ersetze den aktuellen Frame durch den Personen-Frame
        self.main_frame.destroy()
        self.main_frame = PersonsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_person(self):
        # Öffne das Fenster zum Hinzufügen einer neuen Person
        add_person_window = OnePersonWindow(self)
        add_person_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_person_window.wait_window()

    def show_all_students(self):
        # hole alle Studenten aus der Datenbank
        self.students = Student()
        # Ersetze den aktuellen Frame durch den Studenten-Frame 
        self.main_frame.destroy()
        # Hier kommt der entsprechende Frame für die Anzeige der Studenten
        self.main_frame = StudentsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_student(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Studenten
        add_student_window = OneStudentWindow(self)
        add_student_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_student_window.wait_window()
    
    def show_all_lecturers(self):
        # hole alle Dozenten aus der Datenbank
        self.lecturers = Lecturer()
        # Ersetze den aktuellen Frame durch den Dozenten-Frame 
        self.main_frame.destroy()
        # Hier kommt der entsprechende Frame für die Anzeige der Dozenten
        self.main_frame = LecturersFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_lecturer(self):
        # Öffne das Fenster zum Hinzufügen eines neuen Dozenten
        add_lecturer_window = OneLecturerWindow(self)
        add_lecturer_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_lecturer_window.wait_window()

    def show_all_enrollments(self):
        # hole alle Kurse aus der Datenbank
        self.enrollments = Enrollments()
        # Ersetze den aktuellen Frame durch den Kurse-Frame
        self.main_frame.destroy()
        self.main_frame = EnrollmentsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_all_assignments(self):
        # hole alle Kurse aus der Datenbank
        self.assignments = Assignments()
        # Ersetze den aktuellen Frame durch den Kurse-Frame
        self.main_frame.destroy()
        self.main_frame = AssignmentsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_settings(self):
        # Öffne das Einstellungen Fenster
        add_settings_window = EmailSettingsWindow(self)
        add_settings_window.grab_set()
        add_settings_window.wait_window()


    def switch_to_course_management(self,course_id):
              # Zum Beispiel, einen neuen Frame erstellen und den alten ersetzen
        self.main_frame.destroy()  # Zerstöre das alte Frame
        self.main_frame = CourseManagementFrame(self, course_id)  # Setze das neue Frame
        self.main_frame.pack(fill=tk.BOTH, expand=True)    


if __name__ == "__main__":
    app = Main_application()

    photo = tk.PhotoImage(file = 'DHBW_Icon.png')
    app.wm_iconphoto(True, photo)
    app.mainloop()
