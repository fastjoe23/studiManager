import tkinter as tk
from tkinter import ttk

from views.one_assignment_frame import OneAssignmentWindow
from views.one_note_frame import OneNoteWindow

class OneLecturerWindow(tk.Toplevel):
    def __init__(self, parent, lecturer=None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Dozent bearbeiten" if lecturer else "Neuen Dozenten hinzufügen")

        # Frame für Eingabefelder und Notizfeld
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Eingabefelder für die neuen Dozentendaten
        personal_frame = tk.Frame(input_frame)
        personal_frame.pack(side=tk.LEFT, padx=10)
        self.first_name_label = tk.Label(personal_frame, text="Vorname:")
        self.first_name_entry = tk.Entry(personal_frame, width=30)

        self.last_name_label = tk.Label(personal_frame, text="Nachname:")
        self.last_name_entry = tk.Entry(personal_frame, width=30)

        self.email_label = tk.Label(personal_frame, text="E-Mail:")
        self.email_entry = tk.Entry(personal_frame, width=30)

        self.company_label = tk.Label(personal_frame, text="Firma:")
        self.company_entry = tk.Entry(personal_frame, width=30)

        self.first_name_label.grid(row=0, column=0, pady=5, sticky=tk.E)
        self.first_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.last_name_label.grid(row=1, column=0, pady=5, sticky=tk.E)
        self.last_name_entry.grid(row=1, column=1, pady=5, padx=5)
        self.email_label.grid(row=2, column=0, pady=5, sticky=tk.E)
        self.email_entry.grid(row=2, column=1, pady=5, padx=5)
        self.company_label.grid(row=3, column=0, pady=5, sticky=tk.E)
        self.company_entry.grid(row=3, column=1, pady=5, padx=5)

        # Notizfeld
        notes_frame = tk.Frame(input_frame)
        notes_frame.pack(side=tk.LEFT, padx=10)
        notes_label_frame = tk.Frame(notes_frame)
        notes_label_frame.pack(pady=5)
        note_label = tk.Label(notes_label_frame, text="Notizen")
        note_label.pack(fill=tk.X, side=tk.LEFT, padx=10, pady=5)
        self.add_note_button = tk.Button(notes_label_frame, text= "+", command=lambda: self.add_note(lecturer.lecturer_id))
        self.add_note_button.pack(fill=tk.X, side=tk.RIGHT, padx=10, pady=5)
        self.note_treeview = ttk.Treeview(notes_frame, columns=("note_id", "title"), show="headings", height=5)
        self.note_treeview.heading("note_id", text="ID")
        self.note_treeview.column("note_id", width=30)
        self.note_treeview.heading("title", text="Titel")
        # Vertikale Scrollbar hinzufügen
        yscrollbar_notes = ttk.Scrollbar(notes_frame, orient='vertical', command=self.note_treeview.yview)
        self.note_treeview.configure(yscrollcommand=yscrollbar_notes.set)

        yscrollbar_notes.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_treeview.pack(fill=tk.BOTH, expand=True)



        # Wenn ein Dozent vorhanden ist, fülle die Eingabefelder und das Notizfeld vor
        if lecturer:
            self.first_name_entry.insert(0, lecturer.first_name)
            self.last_name_entry.insert(0, lecturer.last_name)
            self.email_entry.insert(0, lecturer.email)
            self.company_entry.insert(0, lecturer.company)

            # Notizfeld befüllen, falls vorhanden
            self.load_lecturer_notes(lecturer.lecturer_id)
            # Doppelklick-Ereignis auf den Treeview binden
            self.note_treeview.bind("<Double-1>", lambda event, lecturer_id=lecturer.lecturer_id: self.on_note_double_click(event, lecturer_id))            

            # Zeige die zugehörigen Assignments an
            # Frame für die Zuordnung der Dozentenarbeiten
            assignment_frame = tk.Frame(self)
            assignment_frame.pack(pady=10)

            # Label für die Tabelle
            assignments_label = tk.Label(assignment_frame, text="Betreute Arbeiten:")
            assignments_label.pack(fill=tk.X, padx=10, pady=5)

            # Treeview für die Zuordnung der Dozentenarbeiten
            self.tree = ttk.Treeview(assignment_frame, columns=("ID", "Typ", "Vorname Student", "Nachname Student"), show="headings", height=4)
            self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
            self.tree.column("ID", width=30)
            self.tree.heading("Typ", text="Typ", command=lambda: self.sort_column("Typ"))
            self.tree.column("Typ", width=90)
            self.tree.heading("Vorname Student", text="Vorname Student", command=lambda: self.sort_column("Vorname Student"))
            self.tree.heading("Nachname Student", text="Nachname Student", command=lambda: self.sort_column("Nachname Student"))
                        
            # Vertikale Scrollbar hinzufügen
            yscrollbar = ttk.Scrollbar(assignment_frame, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=yscrollbar.set)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.tree.pack(fill=tk.BOTH, expand=True)

            # Doppelklick-Ereignis auf den Treeview binden
            self.tree.bind("<Double-1>", lambda event: self.on_assignment_double_click(parent, lecturer, event))            

            #tree view füllen
            self.refresh_table(parent, lecturer)


        # Knöpfe zum Hinzufügen oder Bearbeiten des Dozenten
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if lecturer else "Dozent hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_lecturer(parent, lecturer))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Bindung der Enter-Taste an die Funktion und Setzen des Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_lecturer(parent, lecturer))
        self.focus_set()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)


    def on_assignment_double_click(self, parent, lecturer, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        self.update_selected_assignment(parent, lecturer) 

    def on_note_double_click(self, event, lecturer_id):
        self.update_selected_note(lecturer_id)                     

    def add_or_edit_lecturer(self, parent, lecturer):
        try:
            # Daten aus den Eingabefeldern holen
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            email = self.email_entry.get()
            company = self.company_entry.get()

            if lecturer:
                # Dozent bearbeiten, wenn vorhanden
                parent.controller.update_lecturer(lecturer.lecturer_id, lecturer.person_id, last_name, first_name, email, company)
            else:
                # Neuen Dozenten hinzufügen
                new_lecturer = parent.controller.add_lecturer(last_name, first_name, email, company)

            # Fenster nach dem Hinzufügen oder Bearbeiten schließen
            self.destroy()

        except ValueError as e:
            # Fehlermeldung anzeigen, wenn ein Fehler auftritt
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

    def load_lecturer_notes(self, lecturer_id):
        list_of_notes = self.master.controller.read_notes_by_type_and_related_id("lecturer",lecturer_id)

        # Lösche die Tabelle
        for row in self.note_treeview.get_children():
            self.note_treeview.delete(row)

        for note in list_of_notes:
            self.note_treeview.insert("", tk.END, values=(note.note_id, note.note_title))

    def update_selected_note(self, lecturer_id):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.note_treeview.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return
        
        note_id = self.note_treeview.item(selected_item, "values")[0]
        #Öffne das Fenster zum Hinzufügen oder Ändern einer Notiz
        add_note_window = OneNoteWindow(self.master, "lecturer", lecturer_id, note_id)
        add_note_window.grab_set()
        add_note_window.wait_window()
        
        self.load_lecturer_notes(lecturer_id)

    def add_note(self, lecturer_id):
        add_note_window = OneNoteWindow(self.master, "lecturer", lecturer_id)
        add_note_window.grab_set()
        add_note_window.wait_window()
        
        self.load_lecturer_notes(lecturer_id)


    def update_selected_assignment(self, parent, lecturer):
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
        self.refresh_table(parent, lecturer)

    def refresh_table(self, parent, lecturer):
        # Logik zum Aktualisieren der Tabelle
        assignments = parent.controller.read_all_assignments_by_lecturer_id(lecturer.lecturer_id)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for assignment in assignments:
            # zugehoerigen Studenten lesen
            student = parent.controller.read_student_by_id(assignment.student_id)

            #Zeile fuellen 
            self.tree.insert("", tk.END, values=(assignment.assignment_id, assignment.type, student.first_name, student.last_name))


        

