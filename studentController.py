import csv
from presentationEvaluationPdf import PresentationEvaluationPDF
from studentModel import LastUsedItems, Person
from dhbwMail import DHBWMail
import re 

#Hilfsklassen
class StudentNotFoundException(Exception):
    pass

class LecturerNotFoundException(Exception):
    pass

class StudentController:
    def __init__(self, model):
        self.model = model

# Controller Methoden fuer Person   
    def addPerson(self,lastName,firstName,email):
        newPerson = Person()
        if email:
            self.checkValidMail(email)
        return newPerson.createPerson(lastName,firstName, email)
    
    def deletePerson(self,personId):
        
        return self.model.person.deletePerson(personId)
    
    def updatePerson(self,personId,lastName,firstName,email):
        if email:
            self.checkValidMail(email)
        return self.model.person.updatePerson(personId,lastName,firstName,email)
    
    def readPersonById(self,personId):
        return self.model.person.readPersonById(personId)
    
    def readPersonByName(self, lastName, firstName):
        return self.model.person.readPersonByName(lastName, firstName)
    
    def readAllPersons(self):
        return self.model.person.readAllPersons()
    
# Controller Methoden fuer Student  
    def addStudent(self, lastName, firstName, email, company, matNumber, enrolled):
        if email:
            self.checkValidMail(email)

        newStudent = self.model.student.createStudent(lastName, firstName, email, company, matNumber, enrolled)
        return newStudent

    def deleteStudent(self, studentId):
        return self.model.student.deleteStudent(studentId)

    def updateStudent(self, studentId,personId, lastName, firstName, email, company, matNumber, enrolled):
        if email:
            self.checkValidMail(email)
        return self.model.student.updateStudent(studentId, personId, lastName, firstName, email, company, matNumber, enrolled)
    
    def readStudentById(self,studentId):
        return self.model.student.readStudentById(studentId)
    
    def readStudentByPersonId(self,personId):
        return self.model.student.readStudentByPersonId(personId) 
    
    def readStudentByName(self, lastName, firstName):
        return self.model.student.readStudentByName(lastName, firstName)
    
    def readAllStudents(self):
        return self.model.student.readAllStudents()
    
    def readAllStudentsByCourseId(self,courseId):
        return self.model.student.readAllStudentsByCourseId(courseId)

# Methoden für Lecturer    
    def addLecturer(self, lastName, firstName, email, company):
        if email:
            self.checkValidMail(email)

        newLecturer = self.model.lecturer.createLecturer(lastName, firstName, email, company)
        return newLecturer

    def deleteLecturer(self, lecturerId):
        return self.model.lecturer.deleteLecturer(lecturerId)

    def updateLecturer(self, lecturerId, personId, lastName, firstName, email, company):
        return self.model.lecturer.updateLecturer(lecturerId, personId, lastName, firstName, email, company)

    def readLecturerById(self, lecturerId):
        return self.model.lecturer.readLecturerById(lecturerId)
    
    def readLecturerByPersonId(self,personId):
        return self.model.lecturer.readLecturerByPersonId(personId)
    
    def readLecturerByName(self, lastName, firstName):
        return self.model.lecturer.readLecturerByName(lastName, firstName)

    def readAllLecturers(self):
        return self.model.lecturer.readAllLecturers()

    
    def checkValidMail(self, email):
        # Einfache Validierung für eine gültige E-Mail-Adresse
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Ungültige E-Mail-Adresse")

# Methoden für Course    
    def addCourse(self, courseName,startDate):
        newCourse = self.model.course.createCourse(courseName, startDate)
        return newCourse

    def deleteCourse(self, courseId):
        return self.model.course.deleteCourse(courseId)

    def updateCourse(self, courseId, courseName, startDate):
        return self.model.course.updateCourse(courseId, courseName, startDate)

    def readCourseById(self, courseId):
        return self.model.course.readCourseById(courseId)
    
    def readAllCourses(self):
        return self.model.course.readAllCourses()

