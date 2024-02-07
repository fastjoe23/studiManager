import tkinter as tk
from tkinter import scrolledtext, filedialog

class GenerateCourseListWindow(tk.Toplevel):
    def __init__(self, parent, course_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Mail Parser")

        # Erklärungstext mit Zeilenumbrüchen
        explanation_text = "Kopieren Sie in das folgende Textfeld den Block mit den Email-Abkürzungen\n und den Namen aus einer Test-Mail, welche Sie an den studentischen Verteiler \n 'stud-verteiler+KURS@lehre.dhbw-stuttgart.de' \n gesendet haben.\n  Bspw:\n    wi1234 (Doe, John)\n    wi2345 (Austen, Jane)"
        explanation_label = tk.Label(self, text=explanation_text)
        explanation_label.pack(padx=10, pady=10)

        # Großes Textfeld mit Scrollbar
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10)

        explanation_text2 = "Wenn Sie auf den Knopf drücken, wird der Text interpretiert\n und eine Liste für das Einlesen des Kurses erzeugt."
        explanation_label2 = tk.Label(self,text=explanation_text2)
        explanation_label2.pack(padx=10, pady=10)

        # Button zum Auswählen des Speicherorts
        select_path_button = tk.Button(self, text="Speicherort auswählen", command=self.select_save_path)
        select_path_button.pack(pady=5)

        # Eingabefeld für Dateipfad
        self.save_path_entry = tk.Entry(self, width=40)
        self.save_path_entry.pack(pady=5)

        # Button zum Parsen
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        parse_button = tk.Button(button_frame, text="Parse", command=lambda: self.parse_text(course_id))
        parse_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)


    def select_save_path(self):
        # Funktion zum Auswählen des Speicherorts
        save_path = filedialog.askdirectory()
        if save_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(tk.END, save_path)



    def parse_text(self, course_id):
        # Funktion zum Parsen des Textes hier implementieren
        text_content = self.text_area.get("1.0", tk.END)
        parsed_data = self.master.master.controller.parse_function(text_content)

        # Kursinfos beschaffen
        course = self.master.master.controller.read_course_by_id(course_id)
        
        # Ergebnis speichern
        save_path = self.save_path_entry.get()
        self.master.master.controller.save_list_to_file(parsed_data, save_path, "Kursliste", course.course_name)

        # Schließe das Fenster nach Parsen und Speichern
        self.destroy()

    
