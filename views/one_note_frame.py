import datetime
import tkinter as tk

from studi_manager_model import Notes

class OneNoteWindow(tk.Toplevel):
    def __init__(self, parent, note_type, related_id, note_id = None, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.title("Notiz bearbeiten" if note_id else "Neue Notiz hinzufügen")


        # Eingabefelder für die neue Notiz
        self.title_label = tk.Label(self, text="Titel:")
        self.title_entry = tk.Entry(self, width=30)

        self.creation_date_text_label = tk.Label(self, text="Erstellt am:")
        self.creation_date_label = tk.Label(self,text="")

        self.last_modification_date_text_label = tk.Label(self, text="Zuletzt bearbeitet:")
        self.last_modification_date_label = tk.Label(self, text="")

        self.note_label = tk.Label(self, text="Text:")
        self.note_entry = tk.Text(self, height=6, width=60)

        # Knopf zum Hinzufügen oder Bearbeiten der Notiz
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        button_text = "OK" if note_id else "Notiz hinzufügen"
        add_button = tk.Button(button_frame, text=button_text, command=lambda: self.add_or_edit_note(parent, note_id, note_type, related_id))
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(button_frame, text="Abbrechen", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)        

        # Pack die Widgets
        self.title_label.pack(pady=5)
        self.title_entry.pack(pady=5)

        self.creation_date_text_label.pack(pady=5)
        self.creation_date_label.pack(pady=5)

        self.last_modification_date_text_label.pack(pady=5)
        self.last_modification_date_label.pack(pady=5)

        self.note_label.pack(pady=5)
        self.note_entry.pack(padx= 10, pady=5)


        # Bind Enter-Taste an die Funktion und setze den Fokus auf das Toplevel
        self.bind("<Return>", lambda event: self.add_or_edit_note(parent, note_id, note_type, related_id))
        self.focus_set()


        # Wenn note_id vorhanden ist, fülle die Eingabefelder vor
        if note_id:
            selected_note = parent.controller.read_note_by_id(note_id)
            self.title_entry.insert(0, selected_note.note_title)
            self.creation_date_label.config(text= selected_note.creation_date)
            self.last_modification_date_label.config(text= selected_note.last_modification_date)
            self.note_entry.insert("1.0", selected_note.note)
        else:
            # Wir fuellen die Daten mit dem aktuellen Zeitpunkt
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            self.creation_date_label.config(text= current_time_str)
            self.last_modification_date_label.config(text= current_time_str)
            

    def add_or_edit_note(self, parent, note_id, note_type, related_id):
        try:
            # Hole die Daten aus den Eingabefeldern
            new_note = Notes()
            new_note.note_type = note_type
            new_note.related_id = related_id
            new_note.note_title = self.title_entry.get()
            new_note.creation_date = self.creation_date_label.cget("text")
            # aktualisiere das last modification date
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            new_note.last_modification_date = current_time_str
            new_note.note = self.note_entry.get("1.0", "end-1c")


            if note_id:
                # Bearbeite die vorhandene Notiz, wenn note_id vorhanden ist


                parent.controller.update_note_by_id(note_id, new_note)
            else:
                # Füge hier die Logik zum Hinzufügen der Person hinzu
                parent.controller.create_note(new_note)

            # Schließe das Fenster nach dem Hinzufügen oder Bearbeiten
            self.destroy()

        except ValueError as e:
            # Wenn ein Fehler auftritt, zeige eine Meldung an
            error_label = tk.Label(self, text=str(e), fg="red")
            error_label.pack(pady=5)