# Methoden für Enrollments
    def AddStudentToCourse(self, studentId, courseId):
        return self.model.enrollments.addStudentToCourse(studentId, courseId)
    
    def readAllEnrollments(self):
        return self.model.enrollments.readAllEnrollments()
    
    def readAllEnrollmentsByStudentId(self, studentId):
        return self.model.enrollments.readAllEnrollmentsByStudentId(studentId)
    
    def deleteEnrollment(self, enrollmentId):
        return self.model.enrollments.deleteEnrollment(enrollmentId)

    def updateEnrollment(self, enrollmentId, studentId, courseId):
        return self.model.enrollments.updateEnrollment(enrollmentId, studentId, courseId)

    def readEnrollmentById(self, enrollmentId):
        return self.model.enrollments.readEnrollmentById(enrollmentId)

# Methoden für Assigments
    def createAssignment(self,studentId, lecturerId, type, topic, grade, date, time):
        return self.model.assignments.createAssignment(studentId, lecturerId, type, topic, grade, date, time)

    def AddStudentToAssignment(self, studentId, assignmentId):
        return self.model.assignments.AddStudentToAssignment(studentId, assignmentId)
    
    def AddLecturerToAssignment(self, lecturerId, assignmentId):
        return self.model.assignments.AddStudentToAssignment(lecturerId, assignmentId)
   
    def readAllAssignments(self):
        return self.model.assignments.readAllAssignments()
    
    def readAllAssignmentsByStudentId(self, studentId):
        return self.model.assignments.readAllAssignmentsByStudentId(studentId)
    
    def deleteAssignment(self, assignmentId):
        return self.model.assignments.deleteAssignment(assignmentId)

    def updateAssignment(self,  assignmentId, studentId, lecturerId, type, topic, grade, date, time):
        return self.model.assignments.updateAssignment( assignmentId, studentId, lecturerId, type, topic, grade, date, time)

    def readAssignmentById(self, assignmentId):
        return self.model.assignments.readAssignmentById(assignmentId)
    
    def readAssignmentByStudentIdAndType(self, studentId, assignmentType):
        return self.model.assignments.readAssignmentByStudentIdAndType(studentId, assignmentType)

# Methoden für lastUsedItems
    def createLastUsedItem(self, type, elements):
        return self.model.lastUsedItems.createLastUsedItem(type, elements)
    
    def readLastUsedItemByType(self, type):
        return self.model.lastUsedItems.readLastUsedItemByType(type)
    
    def updateLastUsedItem(self, type, elements):
        return self.model.lastUsedItems.updateLastUsedItem(type, elements)
    
    def addElementToLastUsedItems(self, type, element):
        actualState = LastUsedItems()
        actualState = self.readLastUsedItemByType(type)

        if actualState: # es gibt schon einen Eintrag von diesem Type
            if element in actualState.elements:
                # das element ist schon in den zuletzt verwendeten Elementen wir setzen es also nur ans Ende der Liste
                # als zuletzt zuletzt verwendetes Element
                # erstmal löschen
                actualState.elements.remove(element)
                # jetzt ans Ende setzen
                actualState.elements.append(element)
            else:
                # das Element ist noch nicht in der Liste und die Liste ist noch nicht voll
                if len(actualState.elements) < 3:
                    actualState.elements.append(element)
                else:
                # Es sind schon drei Elemente drin also löschen wir das erste Element (es ist das älteste)
                # und setzen das neue ans Ende
                    actualState.elements.pop(0)
                    actualState.elements.append(element)
        
            # jetzt aktualisieren wir den Eintrag in der Datenbank
            self.updateLastUsedItem(actualState.type, actualState.elements)
        else:
            # es gibt noch keinen Eintrag zu diesem Type also erstellen wir einen
            newElements = [element]
            self.createLastUsedItem(type, newElements)

