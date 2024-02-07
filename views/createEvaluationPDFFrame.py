import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog




class CreateEvaluationPDFWindow(tk.Toplevel):
    def __init__(self, parent, courseId, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Begutachtungsformulare erzeugen")

         # Label für Hinweistext
        self.label = tk.Label(self, text="Hier können Blanko-Begutachtungsformulare erstellt werden.\n Wählen Sie einen Typ der studentischen Arbeit aus\n und geben Sie einen Speicherort an. Anschließend wird für jede stud. Arbeit\n des gewählten Typs aus dem Kurs ein Blanko-Formular erstellt.", anchor="w")
        self.label.pack(pady=10)

        # Dropdown-Menü für Projektauswahl
        self.typeVar = tk.StringVar()
        types = ["Projektarbeit 1", "Projektarbeit 2", "Bachelorarbeit"]
        self.typeDropdown = ttk.Combobox(self, textvariable=self.typeVar, values=types, state="readonly")
        self.typeDropdown.pack(pady=10)

        # Button für die Speicherortauswahl
        browseButton = tk.Button(self, text="Speicherort auswählen", command=self.selectOutputDirectory)
        browseButton.pack(pady=10)

        # Eingabefeld für Dateipfad
        self.savePathEntry = tk.Entry(self, width=40)
        self.savePathEntry.pack(pady=5)

        # Button 
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        parseButton = tk.Button(button_frame, text="Formulare generieren", command=lambda: self.generatePDFs(courseId))
        parseButton.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def selectOutputDirectory(self):
        savePath = filedialog.askdirectory()
        if savePath:
            self.savePathEntry.delete(0, tk.END)
            self.savePathEntry.insert(tk.END, savePath)

    def generatePDFs(self, courseId):
        # Typ der Formulare ermitteln
        type = self.typeDropdown.get()
        # Speicherort ermitteln
        savePath = self.savePathEntry.get()

        # Überprüfe, ob Speicherort und Type ausgewählt wurde
        if savePath and type:
            try:
                # Rufe die Methode zum Importieren von Studenten in den Kurs auf
                generatedPDFs = self.master.master.controller.generatedEvaluationPDFs(savePath, type, courseId)
                if len(generatedPDFs) == 1:
                    messageText = f"Es wurde ein Formular erfolgreich erzeugt."
                else:
                    messageText = f"Es wurden {len(generatedPDFs)} Formulare erfolgreich erzeugt."
                    
                messagebox.showinfo("Formulargenerierung", messageText)

            except Exception as e:
                # Zeige eine Messagebox mit dem Inhalt der Exception an
                messagebox.showerror("Fehler beim Importieren", str(e))
        
        self.destroy()

            