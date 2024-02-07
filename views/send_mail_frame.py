import tkinter as tk
from tkinter import ttk, messagebox

class SendMailWindow(tk.Toplevel):
    def __init__(self, parent, course_id, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Mail versenden")
        

         # Label für Hinweistext
        self.label = tk.Label(self, text="Hier kann eine Email an den Kurs versendet werden.\n\n_durch Auswahl eines Typs wird ein vorformatierter Text erzeugt.\n_dieser kann unten vorm Versenden bearbeitet werden.\n_achtung die versendeten Emails werden im Email-Client NICHT angezeigt!", anchor="w")
        self.label.pack(pady=10)

        # Dropdown-Menü für Projektauswahl
        self.type_var = tk.StringVar()
        types = ["Projektarbeit 1", "Projektarbeit 2", "Bachelorarbeit", "Freitext"]
        self.project_dropdown = ttk.Combobox(self, textvariable=self.type_var, values=types, state="readonly")
        self.project_dropdown.pack(pady=10)

        # Entry-Field für Email-Betreff
        self.email_subject_label = tk.Label(self, text= "Betreff:")
        self.email_subject_entry = tk.Entry(self, width=30)
        self.email_subject_label.pack(padx=20, pady=10, anchor=tk.W)
        self.email_subject_entry.pack(padx=20, pady=10, anchor=tk.W)


        # Texteingabefeld für Email-Inhalt
        self.email_text = tk.Text(self, height=10, width=60)
        self.email_text.pack(pady=10)

        # Knopf zum Versenden der Email
        self.send_button = tk.Button(self, text="Versenden", command=lambda: self.send_email(course_id))
        self.send_button.pack(pady=10)

        # Event Binding für die Combobox-Auswahl
        self.project_dropdown.bind("<<ComboboxSelected>>", self.update_text_field)

    def update_text_field(self, event):
        # Funktion wird aufgerufen, wenn sich die Auswahl in der Combobox ändert
        selected_type = self.type_var.get()

        # Hole den Text entsprechend des ausgewählten Typs
        text = self.master.master.controller.get_mail_text(selected_type)
        # Füge den ausgewählten Text in das Texteingabefeld und den Betreff ein
        self.email_subject_entry.delete(0,tk.END)                    
        self.email_subject_entry.insert(0, selected_type)
        self.email_text.delete("1.0", "end-1c")  # Lösche den vorhandenen Text im Eingabefeld
        self.email_text.insert("1.0", text)


    def send_email(self, course_id):
        # Funktion wird nach Knopfdruck aufgerufen und versendet die Email an den kompletten Kurs + eventuell an Gutachter
        e_mail_subject = self.email_subject_entry.get()
        e_mailtext = self.email_text.get("1.0", "end-1c")

        selected_type = self.type_var.get()
        if selected_type == "Projektarbeit 1" or \
           selected_type == "Projektarbeit 2" or \
           selected_type == "Bachelorarbeit":
            result = self.master.master.controller.send_mail_to_students_and_lecturers(selected_type, e_mail_subject, e_mailtext, course_id)
        else: #type = Freitext
            result =self.master.master.controller.send_mail_to_students(e_mail_subject, e_mailtext, course_id)

        if result['success'] == False:
            if result['error_message'].startswith("(535"):
                # Fehler Authentification failed, eventuell ist das Passwort abgelaufen
                messagebox.showerror("Fehler beim Mailversand", "Anmeldeinformationen ungültig. Ungültiger Benutzername oder falsches Passwort. Ist Ihr Passwort abgelaufen? " + result['error_message'])
            else:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Mailversand", result['error_message'])
        
        # Email-Versand-Fenster schließen
        self.destroy()