# Import Methoden
    def saveListToFile(self,parsedData, savePath, type, courseName):
        fileName = courseName + type + ".csv"
        # Speichern des geparsten Ergebnisses in dem ausgewählten Ordner
        try:
            save_file_path = savePath + "/" + fileName
            with open(save_file_path, 'w', encoding='utf-8') as file:
                file.write(parsedData)
        except Exception as e:
            raise e

    def parseFunction(self, textContent):
        # Hier die eigentliche Parsing-Logik implementieren
        # Verwendet Regular Expressions, um Informationen aus den Zeilen zu extrahieren
        pattern = r'(\w+)\s+\(([^,]+),\s*([^)]+)\)'
        matches = re.findall(pattern, textContent)

        # Extrahiere Informationen und erstelle einen formatierten Text
        parsedResult = "Nachname,Vorname,Firma,Mat-Nr,Email\n"
        for match in matches:
            email, lastname, firstname = match
            parsedResult += f"{lastname},{firstname},,,{email}@lehre.dhbw-stuttgart.de\n"

        return parsedResult

    def importStudentsFromCsvIntoCourse(self, csvPath,courseId):
        try:
            with open(csvPath, 'r', encoding='utf-8') as file:
                csvReader = csv.reader(file)
                next(csvReader)  # Überspringe Header, wenn vorhanden

                for row in csvReader:
                    lastname, firstname, company, matNumber, email = [value.strip() for value in row]
                    newStudent = self.addStudent(lastname, firstname, email, company, matNumber,True)
                    self.AddStudentToCourse(newStudent.studentId, courseId)

        except Exception as e:
            raise e
        
    def importAssignmentsFromCsvIntoCourse(self, csvPath):
        try:
            with open(csvPath, 'r', encoding='utf-8') as file:
                csvReader = csv.reader(file)
                next(csvReader)  # Überspringe Header, wenn vorhanden

                importedAssignments = []

                for row in csvReader:
                    type, lastNameStudent, firstNameStudent, topic, lastNameLecturer, firstNameLecturer, grade, date, time  = [value.strip() for value in row]
                    # Studentendaten holen
                    student = self.readStudentByName(lastNameStudent, firstNameStudent)
                    if not student:
                        raise StudentNotFoundException(f"Student {firstNameStudent} {lastNameStudent} nicht gefunden.")
                    # Gutachterdaten holen
                    lecturer = self.readLecturerByName(lastNameLecturer, firstNameLecturer)
                    if not lecturer:
                        raise LecturerNotFoundException(f"Gutachter {firstNameLecturer} {lastNameLecturer} nicht gefunden.")
                    
                    # jetzt alle Daten zusammen also Assignment erstellen
                    assignment = self.createAssignment(student.studentId, lecturer.lecturerId, type, topic, grade, date, time)
                    importedAssignments.append(assignment)

            return importedAssignments
        except Exception as e:
            raise e
        
    def generateAssignmentList(self, type, courseId):
        # generiert eine Liste mit allen Studenten eines Kurses um eine Übersicht
        # über die Projekt-/Bachelorarbeiten zu erstellen, welche später eingelesen werden kann

        csvData = "Typ, Nachname Student, Vorname Student, Thema, Nachname Gutachter, Vorname Gutachter, Note, Datum, Uhrzeit\n"

        studentsList = self.readAllStudentsByCourseId(courseId)

        for student in studentsList:
            csvData += f"{type}, {student.lastName}, {student.firstName}, , , , ,  , \n"
        
        return csvData
    
