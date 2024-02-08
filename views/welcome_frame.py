import tkinter as tk
from config import Config
from views.one_student_frame import OneStudentWindow


class WelcomeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Daten organisieren
        # Versionsnummer aus config holen:
        configs = Config()
        version_number = configs.version

        # schauen ob es in der Datenbank schon last_used_items gibt
        recently_used_courses = parent.controller.read_last_used_item_by_type("course")
        recently_used_students = parent.controller.read_last_used_item_by_type("student")

        BUTTON_WIDTH = 30
        BUTTON_HEIGHT=6
        # Erster Teil: Willkommenstext
        welcome_frame = tk.Frame(self)
        welcome_label = tk.Label(welcome_frame, text=f"Willkommen im Studi_manager DHBW Version: {version_number}")
        welcome_label.pack(pady=10)
        welcome_frame.grid(row=0, column=0, columnspan=3)

        # Zweiter Teil: Anzeige der zuletzt verwendeten Kurse und Studenten
        recent_frame = tk.Frame(self)

        # Anzeige der Kurse
        recent_courses_frame = tk.Frame(recent_frame)
        recent_courses_label = tk.Label(recent_courses_frame, text="Zuletzt verwendete Kurse:")
        recent_courses_label.pack(pady=10)
      
        if recently_used_courses is not None:
            for entry in reversed(recently_used_courses.elements):
                course = parent.controller.read_course_by_id(entry)
                recent_course_button = tk.Button(recent_courses_frame, text=course.course_name, command=lambda course_id=entry: self.call_course_management(str(course_id)), width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
                recent_course_button.pack(side= tk.LEFT, fill=tk.X, padx=10,pady=10)             
        else:
            # Ausgegraute Knöpfe ohne Funktion anzeigen
            dummy_button = tk.Button(recent_courses_frame, text="Kurs 1", state=tk.DISABLED, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            dummy_button.pack(side=tk.LEFT, fill=tk.X, padx=10,pady=10)

            dummy_button = tk.Button(recent_courses_frame, text="Kurs 2", state=tk.DISABLED, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            dummy_button.pack(side=tk.LEFT, fill=tk.X, padx=10,pady=10)

            dummy_button = tk.Button(recent_courses_frame, text="Kurs 3", state=tk.DISABLED, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            dummy_button.pack(side=tk.LEFT, fill=tk.X, padx=10,pady=10)
        
        recent_courses_frame.grid(row=0,column=0, columnspan=3)

        # Anzeige der Studenten
        recent_students_frame = tk.Frame(recent_frame)
        recent_students_label = tk.Label(recent_students_frame, text="Zuletzt verwendete Studenten:")
        recent_students_label.pack(pady=10)
      
        if recently_used_students is not None:
            for entry in reversed(recently_used_students.elements):
                student = parent.controller.read_student_by_id(entry)
                recent_student_button = tk.Button(recent_students_frame, text=student.last_name + ", " + student.first_name, command=lambda student_id=entry: self.call_one_student_view(parent, str(student_id)), width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
                recent_student_button.pack(side=tk.LEFT, fill=tk.X, padx=10)
        else:
            # Ausgegraute Knöpfe ohne Funktion anzeigen
            dummy_button = tk.Button(recent_students_frame, text="Student 1", state=tk.DISABLED, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            dummy_button.pack(side=tk.LEFT, padx=10)

            dummy_button = tk.Button(recent_students_frame, text="Student 2", state=tk.DISABLED, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            dummy_button.pack(side=tk.LEFT, padx=10)

            dummy_button = tk.Button(recent_students_frame, text="Student 3", state=tk.DISABLED, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            dummy_button.pack(side=tk.LEFT, padx=10)
        
        recent_students_frame.grid(row=1, column=0, columnspan=3)

        recent_frame.grid(row=1, column=0, columnspan=3, rowspan=8)

        # Dritter Teil: Knöpfe
        button_frame = tk.Frame(self)

        dummy_button = tk.Button(button_frame, text="Alle Kurse", command=self.show_all_courses)
        dummy_button.grid(row=0, column=0, padx=5)

        dummy_button = tk.Button(button_frame, text="Alle Studenten", command=self.show_all_students)
        dummy_button.grid(row=0, column=1, padx=5)

        dummy_button = tk.Button(button_frame, text="Alle Dozenten", command=self.show_all_lecturers)
        dummy_button.grid(row=0, column=2, padx=5)

        button_frame.grid(row=9, column=0, columnspan=3, rowspan=8)

        # Gleichmäßige Größe für alle Zeilen und Spalten
        for i in range(10):  # Anzahl der Zeilen
            self.grid_rowconfigure(i, weight=1, uniform="row_uniform")

        for j in range(3):  # Anzahl der Spalten
            self.grid_columnconfigure(j, weight=1, uniform="col_uniform")


    def show_all_courses(self):
        self.master.show_all_courses()

    def show_all_students(self):
        self.master.show_all_students()

    def show_all_lecturers(self):
        self.master.show_all_lecturers()

    def call_course_management(self, course_id):
        self.master.switch_to_course_management(course_id)

    def call_one_student_view(self, parent, student_id):
        student = parent.controller.read_student_by_id(student_id)
        add_student_window = OneStudentWindow(self.master, student)
        add_student_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_student_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird


