import tkinter as tk
from tkinter import ttk, messagebox
from views.one_course_frame import OneCourseWindow
from views.confirmation_dialog_delete_course import ConfirmationDialogDeleteCourse

class CoursesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.title_label = tk.Label(self, text= "Verwaltung Kurse", font=('Arial', 14, 'bold'))
        self.title_label.pack()
        # Tabelle für die Anzeige der Kurse erstellen
        self.tree = ttk.Treeview(self, columns=("ID", "Kursname", "Startdatum", "Erstelldatum"), show="headings")
        self.tree.heading("ID", text="ID", command=lambda: self.sort_column("ID"))
        self.tree.column("ID", width=30)
        self.tree.heading("Kursname", text="Kursname", command=lambda: self.sort_column("Kursname"))
        self.tree.heading("Startdatum", text="Startdatum", command=lambda: self.sort_column("Startdatum"))
        self.tree.heading("Erstelldatum", text="Erstelldatum", command=lambda: self.sort_column("Erstelldatum"))

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

        # Knöpfe zum Hinzufügen, Löschen und Ändern von Kursen erstellen
        add_button = tk.Button(self, text="Neuer Kurs hinzufügen", command=lambda: self.open_add_course_window(parent))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self, text="Kurs löschen", command=self.delete_selected_course)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        update_button = tk.Button(self, text="Kurs ändern", command=self.update_selected_course)
        update_button.pack(side=tk.LEFT, padx=5, pady=5)

        manage_button = tk.Button(self, text="Kurs verwalten", command=self.manage_selected_course)
        manage_button.pack(side=tk.LEFT, padx=5, pady=5)

        close_button = tk.Button(self, text="Schliessen", command=self.close_frame)
        close_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Doppelklick-Ereignis auf den Treeview binden
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        # Funktion, die bei Doppelklick auf eine Zeile aufgerufen wird
        # Hole das selektierte Item
        self.manage_selected_course()

    def sort_column(self, column):
        # Funktion zum Sortieren der Tabelle nach der ausgewählten Spalte
        items = self.tree.get_children("")
        items = sorted(items, key=lambda x: self.tree.set(x, column))
        for i, item in enumerate(items):
            self.tree.move(item, "", i)

    def open_add_course_window(self, parent):
        # Öffne das Fenster zum Hinzufügen eines neuen Kurses
        add_course_window = OneCourseWindow(self.master)  # Annahme: Du hast eine One_course_window-Klasse für die Kurse
        add_course_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        add_course_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table()

    def delete_selected_course(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        course_id = self.tree.item(selected_item, "values")[0]
        course_to_delete = self.master.controller.read_course_by_id(course_id)

        # Überprüfe, ob die Person in keiner untergeordneten Tabelle vorhanden ist
        if not self.are_students_enrolled_in_course(course_to_delete):
            # Erstelle eine Bestätigungsdialogbox
            confirmation_dialog = ConfirmationDialogDeleteCourse(self, course_to_delete, lambda: self.confirm_delete_course(selected_item))
            confirmation_dialog.grab_set()  # Sperrt das Hauptfenster während der Dialogbox geöffnet ist
            confirmation_dialog.wait_window()  # Blockiert das Hauptfenster, bis die Dialogbox geschlossen wird
        else:
        # Zeige eine Meldung an, dass die Person in untergeordneten Tabellen verwendet wird
            messagebox.showwarning("Warnung", "Der Kurs kann nicht gelöscht werden, da noch Studenten eingeschrieben sind.")

    def are_students_enrolled_in_course(self, course):
        # alle Eintraege aus Enrollment holen
        enrolled_students = course.read_all_enrolled_students()

        return len(enrolled_students) > 0
        
        
    def confirm_delete_course(self, selected_item):
        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        course_id = self.tree.item(selected_item, "values")[0]

        # Lösche den ausgewählten Kurs aus der Datenbank
        self.master.controller.delete_course(course_id)

        # Aktualisiere die Tabelle, um die Änderungen zu reflektieren
        self.refresh_table()

    def update_selected_course(self):
        # Erhalte die ausgewählte Zeile in der Tabelle
        selected_item = self.tree.selection()

        if not selected_item:
            # Keine Zeile ausgewählt
            return

        # Extrahiere die Kursdaten aus der ausgewählten Zeile
        course_id = self.tree.item(selected_item, "values")[0]

        # Öffne das Fenster zum Hinzufügen oder Ändern eines neuen Kurses
        update_course_window = OneCourseWindow(self.master, course_id)  # Annahme: Du hast eine One_course_window-Klasse für die Kurse
        update_course_window.grab_set()  # Sperrt das Hauptfenster, während das Unterfenster geöffnet ist
        update_course_window.wait_window()  # Blockiert das Hauptfenster, bis das Unterfenster geschlossen wird
        self.refresh_table()

    def manage_selected_course(self):
        selected_item = self.tree.selection()

        if selected_item:
            # Extrahiere die Kursdaten aus der ausgewählten Zeile
            course_id = self.tree.item(selected_item, "values")[0]

            # Rufe die Funktion im Hauptfenster auf, um zur Kursverwaltung zu wechseln
            self.master.switch_to_course_management(course_id)

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
        courses = self.master.controller.read_all_courses()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for course in courses:
            self.tree.insert("", tk.END, values=(course.course_id, course.course_name, course.start_date, course.creation_date))
