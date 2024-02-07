import tkinter as tk
from tkinter import ttk, messagebox

class SendMailWindow(tk.Toplevel):
    def __init__(self, parent, courseId, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Mail versenden")
        

         # Label für Hinweistext
        self.label = tk.Label(self, text="Hier kann eine Email an den Kurs versendet werden.\n\nDurch Auswahl eines Typs wird ein vorformatierter Text erzeugt.\nDieser kann unten vorm Versenden bearbeitet werden.\nAchtung die versendeten Emails werden im Email-Client NICHT angezeigt!", anchor="w")
        self.label.pack(pady=10)

        # Dropdown-Menü für Projektauswahl
        self.typeVar = tk.StringVar()
        types = ["Projektarbeit 1", "Projektarbeit 2", "Bachelorarbeit", "Freitext"]
        self.projectDropdown = ttk.Combobox(self, textvariable=self.typeVar, values=types, state="readonly")
        self.projectDropdown.pack(pady=10)

        # Entry-Field für Email-Betreff
        self.emailSubjectLabel = tk.Label(self, text= "Betreff:")
        self.emailSubjectEntry = tk.Entry(self, width=30)
        self.emailSubjectLabel.pack(padx=20, pady=10, anchor=tk.W)
        self.emailSubjectEntry.pack(padx=20, pady=10, anchor=tk.W)


        # Texteingabefeld für Email-Inhalt
        self.emailText = tk.Text(self, height=10, width=60)
        self.emailText.pack(pady=10)

        # Knopf zum Versenden der Email
        self.sendButton = tk.Button(self, text="Versenden", command=lambda: self.sendEmail(courseId))
        self.sendButton.pack(pady=10)

        # Event Binding für die Combobox-Auswahl
        self.projectDropdown.bind("<<ComboboxSelected>>", self.updateTextField)

    def updateTextField(self, event):
        # Funktion wird aufgerufen, wenn sich die Auswahl in der Combobox ändert
        selectedType = self.typeVar.get()

        # Hole den Text entsprechend des ausgewählten Typs
        text = self.master.master.controller.getMailText(selectedType)
        # Füge den ausgewählten Text in das Texteingabefeld und den Betreff ein
        self.emailSubjectEntry.delete(0,tk.END)                    
        self.emailSubjectEntry.insert(0, selectedType)
        self.emailText.delete("1.0", "end-1c")  # Lösche den vorhandenen Text im Eingabefeld
        self.emailText.insert("1.0", text)


    def sendEmail(self, courseId):
        # Funktion wird nach Knopfdruck aufgerufen und versendet die Email an den kompletten Kurs + eventuell an Gutachter
        eMailSubject = self.emailSubjectEntry.get()
        eMailtext = self.emailText.get("1.0", "end-1c")

        selectedType = self.typeVar.get()
        if selectedType == "Projektarbeit 1" or \
           selectedType == "Projektarbeit 2" or \
           selectedType == "Bachelorarbeit":
            result = self.master.master.controller.sendMailToStudentsAndLecturers(selectedType, eMailSubject, eMailtext, courseId)
        else: #type = Freitext
            result =self.master.master.controller.sendMailToStudents(eMailSubject, eMailtext, courseId)

        if result['success'] == False:
            if result['errorMessage'].startswith("(535"):
                # Fehler Authentification failed, eventuell ist das Passwort abgelaufen
                messagebox.showerror("Fehler beim Mailversand", "Anmeldeinformationen ungültig. Ungültiger Benutzername oder falsches Passwort. Ist Ihr Passwort abgelaufen? " + result['errorMessage'])
            else:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Mailversand", result['errorMessage'])
        
        # Email-Versand-Fenster schließen
        self.destroy()