# Mail Methoden
    def getMailText(self, type):
        if type == "Freitext":
            text = "Sie können nun einen beliebigen Text verfassen.\n" + \
                "Bitte beachten Sie, dass die versendete Mail nicht ihrem Mail-Client angezeigt wird.\n" + \
                "Besser Sie verwenden den studentischen Verteiler stud-verteiler+Kurs@lehre.dhbw-stuttgart.de."
        else:
            text = "Guten Tag {VornameStudent} {NachnameStudent},\n" + \
                   "in der Zwischenzeit konnten für die meisten Arbeiten passende Prüfer/innen und Betreuer/innen gefunden werden. " + \
                    "{VornameGutachter} {NachnameGutachter} wird die wissenschaftliche Betreuung Ihrer " + str(type) + " übernehmen.\n" + \
                    "Bitte nehmen Sie über die in CC stehende E-Mail-Adresse Kontakt mit Ihrem Gutachter auf, um sich über die Ausarbeitung der Arbeit abzustimmen.\n\n" + \
                    "Viel Erfolg und freundliche Grüße\n" + \
                    " "

        return text
    
    def sendMailToStudents(self, emailSubject, emailText, courseId):
        # versendet eine Mail mit dem Inhalt von emailText an alle eingeschriebenen Studenten im Kurs
        mailClient = DHBWMail()
        # alle Studenten aus dem Kurs lesen
        studentsList = self.readAllStudentsByCourseId(courseId)
        
        result= {'success': True, 'errorMessage': ''}
        for student in studentsList:
            if student.enrolled:
                result = mailClient.sendEmail(student.email, subject=emailSubject, body=emailText)
                if result["success"] == False:
                    return result
        
        return result

    def sendMailToStudentsAndLecturers(self, assignmentType, emailSubject, emailText, courseId):
        # versendet zu jeder studentischen Arbeit aus dem Kurs und vom gewählten Typ eine 
        # Mail mit emailText und emailSubject an alle eingeschriebenen Studenten + den 
        # entsprechenden Gutachter
        # Dabei werden im Text noch die Platzhalter ersetzt.
        mailClient = DHBWMail()
        # alle Studenten aus dem Kurs lesen
        studentsList = self.readAllStudentsByCourseId(courseId)
        
        result= {'success': True, 'errorMessage': ''}
        # Schleife ueber alle Studenten im Kurs
        for student in studentsList:
            if student.enrolled:
                # Assignment ermitteln
                assignment = self.readAssignmentByStudentIdAndType(student.studentId, assignmentType)
                if assignment:
                    # Gutachter ermitteln
                    lecturer = self.readLecturerById(assignment.lecturerId)
                    if not lecturer:
                        raise LecturerNotFoundException(f"Gutachter {assignment.lecturerId} nicht gefunden.")
                    # Platzhalter ersetzen
                    # Variablen für die Ersetzung
                    variables = {
                                    'VornameStudent': student.firstName,
                                    'NachnameStudent': student.lastName,
                                    'VornameGutachter': lecturer.firstName,
                                    'NachnameGutachter': lecturer.lastName,
                                }

                    # Ersetze die Platzhalter in der Zeichenkette durch die Variablen
                    formattedEmailText = emailText.format(**variables)

                    result = mailClient.sendEmail(toAddress= student.email, ccAddress= lecturer.email, subject= emailSubject, body= formattedEmailText)
                    if result["success"] == False:
                        return result
        # Ende Schleife ueber alle Studenten
        
        return result

# PDF Generierung Methoden
    def generatedEvaluationPDFs(self, savePath, type, courseId):
    #erzeugt für alle Assignments zum gewählten Type des Kurses ein Begutachtungsformular im Order savePath

        # Kursdaten ermitteln
        course = self.readCourseById(courseId)

        # alle Studenten aus dem Kurs lesen
        studentsList = self.readAllStudentsByCourseId(courseId)
        

        # Schleife ueber alle Studenten im Kurs
        generatedPDFFiles = []
        for student in studentsList:
            studentName = student.firstName + " " + student.lastName
            if student.enrolled:
                # Assignment ermitteln
                assignment = self.readAssignmentByStudentIdAndType(student.studentId, type)
                if assignment:
                    date = assignment.date
                    time = assignment.time
                    # Gutachter ermitteln
                    lecturer = self.readLecturerById(assignment.lecturerId)
                    lecturerNames = [lecturer.firstName + " " + lecturer.lastName,]
                    if not lecturer:
                        raise LecturerNotFoundException(f"Gutachter {assignment.lecturerId} nicht gefunden.")
                    
                    pdfFile = PresentationEvaluationPDF(savePath, type, course.courseName, assignment.topic, lecturerNames, studentName , date, time)
                    try:
                        pdfFilePath = pdfFile.create_evaluation()
                        generatedPDFFiles.append(pdfFilePath)
                    except Exception as e:
                        raise e
        
        return generatedPDFFiles
                    


