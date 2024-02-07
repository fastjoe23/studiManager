import tkinter as tk
from tkinter import ttk

from views.one_assignment_frame import OneAssignmentWindow

class OneStudentWindow(tk.Toplevel):
    def __init__(self, parent, student=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Student bearbeiten" if student else "Neue Student hinzufügen")

        if student:
            # last_used_items aktualisieren
            parent.controller.add_element_to_last_used_items("student", student.student_id)

        # Frame für Eingabefelder
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Gruppe 1: Personalinformationen
        personal_frame = tk.Frame(input_frame)
        personal_frame.pack(side=tk.LEFT, padx=10)

        self.first_name_label = tk.Label(personal_frame, text="Vorname:")
        self.first_name_entry = tk.Entry(personal_frame, width=30)

        self.last_name_label = tk.Label(personal_frame, text="Nachname:")
        self.last_name_entry = tk.Entry(personal_frame, width=30)

        self.email_label = tk.Label(personal_frame, text="E-Mail:")
        self.email_entry = tk.Entry(personal_frame, width=30)

        self.first_name_label.grid(row=0, column=0, pady=5, sticky=tk.E)
        self.first_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.last_name_label.grid(row=1, column=0, pady=5, sticky=tk.E)
        self.last_name_entry.grid(row=1, column=1, pady=5, padx=5)
        self.email_label.grid(row=2, column=0, pady=5, sticky=tk.E)
        self.email_entry.grid(row=2, column=1, pady=5, padx=5)

        # Gruppe 2: Firmeninformationen
        company_frame = tk.Frame(input_frame)
        company_frame.pack(side=tk.LEFT, padx=10)

        self.company_label = tk.Label(company_frame, text="Firma:")
        self.company_entry = tk.Entry(company_frame, width=30)

        self.mat_number_label = tk.Label(company_frame, text="Matrikel_nummer:")
        self.mat_number_entry = tk.Entry(company_frame, width=30)

        self.enrolled_label = tk.Label(company_frame, text="Eingeschrieben:")
        self.enrolled_var = tk.BooleanVar()
        self.enrolled_checkbox = tk.Checkbutton(company_frame, variable=self.enrolled_var)

        self.company_label.grid(row=0, column=0, pady=5, sticky=tk.E)
        self.company_entry.grid(row=0, column=1, pady=5, padx=5)
        self.mat_number_label.grid(row=1, column=0, pady=5, sticky=tk.E)
        self.mat_number_entry.grid(row=1, column=1, pady=5, padx=5)
        self.enrolled_label.grid(row=2, column=0, pady=5, sticky=tk.E)
        self.enrolled_checkbox.grid(row=2, column=1, pady=5, padx=5)

        # wenn Student vorhanden, dann zeige Assignments-Tabelle an
        
        if student:
            #Frame für studentische Arbeiten
            assignment_frame = tk.Frame(self)
            assignment_frame.pack(pady=10)

            self.assignments_label = tk.Label(assignment_frame, text="Studentische Arbeiten:")
            self.assignments_label.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=5)
            self.add_assignment_button = tk.Button(assignment_frame, text= "+", command=lambda: self.add_assignment(parent, student))
            self.add_assignment_button.pack(fill=tk.X, side=tk.RIGHT, padx=10, pady=5)
            # Tree für Arbeiten
            self.tree = ttk.Treeview(self, columns=("ID", "Typ", "Thema",  "Vorname Gutachter", "Nachname Gutachter", "Note", "Datum", "Uhrzeit"), show="headings", height=4)
            self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
            self.tree.column("ID", width=30)
            self.tree.heading("Typ", text="Typ", command=lambda: self.sort_column("Typ"))
            self.tree.column("Typ", width=50)
            self.tree.heading("Thema", text="Thema", command=lambda: self.sort_column("Thema"))
            self.tree.heading("Vorname Gutachter", text="Vorname Gutachter", command=lambda: self.sort_column("Vorname Gutachter"))
            self.tree.heading("Nachname Gutachter", text="Nachname Gutachter", command=lambda: self.sort_column("Nachname Gutachter"))
            self.tree.heading("Note", text="Note", command=lambda: self.sort_column("Note"))
            self.tree.column("Note", width=35)
            self.tree.heading("Datum", text="Datum", command=lambda: self.sort_column("Datum"))
            self.tree.column("Datum", width=60)
            self.tree.heading("Uhrzeit", text="Uhrzeit", command=lambda: self.sort_column("Uhrzeit"))
            self.tree.column("Uhrzeit", width=80)
            # Treeview füllen
            self.refresh_table(parent, student)
            
            self.tree.pack(fill=tk.BOTH, expand=True)

            # Doppelklick-Ereignis auf den Treeview binden
            self.tree.bind("<Double-1>", lambda event: self.on_double_click(parent, student, event))

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        add_button = tk.Button(button_frame, text="OK" if student else "Student hinzufügen",
                              command=lambda: self.add_or_edit_student(parent, student))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_student(parent, student))
        self.focus_set()

        # Wenn Student vorhanden ist, fülle die Eingabefelder vor
        if student:
            self.first_name_entry.insert(0, student.first_name)
            self.last_name_entry.insert(0, student.last_name)
            self.email_entry.insert(0, student.email)
            self.company_entry.insert(0, student.company)
            self.mat_number_entry.insert(0, student.mat_number)
            self.enrolled_var.set(bool(student.enrolled))

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def on_double_click(self, parent, student, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_assignment(parent, student)

    def add_or_edit_student(self, parent, student):
        try:
            # Hole die Daten aus den Eingabefeldern
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()
            company = self.company_entry.get()
            mat_number = self.mat_number_entry.get()
            enrolled = self.enrolled_var.get()

            if student:
                # Bearbeite den vorhandenen Student, wenn Student_data vorhanden ist
                parent.controller.update_student(student.student_id, student.person_id, last_name, first_name, email,
                                                company, mat_number, enrolled)
            else:
                # Füge hier die Logik zum Hinzufügen der Student hinzu
                parent.controller.add_student(last_name, first_name, email, company, mat_number, enrolled)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

    def update_selected_assignment(self, parent, student):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Daten aus der ausgewählten Zeile
        assignment_id = self.tree.item(selected_item, "values")[0]

        assignment = self.master.controller.read_assignment_by_id(assignment_id)


        # Öffne das Fenster zum Hinzufügen oder Ändern eines Assignments
        add_assignment_window = OneAssignmentWindow(self.master, assignment)
        add_assignment_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_assignment_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table(parent, student)  

    def add_assignment(self, parent, student):
        # Öffne das Fenster zum Hinzufügen eines neuen Assignments
        add_assignment_window = OneAssignmentWindow(self.master, assignment=None, student=student)
        add_assignment_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_assignment_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table(parent, student)          
 
    def refresh_table(self, parent, student):
        # Logik zum Aktualisieren der Tabelle
        assignments = parent.controller.read_all_assignments_by_student_id(student.student_id)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for assignment in assignments:
            # zugehoerigen Gutachter lesen
            lecturer = parent.controller.read_lecturer_by_id(assignment.lecturer_id)

            grade_value = assignment.grade if assignment.grade is not None else ''
            #Zeile fuellen 
            self.tree.insert("", tk.END, values=(assignment.assignment_id, assignment.type, assignment.topic, lecturer.first_name, lecturer.last_name, grade_value, assignment.date, assignment.time))

