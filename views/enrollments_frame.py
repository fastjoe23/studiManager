import tkinter as tk
from tkinter import ttk
from views.confirmation_dialog_delete_enrollment import ConfirmationDialogDeleteEnrollment

class EnrollmentsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = tk.Label(self, text= "Verwaltung Einschreibungen", font=('Arial', 14, 'bold'))
        self.title_label.pack()
        # Tabelle für die Anzeige der Kurse erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Kursname", "Vorname Student", "Nachname Student"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Kursname", text="Kursname", command=lambda: self.sort_column("Kursname"))
        self.tree.heading("Vorname Student", text="Vorname Student", command=lambda: self.sort_column("Vorname Student"))
        self.tree.heading("Nachname Student", text="Nachname Student", command=lambda: self.sort_column("Nachname Student"))

        # Vertikale Scrollbar hinzufügen
        yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        
        self.refresh_table()

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

         # Suchfeld hinzufügen
        self.search_label = tk.Label(self, text="Suche", font=('Arial', 10), fg='grey')
        self.search_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.X)
        search_entry.bind("<KeyRelease>", self.search)  # Suche bei Tastenfreigabe

        delete_button = tk.Button(self, text="Einschreibung löschen", command=self.delete_selected_enrollment)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.close_frame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def delete_selected_enrollment(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        enrollment_id = self.tree.item(selected_item, "values")[0]
        enrollment_to_delete = self.master.controller.read_enrollment_by_id(enrollment_id)

        # Erstelle eine Bestätigungsdialogbox
        confirmation_dialog = ConfirmationDialogDeleteEnrollment(self, enrollment_to_delete, lambda: self.confirm_delete_enrollment(selected_item))
        confirmation_dialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
        confirmation_dialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        
    def confirm_delete_enrollment(self, selected_item):
        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        enrollment_id = self.tree.item(selected_item, "values")[0]

        # Lösche den ausgewählten Kurs aus der Datenbank
        self.master.controller.delete_enrollment(enrollment_id)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refresh_table()

    def close_frame(self):
        self.master.show_main_frame()

    def search(self, event):
        # Suche nach dem eingegebenen Text und markiere die gefundenen Zeilen
        search_query = self.search_var.get().lower()

        # Entferne zuvor gesetzte Tags
        for item in self.tree.get_children():
            self.tree.item(item, tags=[])

        # Schalter um ersten Eintrag zu speichern und später sichtbar zu schalten
        first_itemfound = False
        first_item = self.tree.get_children()[0]
        
        if search_query:
        # Durchsuche alle Zeilen im Treeview
            for item in self.tree.get_children():
                values = [value.lower() for value in self.tree.item(item, "values")]
                if any(search_query in value for value in values):
                # Markiere gefundene Zeilen mit dem "found" Tag
                    if not first_itemfound:
                        first_item = item
                        first_itemfound = True

                    self.tree.item(item, tags=["found"])
            self.tree.see(first_item)

        # Konfiguriere das Tag "found" für die Anzeige
        self.tree.tag_configure("found", background="yellow", foreground="black")


    def refresh_table(self):
        # Logik zum Aktualisieren der Tabelle hinzu
        enrollments = self.master.controller.read_all_enrollments()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for enrollment in enrollments:
            # zugehoerigen Kurs lesen
            course = self.master.controller.read_course_by_id(enrollment.course_id)
            if course:
                # zugehoerigen Studenten lesen
                student = self.master.controller.read_student_by_id(enrollment.student_id)
                if student:
                    #Zeile fuellen 
                    self.tree.insert("", tk.END, values=(enrollment.enrollment_id, course.course_name, student.first_name, student.last_name))
