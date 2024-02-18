""" module for window application    """
import tkinter as tk
from studi_manager_controller import StudentManagerController
from studi_manager_model import Model
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

class MainApplication(tk.Tk):
    """Hauptanwendungsklasse für die DHBW-Studentenverwaltung."""

    def __init__(self, *args, **kwargs):
        """Initialisiert die Hauptanwendung."""
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("DHBW Studenten Verwaltung")
        self.geometry("1200x600")

        # Model und Controller initialisieren
        self.model = Model()
        self.controller = StudentManagerController(self.model)

        # Menü erstellen
        self.create_menu()

        # Hauptframe erstellen
        self.main_frame = WelcomeFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        """Erstellt das Menü für die Hauptanwendung."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menüpunkte hinzufügen
        self.add_courses_menu(menubar)
        self.add_students_menu(menubar)
        self.add_lecturers_menu(menubar)
        self.add_persons_menu(menubar)
        self.add_settings_menu(menubar)

    def add_courses_menu(self, menubar):
        """Fügt das Menü für Kurse hinzu."""
        courses_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Kurse", menu=courses_menu)
        courses_menu.add_command(label="Alle Kurse anzeigen", command=self.show_all_courses)
        courses_menu.add_command(label="Neuen Kurs anlegen", command=self.create_new_course)

    def add_students_menu(self, menubar):
        """Fügt das Menü für Studenten hinzu."""
        students_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Studenten", menu=students_menu)
        students_menu.add_command(label="Alle Studenten anzeigen", command=self.show_all_students)
        students_menu.add_command(label="Neuen Student anlegen", command=self.create_new_student)

    def add_lecturers_menu(self, menubar):
        """Fügt das Menü für Dozenten/Gutachter hinzu."""
        lecturers_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dozenten/Gutachter", menu=lecturers_menu)
        lecturers_menu.add_command(label="Alle Dozenten/Gutachter anzeigen", command=self.show_all_lecturers)
        lecturers_menu.add_command(label="Neuen Dozent/Gutachter anlegen", command=self.create_new_lecturer)

    def add_persons_menu(self, menubar):
        """Fügt das Menü für Personen hinzu."""
        persons_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datenbestände", menu=persons_menu)
        persons_menu.add_command(label="Alle Personen anzeigen", command=self.show_all_persons)
        persons_menu.add_command(label="Neue Person anlegen", command=self.create_new_person)
        persons_menu.add_command(label="Einschreibungen anzeigen", command=self.show_all_enrollments)
        persons_menu.add_command(label="Stud. Arbeiten anzeigen", command=self.show_all_assignments)

    def add_settings_menu(self, menubar):
        """Fügt das Menü für Sonstiges hinzu."""
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sonstiges", menu=settings_menu)
        settings_menu.add_command(label="Email Einstellungen", command=self.show_settings)

    def show_all_courses(self):
        """Zeigt alle Kurse an."""
        self.main_frame.destroy()
        self.main_frame = CoursesFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_course(self):
        """Öffnet das Fenster zum Hinzufügen eines neuen Kurses."""
        add_person_window = OneCourseWindow(self)
        add_person_window.grab_set()
        add_person_window.wait_window()

    def show_all_persons(self):
        """Zeigt alle Personen an."""
        self.main_frame.destroy()
        self.main_frame = PersonsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_person(self):
        """Öffnet das Fenster zum Hinzufügen einer neuen Person."""
        add_person_window = OnePersonWindow(self)
        add_person_window.grab_set()
        add_person_window.wait_window()

    def show_all_students(self):
        """Zeigt alle Studenten an."""
        self.main_frame.destroy()
        self.main_frame = StudentsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_student(self):
        """Öffnet das Fenster zum Hinzufügen eines neuen Studenten."""
        add_student_window = OneStudentWindow(self)
        add_student_window.grab_set()
        add_student_window.wait_window()

    def show_all_lecturers(self):
        """Zeigt alle Dozenten/Gutachter an."""
        self.main_frame.destroy()
        self.main_frame = LecturersFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_new_lecturer(self):
        """Öffnet das Fenster zum Hinzufügen eines neuen Dozenten/Gutachters."""
        add_lecturer_window = OneLecturerWindow(self)
        add_lecturer_window.grab_set()
        add_lecturer_window.wait_window()

    def show_all_enrollments(self):
        """Zeigt alle Einschreibungen an."""
        self.main_frame.destroy()
        self.main_frame = EnrollmentsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_all_assignments(self):
        """Zeigt alle Studienarbeiten an."""
        self.main_frame.destroy()
        self.main_frame = AssignmentsFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_settings(self):
        """Öffnet das Einstellungen Fenster."""
        add_settings_window = EmailSettingsWindow(self)
        add_settings_window.grab_set()
        add_settings_window.wait_window()

    def switch_to_course_management(self, course_id):
        """Wechselt zum Kursmanagement-Fenster."""
        self.main_frame.destroy()
        self.main_frame = CourseManagementFrame(self, course_id)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    photo = tk.PhotoImage(file='DHBW_Icon.png')
    app.wm_iconphoto(True, photo)
    app.mainloop()
