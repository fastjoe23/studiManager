import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class OneAssignmentWindow(tk.Toplevel):
    def __init__(self, parent, assignment=None, student=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Studentische Arbeit bearbeiten" if assignment else "Neue studentische Arbeit hinzufügen")

        # Eingabefelder für die neuen Daten
        self.general_frame = tk.Frame(self)
        self.general_frame.pack(pady=10, anchor=tk.W)

        self.type_label = tk.Label(self.general_frame, text="Art der Arbeit:")
        self.type_label.grid(row=0, column=0)
        # Dropdown-Menü für den Typ der Arbeit
        assignment_types = ["Bachelorarbeit", "Projektarbeit 1", "Projektarbeit 2"]
        self.assignment_type_var = tk.StringVar(self)
        self.assignment_type_var.set(assignment_types[0])  # Standardwert
        self.type_dropdown = ttk.Combobox(self.general_frame, textvariable=self.assignment_type_var, values=assignment_types)
        self.type_dropdown.grid(row=0, column=1, pady=10)

        self.topic_label = tk.Label(self.general_frame, text="Thema:")
        self.topic_entry = tk.Entry(self.general_frame, width=50)
        self.topic_label.grid(row=1, column=0)
        self.topic_entry.grid(row=1, column=1)

        # Erstelle ein Label_frame für eine bessere Anzeige der Studentendaten
        studentlabel_frame = ttk.Labelframe(self, text="Studentendaten", padding=10)
        studentlabel_frame.pack(padx=10, pady=10)

        # Anzeige der Studentendaten im Label_frame
        tk.Label(studentlabel_frame, text="Vorname:").grid(row=0, column=0)
        tk.Label(studentlabel_frame, text="Nachname").grid(row=0, column=1)
        self.student_first_name_entry = tk.Entry(studentlabel_frame, width=30)
        self.student_first_name_entry.grid(row=1, column= 0)
        self.student_last_name_entry = tk.Entry(studentlabel_frame, width=30)
        self.student_last_name_entry.grid(row=1, column= 1)

        # Erstelle ein Label_frame für eine bessere Anzeige der Gutachterdaten
        lecturerlabel_frame = ttk.Labelframe(self, text="Gutachterdaten", padding=10)
        lecturerlabel_frame.pack(padx=10, pady=10)

        # Anzeige der lecturerdaten im Label_frame
        tk.Label(lecturerlabel_frame, text="Vorname:").grid(row=0, column=0)
        tk.Label(lecturerlabel_frame, text="Nachname").grid(row=0, column=1)
        self.lecturer_first_name_entry = tk.Entry(lecturerlabel_frame, width=30)
        self.lecturer_first_name_entry.grid(row=1, column= 0)
        self.lecturer_last_name_entry = tk.Entry(lecturerlabel_frame, width=30)
        self.lecturer_last_name_entry.grid(row=1, column= 1)

        self.misc_frame = tk.Frame(self)
        self.misc_frame.pack(pady=10)
        self.grade_label = tk.Label(self.misc_frame, text="Note:")
        self.grade_label.grid(row=0, column=0)
        self.grade_entry = tk.Entry(self.misc_frame, width=30)
        self.grade_entry.grid(row=0, column=1)

        self.date_label = tk.Label(self.misc_frame, text="Datum:")
        self.date_label.grid(row=1, column=0)
        self.date_entry = tk.Entry(self.misc_frame, width=30)
        self.date_entry.grid(row=2, column=0)

        self.time_label = tk.Label(self.misc_frame, text="Uhrzeit:")
        self.time_label.grid(row=1, column=1)
        self.time_entry = tk.Entry(self.misc_frame, width=30)
        self.time_entry.grid(row=2, column=1)

        # Knopf zum Hinzufügen oder Bearbeiten der Arbeit
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if assignment else "Arbeit hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_assignment(parent, assignment))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_assignment(parent, assignment))
        self.focus_set()

        # Wenn Assignment vorhanden ist, fülle die Eingabefelder vor
        if assignment:
            if not student:
                # Studenten ermitteln
                student = parent.controller.read_student_by_id(assignment.student_id)
            
            # Gutachter ermitteln                          
            lecturer = parent.controller.read_lecturer_by_id(assignment.lecturer_id)

            self.type_dropdown.set(assignment.type)
            self.topic_entry.insert(0, assignment.topic)
            self.student_first_name_entry.insert(0, student.first_name)
            self.student_last_name_entry.insert(0, student.last_name)
            self.lecturer_first_name_entry.insert(0, lecturer.first_name)
            self.lecturer_last_name_entry.insert(0, lecturer.last_name)
            self.grade_entry.insert(0, assignment.grade)
            self.date_entry.insert(0, assignment.date)
            self.time_entry.insert(0, assignment.time)
        else:
            # ggf.wurde ein Student mitgegeben, dann koennen wir diese Felder fuellen
            if student:
                self.student_first_name_entry.insert(0, student.first_name)
                self.student_last_name_entry.insert(0, student.last_name)


    def add_or_edit_assignment(self, parent, assignment):
        try:
            # Hole die Daten aus den Eingabefeldern
            assignment_type = self.type_dropdown.get()
            assignment_topic = self.topic_entry.get()
            assignment_grade = float(self.grade_entry.get().replace(",",".")) if self.grade_entry.get() else None
            assignment_student_first_name = self.student_first_name_entry.get()
            assignment_student_last_name = self.student_last_name_entry.get()
            assignment_lecturer_first_name = self.lecturer_first_name_entry.get()
            assignment_lecturer_last_name = self.lecturer_last_name_entry.get()
            assignment_date = self.date_entry.get()
            assignment_time = self.time_entry.get()

            # Ermittele Student_id und Lecturer_id
            student = parent.controller.read_student_by_name(assignment_student_last_name, assignment_student_first_name)
            if not student:
                messagebox.showerror("Student nicht gefunden", f"Student {assignment_student_first_name} {assignment_lecturer_last_name} ist nicht in der Datenbank.")
                return
            
            lecturer = parent.controller.read_lecturer_by_name(assignment_lecturer_last_name, assignment_lecturer_first_name)
            if not lecturer:
                messagebox.showerror("Gutachter nicht gefunden", f"Gutachter {assignment_lecturer_first_name} {assignment_lecturer_last_name} ist nicht in der Datenbank.")
                return


            if assignment:
                # Bearbeite die vorhandene Arbeit, wenn assignment vorhanden ist
                parent.controller.update_assignment(
                    assignment.assignment_id,
                    student.student_id,
                    lecturer.lecturer_id,
                    assignment_type,
                    assignment_topic,
                    assignment_grade,
                    assignment_date,
                    assignment_time
                )
            else:
                # Füge hier die Logik zum Hinzufügen der Arbeit hinzu
                parent.controller.create_assignment(
                    student.student_id,
                    lecturer.lecturer_id,
                    assignment_type,
                    assignment_topic,
                    assignment_grade,
                    assignment_date,
                    assignment_time
                )

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()
        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

            
