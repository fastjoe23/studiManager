import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from views.all_students_window import AllStudentsWindow
from views.generate_assignment_list_window import GenerateAssignmentListWindow
from views.generate_course_list_window import GenerateCourseListWindow
from views.one_note_frame import OneNoteWindow
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
        course_namelabel.pack(pady=10)

       # Setzen Sie eine einheitliche Breite für alle Buttons
        button_width = 25

        add_student_button = tk.Button(actions_frame, text="Student zu Kurs hinzufügen", command=lambda: self.add_student_to_course(parent, course_id), width=button_width)
        add_student_button.pack(pady=5)

        send_mail_button = tk.Button(actions_frame, text="Kurs Mail versenden", command=lambda: self.send_course_mail(course_id), width=button_width)
        send_mail_button.pack(pady=5)

        create_evaluation_pdfs_button = tk.Button(actions_frame, text="Begutachtungsformulare erstellen", command=lambda: self.create_evaluation_pdfs(course_id), width=button_width)
        create_evaluation_pdfs_button.pack(pady=5)

        # Horizontaler Abstandhalter
        spacer_horizontal = tk.Label(actions_frame, text=" ")
        spacer_horizontal.pack(pady=30)

        label_helpers = tk.Label(actions_frame,text="Hilfsfunktionen",fg="grey")
        label_helpers.pack(pady=10)

        import_list_button = tk.Button(actions_frame, text="Kurs aus Liste einlesen", command=lambda: self.import_course_from_excel_list(course_id), width=button_width)
        import_list_button.pack(pady=5)

        import_assignment_list_button = tk.Button(actions_frame, text="Arbeiten aus Liste einlesen", command= self.import_assignments_from_list, width=button_width)
        import_assignment_list_button.pack(pady=5)

        generate_list_button = tk.Button(actions_frame, text="Kursliste aus Mail generieren", command=lambda: self.generate_course_list(course_id), width=button_width)
        generate_list_button.pack(pady=5)

        generate_assignment_list_button = tk.Button(actions_frame, text="Blanko Arbeiten Liste generieren", command=lambda: self.generate_assignment_list(course_id), width=button_width)
        generate_assignment_list_button.pack(pady=5)

        # Horizontaler Abstandhalter
        spacer_horizontal = tk.Label(actions_frame, text=" ")
        spacer_horizontal.pack(pady=25)

        close_course_button = tk.Button(actions_frame, text="Kurs verlassen", command=lambda: self.close_course_management(course_id), width=button_width)
        close_course_button.pack(pady=10)        

        # Rechter Teil für Liste der eingeschriebenen Studenten und Notiz
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        students_frame = tk.Frame(right_frame)
        students_frame.pack()

        # Tabelle für die Anzeige der eingeschriebenen Studenten erstellen
        students_label = tk.Label(students_frame, text="Eingeschriebene Studenten:", font=font.Font(family="Arial", size=12, weight="bold"))
        students_label.pack(pady=10)
        self.tree = ttk.Treeview(students_frame, columns=("ID", "Vorname", "Nachname", "E-Mail"), show="headings",height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Vorname", text="Vorname")
        self.tree.heading("Nachname", text="Nachname")
        self.tree.heading("E-Mail", text="E-Mail")


        # Vertikale Scrollbar hinzufügen
        yscrollbar_notes = ttk.Scrollbar(students_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar_notes.set)

        yscrollbar_notes.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", lambda event, course_id=course_id: self.on_student_double_click(event, course_id))

        # Unterer Teil für Notizen
        notes_frame = tk.Frame(right_frame)
        notes_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)

        # Label für Notizen
        notes_label_frame = tk.Frame(notes_frame)
        notes_label_frame.pack(pady=5)
        note_label = tk.Label(notes_label_frame, text="Notizen", font=font.Font(family="Arial", size=12, weight="bold"))
        note_label.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=5)
        self.add_note_button = tk.Button(notes_label_frame, text= "+", command=lambda: self.add_note(course_id))
        self.add_note_button.pack(fill=tk.X, side=tk.RIGHT, padx=10, pady=5)

        # Treeview für Notizen
        self.note_treeview = ttk.Treeview(notes_frame, columns=("note_id", "title", "kurzfassung"), show="headings")
        self.note_treeview.heading("note_id", text="ID")
        self.note_treeview.heading("title", text="Titel")
        self.note_treeview.heading("kurzfassung", text="Kurzfassung")

        
        # Vertikale Scrollbar hinzufügen
        yscrollbar_notes = ttk.Scrollbar(notes_frame, orient='vertical', command=self.note_treeview.yview)
        self.note_treeview.configure(yscrollcommand=yscrollbar_notes.set)

        yscrollbar_notes.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_treeview.pack(fill=tk.BOTH, expand=True)

        # Doppelklick-Ereignis auf den Treeview binden
        self.note_treeview.bind("<Double-1>", lambda event, course_id=course_id: self.on_note_double_click(event, course_id))

        # Notizen hinzufügen
        self.load_course_notes(course_id)
        

        # Lade die Liste der eingeschriebenen Studenten
        self.load_enrolled_students(course_id)

    def on_student_double_click(self, event, course_id):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_student(course_id)

    def on_note_double_click(self, event, course_id):
        self.update_selected_note(course_id)

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

    def import_course_from_csv_list(self, course_id):
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

    def import_course_from_excel_list(self, course_id):
        # Öffne einen Dateidialog, um die Excel-Datei auszuwählen
        excel_path = filedialog.askopenfilename(defaultextension=".xlxs",filetypes=[("Excel Dateien", "*.xlsx")])

        # Überprüfe, ob eine Datei ausgewählt wurde
        if excel_path:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                self.master.controller.import_students_from_excel_into_course(excel_path, course_id)
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
        excel_path = filedialog.askopenfilename(defaultextension=".xlsx",filetypes=[("Excel Dateien", "*.xlsx")])

        # Überprüfe, ob eine Datei ausgewählt wurde
        if excel_path:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                imported_assignments = self.master.controller.import_assignments_from_excel_into_course(excel_path)
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

    def close_course_management(self, course_id):
        
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
    
    def load_course_notes(self, course_id):
        list_of_notes = self.master.controller.read_notes_by_type_and_related_id("course",course_id)

        # Lösche die Tabelle
        for row in self.note_treeview.get_children():
            self.note_treeview.delete(row)

        for note in list_of_notes:
            self.note_treeview.insert("", tk.END, values=(note.note_id, note.note_title, note.note[:50]))



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

    def update_selected_note(self, course_id):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.note_treeview.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return
        
        note_id = self.note_treeview.item(selected_item, "values")[0]
        #Öffne das Fenster zum Hinzufügen oder Ändern einer Notiz
        add_note_window = OneNoteWindow(self.master, "course", course_id, note_id)
        add_note_window.grab_set()
        add_note_window.wait_window()
        
        self.load_course_notes(course_id)

    def add_note(self, course_id):
        add_note_window = OneNoteWindow(self.master, "course", course_id)
        add_note_window.grab_set()
        add_note_window.wait_window()
        
        self.load_course_notes(course_id)


