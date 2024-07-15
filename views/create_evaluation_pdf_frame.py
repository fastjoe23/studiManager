import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog


class CreateEvaluationPDFWindow(tk.Toplevel):
    def __init__(self, parent, course_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Begutachtungsformulare erzeugen")

        # Label für Hinweistext
        self.label = tk.Label(
            self,
            text="Hier können Blanko-Begutachtungsformulare erstellt werden.\n Wählen Sie einen Typ der studentischen Arbeit aus\n und geben Sie einen Speicherort an. Anschließend wird für jede stud. Arbeit\n des gewählten Typs aus dem Kurs ein Blanko-Formular erstellt.",
            anchor="w",
        )
        self.label.pack(pady=10)

        # Dropdown-Menü für Projektauswahl
        self.type_var = tk.StringVar()
        types = ["Projektarbeit 1", "Projektarbeit 2", "Bachelorarbeit"]
        self.type_dropdown = ttk.Combobox(
            self, textvariable=self.type_var, values=types, state="readonly"
        )
        self.type_dropdown.pack(pady=10)

        # Button für die Speicherortauswahl
        browse_button = tk.Button(
            self, text="Speicherort auswählen", command=self.select_output_directory
        )
        browse_button.pack(pady=10)

        # Eingabefeld für Dateipfad
        self.save_path_entry = tk.Entry(self, width=40)
        self.save_path_entry.pack(pady=5)

        # Button
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        parse_button = tk.Button(
            button_frame,
            text="Formulare generieren",
            command=lambda: self.generate_pdfs(course_id),
        )
        parse_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def select_output_directory(self):
        save_path = filedialog.askdirectory()
        if save_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(tk.END, save_path)

    def generate_pdfs(self, course_id):
        # Typ der Formulare ermitteln
        assignment_type = self.type_dropdown.get()
        # Speicherort ermitteln
        save_path = self.save_path_entry.get()

        # Überprüfe, ob Speicherort und Type ausgewählt wurde
        if save_path and assignment_type:
            try:
                # Rufe die Methode zum Generieren der Pdfs auf
                generated_pdfs = self.master.master.controller.generate_evaluation_pdfs(
                    save_path, assignment_type, course_id
                )
                if len(generated_pdfs) == 1:
                    message_text = "Es wurde ein Formular erfolgreich erzeugt."
                else:
                    message_text = f"Es wurden {len(generated_pdfs)} Formulare erfolgreich erzeugt."

                messagebox.showinfo("Formulargenerierung", message_text)

            except Exception as e:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Erzeugen der Pdfs", str(e))

        self.destroy()
