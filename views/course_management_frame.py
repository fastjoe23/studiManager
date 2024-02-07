import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from views.all_students_window import AllStudentsWindow
from views.generate_assignment_list_window import GenerateAssignmentListWindow
from views.generate_course_list_window import GenerateCourseListWindow
from views.one_student_frame import OneStudentWindow
from views.send_mail_frame import SendMailWindow
from views.create_evaluation_pdf_frame import CreateEvaluationPDFWindow


class CourseManagementFrame(tk.Frame):
    def __init__(self, parent, course_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        course = self.master.controller.read_course_by_id(course_id)

        # last_used_items aktualisieren
        self.master.controller.add_element_to_last_used_items("course", course_id)


        # Linker Teil für Aktionen
        actions_frame = tk.Frame(self)
        actions_frame.pack(side=tk.LEFT, padx=10, pady=10)

        course_namelabel = tk.Label(actions_frame, text=course.course_name, font=font.Font(family="Arial", size=16, weight="bold"))
        course_namelabel.pack(pady=50)

       # Setzen Sie eine einheitliche Breite für alle Buttons
        button_width = 25

        add_student_button = tk.Button(actions_frame, text="Student zu Kurs hinzufügen", command=lambda: self.add_student_to_course(parent, course_id), width=button_width)
        add_student_button.pack(pady=5)

        send_mail_button = tk.Button(actions_frame, text="Kurs Mail versenden", command=lambda: self.send_course_mail(course_id), width=button_width)
        send_mail_button.pack(pady=5)

        create_evaluation_pdfs_button = tk.Button(actions_frame, text="Begutachtungsformulare erstellen", command=lambda: self.create_evaluation_pdfs(course_id), width=button_width)
        create_evaluation_pdfs_button.pack(pady=5)

        label_helpers = tk.Label(actions_frame,text="Hilfsfunktionen",fg="grey")
        label_helpers.pack(pady=20)

        import_list_button = tk.Button(actions_frame, text="Kurs aus Liste einlesen", command=lambda: self.import_course_from_list(course_id), width=button_width)
        import_list_button.pack(pady=5)

        import_assignment_list_button = tk.Button(actions_frame, text="Arbeiten aus Liste einlesen", command= self.import_assignments_from_list, width=button_width)
        import_assignment_list_button.pack(pady=5)

        generate_list_button = tk.Button(actions_frame, text="Kursliste aus Mail generieren", command=lambda: self.generate_course_list(course_id), width=button_width)
        generate_list_button.pack(pady=5)

        generate_assignment_list_button = tk.Button(actions_frame, text="Blanko Arbeiten Liste generieren", command=lambda: self.generate_assignment_list(course_id), width=button_width)
        generate_assignment_list_button.pack(pady=5)

        close_course_button = tk.Button(actions_frame, text="Kurs verlassen", command=self.close_course_management, width=button_width)
        close_course_button.pack(pady=25)        

        # Rechter Teil für Liste der eingeschriebenen Studenten
        students_frame = tk.Frame(self)
        students_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabelle für die Anzeige der eingeschriebenen Studenten erstellen
        self.tree = ttk.Treeview(students_frame, columns=("ID", "Vorname", "Nachname", "E-Mail"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Vorname", text="Vorname")
        self.tree.heading("Nachname", text="Nachname")
        self.tree.heading("E-Mail", text="E-Mail")


        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(students_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", lambda event, course_id=course_id: self.on_double_click(event, course_id))

        # Lade die Liste der eingeschriebenen Studenten
        self.load_enrolled_students(course_id)

    def on_double_click(self, event, course_id):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_student(course_id)

    def add_student_to_course(self, parent, course_id):
        # Logik zum Hinzufügen eines Studenten zum Kurs
         # Öffne das Fenster zum Hinzufügen eines Studenten
        add_student_window = AllStudentsWindow(self,course_id)
        add_student_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_student_window.wait_window()

        self.load_enrolled_students(course_id)

    def send_course_mail(self, course_id):
        # Öffnet das Fenster zum Versenden einer Mail an den Kurs
        add_send_window = SendMailWindow(self, course_id)
        add_send_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_send_window.wait_window()

    def create_evaluation_pdfs(self, course_id):
        # Öffnet das Fenster zum Erstellen der Begutachtungsformulare für den Kurs
        add_create_pdf_window = CreateEvaluationPDFWindow(self, course_id)
        add_create_pdf_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_create_pdf_window.wait_window()

    def import_course_from_list(self, course_id):
        # Öffne einen Dateidialog, um die CSV-Datei auszuwählen
        csv_path = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV Dateien", "*.csv")])

        # Überprüfe, ob eine Datei ausgewählt wurde
        if csv_path:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                self.master.controller.import_students_from_csv_into_course(csv_path, course_id)
            except Exception as e:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Importieren", str(e))

        self.load_enrolled_students(course_id)

    def generate_course_list(self, course_id):
        # Öffne das Fenster um eine Liste aus Plain-Text zu erzeugen
        add_generate_window = GenerateCourseListWindow(self, course_id)
        add_generate_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_generate_window.wait_window()

    def import_assignments_from_list(self):
        # Öffne einen Dateidialog, um die CSV-Datei auszuwählen
        csv_path = filedialog.askopenfilename(defaultextension=".csv",filetypes=[("CSV Dateien", "*.csv")])

        # Überprüfe, ob eine Datei ausgewählt wurde
        if csv_path:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                imported_assignments = self.master.controller.import_assignments_from_csv_into_course(csv_path)
                messagebox.showinfo("Import", f"Es wurden {len(imported_assignments)} Arbeiten erfolgreich importiert.")

            except Exception as e:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Importieren", str(e))

    def generate_assignment_list(self, course_id):
        # erstellt eine csv-Datei in welche die Studenten, ihre Arbeiten und die Gutachter eingetragen werden können
        # Öffne das Fenster um eine Liste aus Plain-Text zu erzeugen
        add_generate_window = GenerateAssignmentListWindow(self, course_id)
        add_generate_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_generate_window.wait_window()

    def close_course_management(self):
        self.master.show_main_frame()

    def load_enrolled_students(self,course_id):
        # Lade die Liste der eingeschriebenen Studenten für den aktuellen Kurs
        enrolled_students = self.master.controller.read_all_students_by_course_id(course_id)

        # Lösche die Tabelle
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Baue die Tabelle neu auf
        for student in enrolled_students:
            self.tree.insert("", tk.END, values=(student.student_id, student.first_name, student.last_name, student.email))

    def update_selected_student(self, course_id):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Studentendaten aus der ausgewählten Zeile
        student_id = self.tree.item(selected_item, "values")[0]

        student = self.master.controller.read_student_by_id(student_id)

        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Studenten
        add_student_window = OneStudentWindow(self.master, student)
        add_student_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_student_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        
        self.load_enrolled_students(course_id)
