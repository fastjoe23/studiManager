from fpdf import FPDF
from fpdf.enums import XPos, YPos


class EvaluationCreationError(Exception):
    pass


class PresentationEvaluationPDF(FPDF):
    def __init__(
        self,
        save_path,
        evaluation_type,
        course_name,
        topic,
        lecturers,
        student,
        date,
        time,
    ):
        super().__init__()
        self.save_path = save_path
        self.topic = topic
        self.course_name = course_name
        self.lecturers = lecturers
        self.student_name = student
        self.evaluation_type = evaluation_type
        self.date = date
        self.time = time

    def header(self):
        self.set_font("helvetica", "B", 13)
        # Abkürzung für Art der Prüfung
        if self.evaluation_type == "Bachelorarbeit":
            abbrevation_type = "BA"
        elif self.evaluation_type == "Projektarbeit 1":
            abbrevation_type = "PA 1"
        elif self.evaluation_type == "Projektarbeit 2":
            abbrevation_type = "PA 2"
        else:
            abbrevation_type = self.evaluation_type

        title = f"Bewertung mündliche {abbrevation_type}-Prüfung"
        self.cell(
            w=0, h=10, text=title, border=0, new_x=XPos.LEFT, new_y=YPos.NEXT, align="C"
        )
        self.cell(
            w=0,
            h=10,
            text=f"Kurs {self.course_name}",
            border=0,
            new_x=XPos.LEFT,
            new_y=YPos.NEXT,
            align="C",
        )

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 12)
        max_width = 180  # Maximale Breite der Zelle
        self.multi_cell(
            w=max_width, h=10, text=title, border=0, align="L", new_x=XPos.LEFT
        )
        self.set_font("helvetica", "", 12)

    def create_evaluation(self):
        try:
            self.add_page()

            self.chapter_title(f"Titel: {self.topic}")
            self.chapter_title(f"Vortragende/r: {self.student_name}")
            self.chapter_title(f"Datum: {self.date}, {self.time} Uhr")
            self.chapter_title(
                f"Gutachter*in: {', '.join(str(x) for x in self.lecturers)} "
            )
            self.ln(3)
            self.chapter_title("(A) Präsentation")

            self.set_font("helvetica", "", 11)
            with self.table(
                col_widths=(60, 60, 50, 60), borders_layout="NONE"
            ) as table:
                row = table.row()
                row.cell("Vortragsstil", colspan=4)
                row = table.row()
                row.cell("(Umfang und Rhetorik)")
                row.cell("spannend / überzeugend")
                row.cell("O---O---O---O---O")
                row.cell("langatmig/zäh und wenig überzeugend")

                row = table.row()
                self.set_font("helvetica", "B", 11)
                row.cell("Fachkenntnisse", colspan=4)
                self.set_font("helvetica", "", 11)
                row = table.row()
                row.cell("(Qualität + Logik)")
                row.cell("kompetenter Eindruck, durchgehend logisch")
                row.cell("O---O---O---O---O")
                row.cell("kein kompetenter Eindruck, roter Faden fehlt")

                row = table.row()
                self.set_font("helvetica", "B", 11)
                row.cell("Unterlagen", colspan=4)
                self.set_font("helvetica", "", 11)
                row = table.row()
                row.cell("(Folien + Handout)")
                row.cell("gut aufbereitet, gut verständlich")
                row.cell("O---O---O---O---O")
                row.cell("schlecht aufbereitet, wenig verständlich")

            self.ln(5)
            self.chapter_title("(B) Diskussion")
            self.set_font("helvetica", "", 11)
            with self.table(
                col_widths=(60, 60, 50, 60),
                borders_layout="NONE",
                first_row_as_headings=False,
            ) as table:
                row = table.row()
                row.cell("Antwortverhalten")
                row.cell("kompetente Antworten")
                row.cell("O---O---O---O---O")
                row.cell("wenig überzeugend")

            self.ln(5)
            self.chapter_title("(C) Allgemeine Anmerkungen:")
            self.cell(text="-")
            self.ln(10)
            self.cell(text="-")
            self.ln(30)
            self.chapter_title("(D) Note:")
            self.ln()
            self.cell(text="Unterschriften:", align="L")
            
            pdf_file_path = (
                self.save_path
                + f"/{str(self.course_name)}_{str(self.evaluation_type).replace(' ','')}_{str(self.student_name).replace(' ','')}_Bewertungsbogen.pdf"
            )
            self.output(pdf_file_path)
            return pdf_file_path

        except Exception as e:
            error_message = f"Fehler bei der Erstellung der Bewertung: {self.topic} {e}"
            raise EvaluationCreationError(error_message) from e
