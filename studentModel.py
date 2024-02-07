import sqlite3
from config import Config

class Model:
    def __init__(self) -> None:
        self.person = Person()
        self.student = Student()
        self.lecturer = Lecturer()
        self.course = Course()
        self.enrollments = Enrollments()
        self.assignments = Assignments()
        self.lastUsedItems = LastUsedItems()



class Person:
    def __init__(self):
        self.personId = None
        self.firstName = None
        self.lastName = None
        self.email = None
        self.creationDate = None

        self.connectToDatabase()

        

    def createPerson(self, lastName, firstName, email):
        newPerson = Person()
        newPerson.firstName = firstName
        newPerson.lastName = lastName
        newPerson.email = email

        newPerson.personId = self.writePersonToDB(lastName, firstName, email)

        return newPerson
    
    def writePersonToDB(self, lastName, firstName, email):
        self.cursor.execute('''
            INSERT INTO persons (lastName, firstName, email)
            VALUES (?, ?, ?)
        ''', (lastName, firstName, email))
        self.conn.commit()
        return self.cursor.lastrowid

    def readAllPersons(self):
        personsDBDump = self.readAllPersonsFromDB()

        #baue Liste von Personen aus DB Dump
        personsList =[]
        for row in personsDBDump:
            newPerson = Person()
            newPerson.personId = row[0]
            newPerson.firstName = row[1]
            newPerson.lastName = row[2]
            newPerson.email = row[3]
            newPerson.creationDate = row[4]
            personsList.append(newPerson)

        return personsList
    
    def readAllPersonsFromDB(self):
        self.cursor.execute('SELECT * FROM persons')
        return self.cursor.fetchall()
    
    def readPersonById(self,personId):
        person = Person()
        personDBDump = self.readPersonByPersonIdFromDB(personId)

        if personDBDump:
            person.personId = personDBDump[0]
            person.firstName = personDBDump[1]
            person.lastName = personDBDump[2]
            person.email = personDBDump[3]
            person.creationDate = personDBDump[4]
            return person
        else:
            return None

    def readPersonByPersonIdFromDB(self,personId):
        self.cursor.execute('SELECT * FROM persons WHERE personId = ?',(personId,))
        return self.cursor.fetchone()
    
    def readPersonByName(self,lastName, firstName):
        person = Person()
        personDBDump = self.readPersonByNameFromDB(lastName, firstName)

        if personDBDump:
            person.personId = personDBDump[0]
            person.firstName = personDBDump[1]
            person.lastName = personDBDump[2]
            person.email = personDBDump[3]
            person.creationDate = personDBDump[4]
            return person
        else:
            return None

    def readPersonByNameFromDB(self, lastName, firstName):
        self.cursor.execute('SELECT * FROM persons WHERE firstName = ? AND lastName = ?',(firstName, lastName, ))
        return self.cursor.fetchone()

    def updatePerson(self, personId, newLastName, newFirstName, newEmail):
        self.cursor.execute('''
            UPDATE persons
            SET lastName = ?,
                firstName = ?,
                email = ?
            WHERE personId = ?
        ''', (newLastName, newFirstName, newEmail, personId))
        self.conn.commit()

    def deletePerson(self, personId):
        self.cursor.execute('DELETE FROM persons WHERE personId = ?', (personId,))
        self.conn.commit()

    def connectToDatabase(self):
        configs = Config()
        databaseName = configs.dataBaseName
        self.conn = sqlite3.connect(databaseName)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class Student(Person):
    def __init__(self):
        self.studentId = None
        self.company = None
        self.matNumber = None
        self.enrolled = False
        self.connectToDatabase()

    def createStudent(self, lastName, firstName, email, company, matNumber, enrolled):
        newStudent = Student()
        newStudent.firstName = firstName
        newStudent.lastName = lastName
        newStudent.email = email
        newStudent.company = company
        newStudent.matNumber = matNumber
        newStudent.enrolled = enrolled

        # Erstelle eine neue Person
        studentPerson = self.createPerson(lastName, firstName, email)
        newStudent.personId = studentPerson.personId

        # schreibe Student in die Studentendatenbank
        newStudent.studentId = self.writeStudentToDB(studentPerson.personId, company, matNumber, enrolled)

        return newStudent

    def writeStudentToDB(self,personId, company, matNumber, enrolled):
        # Füge den Studenten hinzu
        self.cursor.execute('''
            INSERT INTO students (personId, company, matNumber, enrolled)
            VALUES (?, ?, ?, ?)
        ''', (personId, company, matNumber, enrolled))
        self.conn.commit()

        return self.cursor.lastrowid

    def readAllStudents(self):
        studentsDBDump = self.readAllStudentsFromDB()

        #baue Liste von Personen aus DB Dump
        studentsList =[]
        for row in studentsDBDump:
            newStudent = Student()
            newStudent.personId = row[0]
            newStudent.firstName = row[1]
            newStudent.lastName = row[2]
            newStudent.email = row[3]
            newStudent.studentId = row[4]
            newStudent.company = row[5]
            newStudent.matNumber = row[6]
            newStudent.enrolled = bool(row[7])
            newStudent.creationDate = row[8]
            studentsList.append(newStudent)

        return studentsList


    def readAllStudentsFromDB(self):
        self.cursor.execute('SELECT persons.personId, persons.firstName, persons.LastName, persons.eMail,students.studentId, students.company, students.matNumber, students.enrolled, students.creationDate FROM persons JOIN students ON persons.personId = students.personId')
        return self.cursor.fetchall()
    
    def readAllStudentsByCourseId(self, courseId):
        studentsDBDump = self.readAllStudentsByCourseIdFromDB(courseId)

        #baue Liste von Personen aus DB Dump
        studentsList =[]
        for row in studentsDBDump:
            newStudent = Student()
            newStudent.personId = row[0]
            newStudent.firstName = row[1]
            newStudent.lastName = row[2]
            newStudent.email = row[3]
            newStudent.studentId = row[4]
            newStudent.company = row[5]
            newStudent.matNumber = row[6]
            newStudent.enrolled = bool(row[7])
            newStudent.creationDate = row[8]
            studentsList.append(newStudent)

        return studentsList

    def readAllStudentsByCourseIdFromDB(self, courseId):
        self.cursor.execute('''
            SELECT
                persons.personId,
                persons.firstName,
                persons.LastName,
                persons.eMail,
                students.studentId,
                students.company,
                students.matNumber,
                students.enrolled,
                students.creationDate
            FROM persons
            JOIN students ON persons.personId = students.personId
            WHERE students.studentId IN (SELECT enrollments.studentId FROM enrollments WHERE enrollments.courseId = ?)
            ''',(courseId,))
        return self.cursor.fetchall()

    def readStudentById(self, studentId):
        # Studentendaten holen
        student = Student()
        studentDBDump = self.readStudentFromDB(studentId)

        if studentDBDump:
            student.studentId = studentDBDump[0]
            student.personId = studentDBDump[1]
            student.company  = studentDBDump[2]
            student.matNumber = studentDBDump[3]
            student.enrolled = bool(studentDBDump[4])

            # Personendaten ergaenzen
            studentPerson = self.readPersonById(student.personId)

            student.lastName = studentPerson.lastName
            student.firstName = studentPerson.firstName
            student.email = studentPerson.email

            return student
        else: 
            return None

    def readStudentFromDB(self, studentId):
        self.cursor.execute('SELECT * FROM students WHERE studentId = ?',(studentId,))
        return self.cursor.fetchone()

    def readStudentByPersonId(self, personId):
        # Studentendaten holen
        student = Student()
        studentDBDump = self.readStudentFromDBByPersonId(personId)

        if studentDBDump:
            student.studentId = studentDBDump[0]
            student.personId = studentDBDump[1]
            student.company = studentDBDump[2]
            student.matNumber = studentDBDump[3]
            student.enrolled = bool(studentDBDump[4])

            # Personendaten ergaenzen
            studentPerson = self.readPersonById(student.personId)

            student.lastName = studentPerson.lastName
            student.firstName = studentPerson.firstName
            student.email = studentPerson.email

            return student
        else: 
            return None

    def readStudentFromDBByPersonId(self, personId):
        self.cursor.execute('SELECT * FROM students WHERE personId = ?',(personId,))
        return self.cursor.fetchone()
    
    def readStudentByName(self, lastName, firstName):
        # zuerst die Person holen:
        person = self.readPersonByName(lastName, firstName)

        if person:
            # jetzt studentendaten ergänzen
            return self.readStudentByPersonId(person.personId)
        else:
            return None

    def updateStudent(self, studentId, personId, newLastName, newFirstName, newEmail, newCompany, newMatNumber, newEnrolled):
        self.updatePerson(personId, newLastName, newFirstName, newEmail)

        # Aktualisiere die Informationen des Studenten
        self.cursor.execute('''
            UPDATE students
            SET company = ?,
                matNumber = ?,
                enrolled = ?
            WHERE studentId = ?
        ''', (newCompany, newMatNumber, newEnrolled, studentId))
        self.conn.commit()

    def deleteStudent(self, studentId):
        # Lösche den Studenten (Person wird automatisch gelöscht durch Fremdschlüsselbeziehung)
        self.cursor.execute('DELETE FROM students WHERE studentId = ?', (studentId,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Lecturer(Person):
    def __init__(self):
        self.lecturerId = None
        self.company = None
        self.connectToDatabase()

    def createLecturer(self, lastName, firstName, email, company):
        newLecturer = Lecturer()
        newLecturer.firstName = firstName
        newLecturer.lastName = lastName
        newLecturer.email = email
        newLecturer.company = company

        # Erstelle eine neue Person
        lecturerPerson = self.createPerson(lastName, firstName, email)
        newLecturer.personId = lecturerPerson.personId

        # Schreibe Dozenten in die Dozentendatenbank
        newLecturer.lecturerId = self.writeLecturerToDB(lecturerPerson.personId, company)

        return newLecturer

    def writeLecturerToDB(self, personId, company):
        # Füge den Dozenten hinzu
        self.cursor.execute('''
            INSERT INTO lecturers (personId, company)
            VALUES (?, ?)
        ''', (personId, company))
        self.conn.commit()

        return self.cursor.lastrowid

    def readAllLecturers(self):
        lecturersDBDump = self.readAllLecturersFromDB()

        # Baue Liste von Dozenten aus DB Dump
        lecturersList = []
        for row in lecturersDBDump:
            newLecturer = Lecturer()
            newLecturer.personId = row[0]
            newLecturer.firstName = row[1]
            newLecturer.lastName = row[2]
            newLecturer.email = row[3]
            newLecturer.lecturerId = row[4]
            newLecturer.company = row[5]
            newLecturer.creationDate = row[6]
            lecturersList.append(newLecturer)

        return lecturersList

    def readAllLecturersFromDB(self):
        self.cursor.execute('SELECT persons.personId, persons.firstName, persons.LastName, persons.eMail, lecturers.lecturerId, lecturers.company, lecturers.creationDate FROM persons JOIN lecturers ON persons.personId = lecturers.personId')
        return self.cursor.fetchall()

    def readLecturerById(self, lecturerId):
        # Dozentendaten holen
        lecturer = Lecturer()
        lecturerDBDump = self.readLecturerFromDB(lecturerId)

        if lecturerDBDump:
            lecturer.lecturerId = lecturerDBDump[0]
            lecturer.personId = lecturerDBDump[1]
            lecturer.company = lecturerDBDump[2]

            # Personendaten ergänzen
            lecturerPerson = self.readPersonById(lecturer.personId)

            lecturer.lastName = lecturerPerson.lastName
            lecturer.firstName = lecturerPerson.firstName
            lecturer.email = lecturerPerson.email

            return lecturer
        else:
            return None

    def readLecturerFromDB(self, lecturerId):
        self.cursor.execute('SELECT * FROM lecturers WHERE lecturerId = ?', (lecturerId,))
        return self.cursor.fetchone()
    
    def readLecturerByPersonId(self, personId):
        # Dozentendaten holen
        lecturer = Lecturer()
        lecturerDBDump = self.readLecturerFromDBByPersonId(personId)

        if lecturerDBDump:
            lecturer.lecturerId = lecturerDBDump[0]
            lecturer.personId = lecturerDBDump[1]
            lecturer.company = lecturerDBDump[2]

            # Personendaten ergänzen
            lecturerPerson = self.readPersonById(lecturer.personId)

            lecturer.lastName = lecturerPerson.lastName
            lecturer.firstName = lecturerPerson.firstName
            lecturer.email = lecturerPerson.email

            return lecturer
        else:
            return None
    
    def readLecturerFromDBByPersonId(self, personId):
        self.cursor.execute('SELECT * FROM lecturers WHERE personId = ?', (personId,))
        return self.cursor.fetchone()
    
    def readLecturerByName(self, lastName, firstName):
        # zuerst die Person holen:
        person = self.readPersonByName(lastName, firstName)

        if person:
            # jetzt Dozentendaten ergänzen
            return self.readLecturerByPersonId(person.personId)
        else:
            return None

    def updateLecturer(self, lecturerId, personId, newLastName, newFirstName, newEmail, newCompany):
        self.updatePerson(personId, newLastName, newFirstName, newEmail)

        # Aktualisiere die Informationen des Dozenten
        self.cursor.execute('''
            UPDATE lecturers
            SET company = ?
            WHERE lecturerId = ?
        ''', (newCompany, lecturerId))
        self.conn.commit()

    def deleteLecturer(self, lecturerId):
        # Lösche den Dozenten (Person wird automatisch gelöscht durch Fremdschlüsselbeziehung)
        self.cursor.execute('DELETE FROM lecturers WHERE lecturerId = ?', (lecturerId,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Course:
    def __init__(self):
        self.courseId = None
        self.courseName = None
        self.startDate = None
        self.creationDate = None

        self.connectToDatabase()
    
    def createCourse(self,courseName, startDate):
        newCourse = Course()
        newCourse.courseName = courseName
        newCourse.startDate = startDate

        newCourse.courseId = self.writeCourseToDB(courseName, startDate)

        return newCourse
    
    def writeCourseToDB(self, courseName, startDate):
        # Füge den Kurs zur Datenbank hinzu
        self.cursor.execute('''
            INSERT INTO courses (courseName, startDate)
            VALUES (?, ?)
        ''', (courseName, startDate))
        self.conn.commit()

        return self.cursor.lastrowid
    
    def readCourseById(self,courseId):
        # Kursdaten holen
        course = Course()
        courseDBDump = self.readCourseFromDB(courseId)

        if courseDBDump:
            course.courseId = courseDBDump[0]
            course.courseName = courseDBDump[1]
            course.startDate = courseDBDump[2]
            course.creationDate = courseDBDump[3]

            return course
        else:
            return None

    def readCourseFromDB(self, courseId):
        self.cursor.execute('SELECT * FROM courses WHERE courseId = ?', (courseId,))
        return self.cursor.fetchone()
    
    def readAllCourses(self):
        coursesDBDump = self.readAllCoursesFromDB()

        # Baue Liste von Dozenten aus DB Dump
        coursesList = []
        for row in coursesDBDump:
            newCourse = Course()
            newCourse.courseId = row[0]
            newCourse.courseName = row[1]
            newCourse.startDate = row[2]
            newCourse.creationDate = row[3]
            coursesList.append(newCourse)

        return coursesList

    def readAllCoursesFromDB(self):
        self.cursor.execute('SELECT * FROM courses')
        return self.cursor.fetchall()

    def updateCourse(self, courseId, courseName, startDate):
        # Aktualisiere die Informationen des Kurses
        self.cursor.execute('''
            UPDATE courses
            SET courseName = ?,
                startDate = ?
            WHERE courseId = ?
        ''', (courseName, startDate, courseId))
        self.conn.commit()

    def deleteCourse(self, courseId):
        # Lösche den Kurs
        self.cursor.execute('DELETE FROM courses WHERE courseId = ?', (courseId,))
        self.conn.commit()

    def readAllEnrolledStudents(self):
        # alle enrollenments zum Kurs holen
        enrollmentsDBDump = self.cursor.execute('SELECT * FROM enrollments WHERE courseId = ?', (self.courseId,))

        enrollmentsList = []
        for row in enrollmentsDBDump:
            newEnrollment = Enrollments()
            newEnrollment.enrollmentId = row[0]
            newEnrollment.studentId = row[1]
            newEnrollment.courseId = row[2]
            enrollmentsList.append(newEnrollment)

        # jetzt aus den enrollments die Studenten in eine Liste packen
        studentsList = []

        for enrollment in enrollmentsList:
            newStudent = Student()
            newStudent.readStudentById(enrollment.studentId)
            studentsList.append(newStudent)

        return studentsList


    def connectToDatabase(self):
        configs = Config()
        databaseName = configs.dataBaseName
        self.conn = sqlite3.connect(databaseName)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class Enrollments:
    def __init__(self):
        self.enrollmentId = None
        self.studentId = None
        self.courseId = None

        self.connectToDatabase()

    def addStudentToCourse(self, studentId, courseId):
        self.cursor.execute('''
            INSERT INTO enrollments (studentId, courseId)
            VALUES (?, ?)
        ''', (studentId, courseId))
        self.conn.commit()

    def readEnrollmentById(self,enrollmentId):
        # Kursdaten holen
        enrollment = Enrollments()
        enrollmentDBDump = self.readEnrollmentFromDB(enrollmentId)

        if enrollmentDBDump:
            enrollment.enrollmentId = enrollmentDBDump[0]
            enrollment.studentId = enrollmentDBDump[1]
            enrollment.courseId = enrollmentDBDump[2]

            return enrollment
        else:
            return None

    def readEnrollmentFromDB(self, enrollmentId):
        self.cursor.execute('SELECT * FROM enrollments WHERE enrollmentId = ?', (enrollmentId,))
        return self.cursor.fetchone()

    def readAllEnrollments(self):
        enrollmentsDBDump = self.readAllEnrollmentsFromDB()

        # Baue Liste von Enrollments aus DB Dump
        enrollmentsList = []
        for row in enrollmentsDBDump:
            newEnrollment = Enrollments()
            newEnrollment.enrollmentId = row[0]
            newEnrollment.studentId = row[1]
            newEnrollment.courseId = row[2]
            enrollmentsList.append(newEnrollment)

        return enrollmentsList

    def readAllEnrollmentsFromDB(self):
        self.cursor.execute('SELECT * FROM enrollments')
        return self.cursor.fetchall()
    
    def readAllEnrollmentsByStudentId(self, studentId):
        enrollmentsDBDump = self.readAllEnrollmentsByStudentIdFromDB(studentId)

        # Baue Liste von Enrollments aus DB Dump
        enrollmentsList = []
        for row in enrollmentsDBDump:
            newEnrollment = Enrollments()
            newEnrollment.enrollmentId = row[0]
            newEnrollment.studentId = row[1]
            newEnrollment.courseId = row[2]
            enrollmentsList.append(newEnrollment)

        return enrollmentsList

    def readAllEnrollmentsByStudentIdFromDB(self, studentId):
        self.cursor.execute('SELECT * FROM enrollments WHERE studentId = ?', (studentId, ))
        return self.cursor.fetchall()
    
    def updateEnrollment(self, enrollmentId, studentId, courseId):
        # Aktualisiere die Informationen des Kurses
        self.cursor.execute('''
            UPDATE enrollments
            SET studentId = ?,
                courseId = ?
            WHERE enrollmentId = ?
        ''', (studentId, courseId, enrollmentId))
        self.conn.commit()

    def deleteEnrollment(self, enrollmentId):
        # Lösche den Kurs
        self.cursor.execute('DELETE FROM enrollments WHERE enrollmentId = ?', (enrollmentId,))
        self.conn.commit()  

    def connectToDatabase(self):
        configs = Config()
        databaseName = configs.dataBaseName
        self.conn = sqlite3.connect(databaseName)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class Assignments:
    def __init__(self):
        self.assignmentId = None
        self.studentId = None
        self.lecturerId = None
        self.type = None
        self.topic = None
        self.grade = None
        self.date = None
        self.time = None

        self.connectToDatabase()

    def createAssignment(self, studentId, lecturerId, type, topic, grade, date, time):
        newAssignment = Assignments()
        newAssignment.studentId = studentId
        newAssignment.lecturerId = lecturerId
        newAssignment.type = type
        newAssignment.topic = topic
        newAssignment.grade = grade
        newAssignment.date = date
        newAssignment.time = time

        newAssignment.assignmentId = self.writeAssignmentToDB(studentId, lecturerId, type, topic, grade, date, time)

        return newAssignment
    
    def writeAssignmentToDB(self, studentId, lecturerId, type, topic, grade, date, time):
        realGrade = str(grade).replace(",",".")
        # Füge das Assignment zur Datenbank hinzu
        self.cursor.execute('''
            INSERT INTO assignments (studentId, lecturerId, type, topic, grade, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (studentId, lecturerId, type, topic, realGrade, date, time))
        self.conn.commit()

        return self.cursor.lastrowid

    def AddStudentToAssignment(self, studentId, assignmentId):
        self.cursor.execute('''
            INSERT INTO assignments (studentId)
            VALUES (?)
            WHERE assignmentId = ?
        ''', (studentId, assignmentId))
        self.conn.commit()

    def AddLecturerToAssignment(self, lecturerId, assignmentId):
        self.cursor.execute('''
            INSERT INTO assignments (lecturerId)
            VALUES (?)
            WHERE assignmentId = ?
        ''', (lecturerId, assignmentId))
        self.conn.commit()

    def readAssignmentById(self, assignmentId):
        # Daten holen
        assignmentDBDump = self.readAssignmentFromDBById(assignmentId)

        if assignmentDBDump:
            return self.createAssignmentFromDBDump(assignmentDBDump)
        else:
            return None

    def readAssignmentFromDBById(self, assignmentId):
        self.cursor.execute('SELECT * FROM assignments WHERE assignmentId = ?', (assignmentId,))
        return self.cursor.fetchone()

    def readAssignmentByStudentIdAndType(self, studentId, assignmentType):
        # Daten holen
        assignmentDBDump = self.readAssignmentFromDBBytudentIdAndType(studentId, assignmentType)

        if assignmentDBDump:
            return self.createAssignmentFromDBDump(assignmentDBDump)
        else:
            return None

    def readAssignmentFromDBBytudentIdAndType(self, studentId, assignmentType):
        self.cursor.execute('SELECT * FROM assignments WHERE studentId = ? AND type = ?', (studentId, assignmentType,))
        return self.cursor.fetchone()

    def readAllAssignments(self):
        assignmentsDBDump = self.readAllAssignmentsFromDB()

        AssignmentsList = []
        for row in assignmentsDBDump:
            newAssignment = self.createAssignmentFromDBDump(row)
            AssignmentsList.append(newAssignment)

        return AssignmentsList

    def readAllAssignmentsFromDB(self):
        self.cursor.execute('SELECT * FROM Assignments')
        return self.cursor.fetchall()

    def readAllAssignmentsByStudentId(self, studentId):
        assignmentsDBDump = self.readAllAssignmentsByStudentIdFromDB(studentId)

        AssignmentsList = []
        for row in assignmentsDBDump:
            newAssignment = self.createAssignmentFromDBDump(row)
            AssignmentsList.append(newAssignment)

        return AssignmentsList
    
    def createAssignmentFromDBDump(self, assignmentDump):
        # Assignment aus DB Dump
        
        newAssignment = Assignments()
        newAssignment.assignmentId = assignmentDump[0]
        newAssignment.studentId = assignmentDump[1]
        newAssignment.lecturerId = assignmentDump[2]
        newAssignment.type = assignmentDump[3]
        newAssignment.topic = assignmentDump[4]
        newAssignment.grade = str(assignmentDump[5]).replace(".",",")
        newAssignment.date = assignmentDump[6]
        newAssignment.time = assignmentDump[7]
        
        return newAssignment

    def readAllAssignmentsByStudentIdFromDB(self, studentId):
        self.cursor.execute('SELECT * FROM assignments WHERE studentId = ?', (studentId, ))
        return self.cursor.fetchall()

    def updateAssignment(self, assignmentId, studentId, lecturerId, type, topic, grade, date, time):
        # Aktualisiere die Informationen der Arbeit
        realGrade = str(grade).replace(",",".")
        self.cursor.execute('''
            UPDATE assignments
            SET studentId = ?,
                lecturerId = ?,
                type = ?,
                topic = ?,
                grade = ?,
                date = ?,
                time = ?
            WHERE assignmentId = ?
        ''', (studentId, lecturerId, type, topic, realGrade, date, time, assignmentId))
        self.conn.commit()

    def deleteAssignment(self, assignmentId):
        # Lösche den Kurs
        self.cursor.execute('DELETE FROM assignments WHERE assignmentId = ?', (assignmentId,))
        self.conn.commit()  

    def connectToDatabase(self):
        configs = Config()
        databaseName = configs.dataBaseName
        self.conn = sqlite3.connect(databaseName)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class LastUsedItems():
    def __init__(self):
        self.type = None
        self.elements = None
        
        self.connectToDatabase()

    def createLastUsedItem(self, type, elements):
        newLastUsedItem = LastUsedItems()
        newLastUsedItem.type = type
        newLastUsedItem.elements = elements

        elementsAsString = ','.join(map(str, elements))

        self.writeLastUsedItemToDB(type, elementsAsString)

        return newLastUsedItem
    
    def writeLastUsedItemToDB(self, type, elementsString):
        self.cursor.execute('''
            INSERT INTO lastUsedItems (type, elements)
            VALUES (?, ?)
        ''', (type, elementsString, ))
        self.conn.commit() 

    def readLastUsedItemByType(self, type):
        self.cursor.execute('SELECT * FROM lastUsedItems WHERE type = ?', (type, ))
        lastUsedItemDBDump = self.cursor.fetchone()

        if lastUsedItemDBDump:
            newLastUsedItem = LastUsedItems()
            newLastUsedItem.type = lastUsedItemDBDump[0]
            newLastUsedItem.elements = list(map(str, lastUsedItemDBDump[1].split(',')))

            return newLastUsedItem
        else: 
            return None
    
    def updateLastUsedItem(self, type, elements):
        elementsAsString = ','.join(map(str, elements))
        self.cursor.execute('''
            UPDATE lastUsedItems
            SET elements = ?
            WHERE type = ?
        ''', (elementsAsString, type))
        self.conn.commit()

    def deleteAllLastUsedElements(self):
        self.cursor.execute('DELETE FROM lastUsedItems')
        self.conn.commit()


    def connectToDatabase(self):
        configs = Config()
        databaseName = configs.dataBaseName
        self.conn = sqlite3.connect(databaseName)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

