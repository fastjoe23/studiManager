# Kleines Skript um alle Assignements eines bestimmten Kurses zu exportieren
import logging
from config import Config
from studi_manager_controller import StudentManagerController
from studi_manager_model import Model
from dhbw_mail import DHBWMail

# Variablen festlegen
COURSE_ID = 4
ASSIGNMENT_TYPE = "Projektarbeit 2"

myModel = Model()
myController = StudentManagerController(myModel)
mail_client = DHBWMail()
logger = logging.getLogger(__name__)

# Konfigurationsdaten holen
configs = Config()
# Logger initialisieren
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=configs.log_file_path + configs.log_file_name,
    encoding="utf-8",
    level=configs.log_level,
    format=configs.log_format,
)
logger.info("Email-Versand gestartet")


# Kurs einlesen
course = myController.read_course_by_id(COURSE_ID)
logger.info("Kurs %s eingelesen.", course.course_name)
# alle Studenten aus dem Kurs lesen
students_list = myController.read_all_students_by_course_id(COURSE_ID)

# Login in Mail-Client
try:
    mail_client.login()
except Exception as e:
    raise e

# Schleife ueber alle Studenten im Kurs
email_counter = 0
result = {"success": True, "error_message": ""}
for student in students_list:
    if student.enrolled:
        # Assignment ermitteln
        assignment = myController.read_assignment_by_student_id_and_type(
            student.student_id, ASSIGNMENT_TYPE
        )
        if assignment:
            # Gutachter ermitteln
            lecturer = myController.read_lecturer_by_id(assignment.lecturer_id)
            if not lecturer:
                print(f"Gutachter {assignment.lecturer_id} nicht gefunden.")
            # Platzhalter ersetzen
            # Variablen für die Ersetzung
            variables = {
                "Vorname_student": student.first_name,
                "Nachname_student": student.last_name,
                "Vorname_gutachter": lecturer.first_name,
                "Nachname_gutachter": lecturer.last_name,
            }
            # Ersetze die Platzhalter in der Zeichenkette durch die Variablen
            email_text = myController.get_mail_text(ASSIGNMENT_TYPE)
            formatted_email_text = email_text.format(**variables)

            logger.debug(
                "Sende Mail mit Betreff %s an %s", ASSIGNMENT_TYPE, student.email
            )
            result = mail_client.send_email_without_login(
                to_address=student.email,
                cc_address=lecturer.email,
                subject=ASSIGNMENT_TYPE,
                body=formatted_email_text,
            )

            if result["success"] is False:
                logger.warning(
                    "Fehler beim Mailversand mit Betreff %s an %s",
                    ASSIGNMENT_TYPE,
                    student.email,
                )
                logger.error("Fehler beim Mailverand: %s", result["error_message"])
            else:
                email_counter += 1
                logger.debug(
                    "Mail mit Betreff %s an %s (Student %s %s) erfolgreich versendet.",
                    ASSIGNMENT_TYPE,
                    student.email,
                    student.first_name,
                    student.last_name,
                )
mail_client.logout()

logger.info("Es wurden %s Emails erfolgreich versandt.", email_counter)
