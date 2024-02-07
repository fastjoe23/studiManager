import tkinter as tk
from tkinter import ttk, filedialog

class GenerateAssignmentListWindow(tk.Toplevel):
    def __init__(self, parent, course_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Mail Parser")

        # Erklärungstext mit Zeilenumbrüchen
        explanation_text = "Wählen Sie den Typ der Arbeit aus und geben Sie einen Speicherort an:"
        explanation_label = tk.Label(self, text=explanation_text)
        explanation_label.pack(padx=10, pady=10)

        # Dropdown-Menü für den Typ der Arbeit
        assignment_types = ["Bachelorarbeit", "Projektarbeit 1", "Projektarbeit 2"]
        self.assignment_type_var = tk.StringVar(self)
        self.assignment_type_var.set(assignment_types[0])  # Standardwert
        self.type_dropdown = ttk.Combobox(self, textvariable=self.assignment_type_var, values=assignment_types)
        self.type_dropdown.pack(pady=10)

        # Button für die Speicherortauswahl
        browse_button = tk.Button(self, text="Speicherort auswählen", command=self.select_output_directory)
        browse_button.pack(pady=10)

        # Eingabefeld für Dateipfad
        self.save_path_entry = tk.Entry(self, width=40)
        self.save_path_entry.pack(pady=5)

        # Button zum Parsen
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        parse_button = tk.Button(button_frame, text="Liste generieren", command=lambda: self.generate_list(course_id))
        parse_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def select_output_directory(self):
        save_path = filedialog.askdirectory()
        if save_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(tk.END, save_path)

    def generate_list(self, course_id):
        # csv-Liste erzeugen
        # Typ der Liste ermitteln
        type = self.type_dropdown.get()
        if type:
            csv_data = self.master.master.controller.generate_assignment_list(type, course_id)

            # Kursinfos beschaffen
            course = self.master.master.controller.read_course_by_id(course_id)

            # Ergebnis speichern
            save_path = self.save_path_entry.get()
            if save_path:
                self.master.master.controller.save_list_to_file(csv_data, save_path, type, course.course_name)

        # Schließe das Fenster nach Generierung und Speichern
        self.destroy()

