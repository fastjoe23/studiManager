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
        self.person_id = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.creation_date = None

        self.connect_to_database()

        

    def create_person(self, last_name, first_name, email):
        new_person = Person()
        new_person.first_name = first_name
        new_person.last_name = last_name
        new_person.email = email

        new_person.person_id = self.write_person_to_dB(last_name, first_name, email)

        return new_person
    
    def write_person_to_dB(self, last_name, first_name, email):
        self.cursor.execute('''
            INSERT INTO persons (lastName, firstName, email)
            VALUES (?, ?, ?)
        ''', (last_name, first_name, email))
        self.conn.commit()
        return self.cursor.lastrowid

    def read_all_persons(self):
        persons_dBDump = self.read_all_persons_from_db()

        #baue Liste von Personen aus DB Dump
        persons_list =[]
        for row in persons_dBDump:
            new_person = Person()
            new_person.person_id = row[0]
            new_person.first_name = row[1]
            new_person.last_name = row[2]
            new_person.email = row[3]
            new_person.creation_date = row[4]
            persons_list.append(new_person)

        return persons_list
    
    def read_all_persons_from_db(self):
        self.cursor.execute('SELECT * FROM persons')
        return self.cursor.fetchall()
    
    def read_person_by_id(self,person_id):
        person = Person()
        person_dBDump = self.read_person_by_person_id_from_db(person_id)

        if person_dBDump:
            person.person_id = person_dBDump[0]
            person.first_name = person_dBDump[1]
            person.last_name = person_dBDump[2]
            person.email = person_dBDump[3]
            person.creation_date = person_dBDump[4]
            return person
        else:
            return None

    def read_person_by_person_id_from_db(self,person_id):
        self.cursor.execute('SELECT * FROM persons WHERE personId = ?',(person_id,))
        return self.cursor.fetchone()
    
    def read_person_by_name(self,last_name, first_name):
        person = Person()
        person_dBDump = self.read_person_by_name_from_db(last_name, first_name)

        if person_dBDump:
            person.person_id = person_dBDump[0]
            person.first_name = person_dBDump[1]
            person.last_name = person_dBDump[2]
            person.email = person_dBDump[3]
            person.creation_date = person_dBDump[4]
            return person
        else:
            return None

    def read_person_by_name_from_db(self, last_name, first_name):
        self.cursor.execute('SELECT * FROM persons WHERE firstName = ? AND lastName = ?',(first_name, last_name, ))
        return self.cursor.fetchone()

    def update_person(self, person_id, new_last_name, new_first_name, new_email):
        self.cursor.execute('''
            UPDATE persons
            SET lastName = ?,
                firstName = ?,
                email = ?
            WHERE personId = ?
        ''', (new_last_name, new_first_name, new_email, person_id))
        self.conn.commit()

    def delete_person(self, person_id):
        self.cursor.execute('DELETE FROM persons WHERE personId = ?', (person_id,))
        self.conn.commit()

    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class Student(Person):
    def __init__(self):
        self.student_id = None
        self.company = None
        self.mat_number = None
        self.enrolled = False
        self.connect_to_database()

    def create_student(self, last_name, first_name, email, company, mat_number, enrolled):
        new_student = Student()
        new_student.first_name = first_name
        new_student.last_name = last_name
        new_student.email = email
        new_student.company = company
        new_student.mat_number = mat_number
        new_student.enrolled = enrolled

        # Erstelle eine neue Person
        student_person = self.create_person(last_name, first_name, email)
        new_student.person_id = student_person.person_id

        # schreibe Student in die Studentendatenbank
        new_student.student_id = self.write_student_to_db(student_person.person_id, company, mat_number, enrolled)

        return new_student

    def write_student_to_db(self,person_id, company, mat_number, enrolled):
        # Füge den Studenten hinzu
        self.cursor.execute('''
            INSERT INTO students (personId, company, matNumber, enrolled)
            VALUES (?, ?, ?, ?)
        ''', (person_id, company, mat_number, enrolled))
        self.conn.commit()

        return self.cursor.lastrowid

    def read_all_students(self):
        students_dBDump = self.read_all_students_from_db()

        #baue Liste von Personen aus DB Dump
        students_list =[]
        for row in students_dBDump:
            new_student = Student()
            new_student.person_id = row[0]
            new_student.first_name = row[1]
            new_student.last_name = row[2]
            new_student.email = row[3]
            new_student.student_id = row[4]
            new_student.company = row[5]
            new_student.mat_number = row[6]
            new_student.enrolled = bool(row[7])
            new_student.creation_date = row[8]
            students_list.append(new_student)

        return students_list


    def read_all_students_from_db(self):
        self.cursor.execute('SELECT persons.personId, persons.firstName, persons.lastName, persons.eMail, students.studentId, students.company, students.matNumber, students.enrolled, students.creationDate FROM persons JOIN students ON persons.personId = students.personId')
        return self.cursor.fetchall()
    
    def read_all_students_by_course_id(self, course_id):
        students_dBDump = self.read_all_students_by_course_id_from_db(course_id)

        #baue Liste von Personen aus DB Dump
        students_list =[]
        for row in students_dBDump:
            new_student = Student()
            new_student.person_id = row[0]
            new_student.first_name = row[1]
            new_student.last_name = row[2]
            new_student.email = row[3]
            new_student.student_id = row[4]
            new_student.company = row[5]
            new_student.mat_number = row[6]
            new_student.enrolled = bool(row[7])
            new_student.creation_date = row[8]
            students_list.append(new_student)

        return students_list

    def read_all_students_by_course_id_from_db(self, course_id):
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
            ''',(course_id,))
        return self.cursor.fetchall()

    def read_student_by_id(self, student_id):
        # Studentendaten holen
        student = Student()
        student_dBDump = self.read_student_from_db(student_id)

        if student_dBDump:
            student.student_id = student_dBDump[0]
            student.person_id = student_dBDump[1]
            student.company  = student_dBDump[2]
            student.mat_number = student_dBDump[3]
            student.enrolled = bool(student_dBDump[4])

            # Personendaten ergaenzen
            student_person = self.read_person_by_id(student.person_id)

            student.last_name = student_person.last_name
            student.first_name = student_person.first_name
            student.email = student_person.email

            return student
        else: 
            return None

    def read_student_from_db(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE studentId = ?',(student_id,))
        return self.cursor.fetchone()

    def read_student_by_person_id(self, person_id):
        # Studentendaten holen
        student = Student()
        student_dBDump = self.read_student_from_db_by_person_id(person_id)

        if student_dBDump:
            student.student_id = student_dBDump[0]
            student.person_id = student_dBDump[1]
            student.company = student_dBDump[2]
            student.mat_number = student_dBDump[3]
            student.enrolled = bool(student_dBDump[4])

            # Personendaten ergaenzen
            student_person = self.read_person_by_id(student.person_id)

            student.last_name = student_person.last_name
            student.first_name = student_person.first_name
            student.email = student_person.email

            return student
        else: 
            return None

    def read_student_from_db_by_person_id(self, person_id):
        self.cursor.execute('SELECT * FROM students WHERE personId = ?',(person_id,))
        return self.cursor.fetchone()
    
    def read_student_by_name(self, last_name, first_name):
        # zuerst die Person holen:
        person = self.read_person_by_name(last_name, first_name)

        if person:
            # jetzt studentendaten ergänzen
            return self.read_student_by_person_id(person.person_id)
        else:
            return None

    def update_student(self, student_id, person_id, new_last_name, new_first_name, new_email, new_company, new_mat_number, new_enrolled):
        self.update_person(person_id, new_last_name, new_first_name, new_email)

        # Aktualisiere die Informationen des Studenten
        self.cursor.execute('''
            UPDATE students
            SET company = ?,
                matNumber = ?,
                enrolled = ?
            WHERE studentId = ?
        ''', (new_company, new_mat_number, new_enrolled, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        # Lösche den Studenten (Person wird automatisch gelöscht durch Fremdschlüsselbeziehung)
        self.cursor.execute('DELETE FROM students WHERE studentId = ?', (student_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Lecturer(Person):
    def __init__(self):
        self.lecturer_id = None
        self.company = None
        self.connect_to_database()

    def create_lecturer(self, last_name, first_name, email, company):
        new_lecturer = Lecturer()
        new_lecturer.first_name = first_name
        new_lecturer.last_name = last_name
        new_lecturer.email = email
        new_lecturer.company = company

        # Erstelle eine neue Person
        lecturer_person = self.create_person(last_name, first_name, email)
        new_lecturer.person_id = lecturer_person.person_id

        # Schreibe Dozenten in die Dozentendatenbank
        new_lecturer.lecturer_id = self.write_lecturer_to_db(lecturer_person.person_id, company)

        return new_lecturer

    def write_lecturer_to_db(self, person_id, company):
        # Füge den Dozenten hinzu
        self.cursor.execute('''
            INSERT INTO lecturers (personId, company)
            VALUES (?, ?)
        ''', (person_id, company))
        self.conn.commit()

        return self.cursor.lastrowid

    def read_all_lecturers(self):
        lecturers_dBDump = self.read_all_lecturers_from_db()

        # Baue Liste von Dozenten aus DB Dump
        lecturers_list = []
        for row in lecturers_dBDump:
            new_lecturer = Lecturer()
            new_lecturer.person_id = row[0]
            new_lecturer.first_name = row[1]
            new_lecturer.last_name = row[2]
            new_lecturer.email = row[3]
            new_lecturer.lecturer_id = row[4]
            new_lecturer.company = row[5]
            new_lecturer.creation_date = row[6]
            lecturers_list.append(new_lecturer)

        return lecturers_list

    def read_all_lecturers_from_db(self):
        self.cursor.execute('SELECT persons.personId, persons.firstName, persons.LastName, persons.eMail, lecturers.lecturerId, lecturers.company, lecturers.creationDate FROM persons JOIN lecturers ON persons.personId = lecturers.personId')
        return self.cursor.fetchall()

    def read_lecturer_by_id(self, lecturer_id):
        # Dozentendaten holen
        lecturer = Lecturer()
        lecturer_dBDump = self.read_lecturer_from_db(lecturer_id)

        if lecturer_dBDump:
            lecturer.lecturer_id = lecturer_dBDump[0]
            lecturer.person_id = lecturer_dBDump[1]
            lecturer.company = lecturer_dBDump[2]

            # Personendaten ergänzen
            lecturer_person = self.read_person_by_id(lecturer.person_id)

            lecturer.last_name = lecturer_person.last_name
            lecturer.first_name = lecturer_person.first_name
            lecturer.email = lecturer_person.email

            return lecturer
        else:
            return None

    def read_lecturer_from_db(self, lecturer_id):
        self.cursor.execute('SELECT * FROM lecturers WHERE lecturerId = ?', (lecturer_id,))
        return self.cursor.fetchone()
    
    def read_lecturer_by_person_id(self, person_id):
        # Dozentendaten holen
        lecturer = Lecturer()
        lecturer_dBDump = self.read_lecturer_from_db_by_person_id(person_id)

        if lecturer_dBDump:
            lecturer.lecturer_id = lecturer_dBDump[0]
            lecturer.person_id = lecturer_dBDump[1]
            lecturer.company = lecturer_dBDump[2]

            # Personendaten ergänzen
            lecturer_person = self.read_person_by_id(lecturer.person_id)

            lecturer.last_name = lecturer_person.last_name
            lecturer.first_name = lecturer_person.first_name
            lecturer.email = lecturer_person.email

            return lecturer
        else:
            return None
    
    def read_lecturer_from_db_by_person_id(self, person_id):
        self.cursor.execute('SELECT * FROM lecturers WHERE personId = ?', (person_id,))
        return self.cursor.fetchone()
    
    def read_lecturer_by_name(self, last_name, first_name):
        # zuerst die Person holen:
        person = self.read_person_by_name(last_name, first_name)

        if person:
            # jetzt Dozentendaten ergänzen
            return self.read_lecturer_by_person_id(person.person_id)
        else:
            return None

    def update_lecturer(self, lecturer_id, person_id, new_last_name, new_first_name, new_email, new_company):
        self.update_person(person_id, new_last_name, new_first_name, new_email)

        # Aktualisiere die Informationen des Dozenten
        self.cursor.execute('''
            UPDATE lecturers
            SET company = ?
            WHERE lecturerId = ?
        ''', (new_company, lecturer_id))
        self.conn.commit()

    def delete_lecturer(self, lecturer_id):
        # Lösche den Dozenten (Person wird automatisch gelöscht durch Fremdschlüsselbeziehung)
        self.cursor.execute('DELETE FROM lecturers WHERE lecturerId = ?', (lecturer_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Course:
    def __init__(self):
        self.course_id = None
        self.course_name = None
        self.start_date = None
        self.creation_date = None

        self.connect_to_database()
    
    def create_course(self,course_name, start_date):
        new_course = Course()
        new_course.course_name = course_name
        new_course.start_date = start_date

        new_course.course_id = self.write_course_to_dB(course_name, start_date)

        return new_course
    
    def write_course_to_dB(self, course_name, start_date):
        # Füge den Kurs zur Datenbank hinzu
        self.cursor.execute('''
            INSERT INTO courses (courseName, startDate)
            VALUES (?, ?)
        ''', (course_name, start_date))
        self.conn.commit()

        return self.cursor.lastrowid
    
    def read_course_by_id(self,course_id):
        # Kursdaten holen
        course = Course()
        course_dBDump = self.read_course_from_db(course_id)

        if course_dBDump:
            course.course_id = course_dBDump[0]
            course.course_name = course_dBDump[1]
            course.start_date = course_dBDump[2]
            course.creation_date = course_dBDump[3]

            return course
        else:
            return None

    def read_course_from_db(self, course_id):
        self.cursor.execute('SELECT * FROM courses WHERE courseId = ?', (course_id,))
        return self.cursor.fetchone()
    
    def read_all_courses(self):
        courses_dBDump = self.read_all_courses_from_db()

        # Baue Liste von Dozenten aus DB Dump
        courses_list = []
        for row in courses_dBDump:
            new_course = Course()
            new_course.course_id = row[0]
            new_course.course_name = row[1]
            new_course.start_date = row[2]
            new_course.creation_date = row[3]
            courses_list.append(new_course)

        return courses_list

    def read_all_courses_from_db(self):
        self.cursor.execute('SELECT * FROM courses')
        return self.cursor.fetchall()

    def update_course(self, course_id, course_name, start_date):
        # Aktualisiere die Informationen des Kurses
        self.cursor.execute('''
            UPDATE courses
            SET courseName = ?,
                startDate = ?
            WHERE courseId = ?
        ''', (course_name, start_date, course_id))
        self.conn.commit()

    def delete_course(self, course_id):
        # Lösche den Kurs
        self.cursor.execute('DELETE FROM courses WHERE courseId = ?', (course_id,))
        self.conn.commit()

    def read_all_enrolled_students(self):
        # alle enrollenments zum Kurs holen
        enrollments_db_dump = self.cursor.execute('SELECT * FROM enrollments WHERE courseId = ?', (self.course_id,))

        enrollments_list = []
        for row in enrollments_db_dump:
            new_enrollment = Enrollments()
            new_enrollment.enrollment_id = row[0]
            new_enrollment.student_id = row[1]
            new_enrollment.course_id = row[2]
            enrollments_list.append(new_enrollment)

        # jetzt aus den enrollments die Studenten in eine Liste packen
        students_list = []

        for enrollment in enrollments_list:
            new_student = Student()
            new_student.read_student_by_id(enrollment.student_id)
            students_list.append(new_student)

        return students_list


    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class Enrollments:
    def __init__(self):
        self.enrollment_id = None
        self.student_id = None
        self.course_id = None

        self.connect_to_database()

    def add_student_to_course(self, student_id, course_id):
        self.cursor.execute('''
            INSERT INTO enrollments (studentId, courseId)
            VALUES (?, ?)
        ''', (student_id, course_id))
        self.conn.commit()

    def read_enrollment_by_id(self,enrollment_id):
        # Kursdaten holen
        enrollment = Enrollments()
        enrollment_dBDump = self.read_enrollment_from_db(enrollment_id)

        if enrollment_dBDump:
            enrollment.enrollment_id = enrollment_dBDump[0]
            enrollment.student_id = enrollment_dBDump[1]
            enrollment.course_id = enrollment_dBDump[2]

            return enrollment
        else:
            return None

    def read_enrollment_from_db(self, enrollment_id):
        self.cursor.execute('SELECT * FROM enrollments WHERE enrollmentId = ?', (enrollment_id,))
        return self.cursor.fetchone()

    def read_all_enrollments(self):
        enrollments_dBDump = self.read_all_enrollments_from_db()

        # Baue Liste von Enrollments aus DB Dump
        enrollments_list = []
        for row in enrollments_dBDump:
            new_enrollment = Enrollments()
            new_enrollment.enrollment_id = row[0]
            new_enrollment.student_id = row[1]
            new_enrollment.course_id = row[2]
            enrollments_list.append(new_enrollment)

        return enrollments_list

    def read_all_enrollments_from_db(self):
        self.cursor.execute('SELECT * FROM enrollments')
        return self.cursor.fetchall()
    
    def read_all_enrollments_by_student_id(self, student_id):
        enrollments_dBDump = self.read_all_enrollments_by_student_id_from_db(student_id)

        # Baue Liste von Enrollments aus DB Dump
        enrollments_list = []
        for row in enrollments_dBDump:
            new_enrollment = Enrollments()
            new_enrollment.enrollment_id = row[0]
            new_enrollment.student_id = row[1]
            new_enrollment.course_id = row[2]
            enrollments_list.append(new_enrollment)

        return enrollments_list

    def read_all_enrollments_by_student_id_from_db(self, student_id):
        self.cursor.execute('SELECT * FROM enrollments WHERE studentId = ?', (student_id, ))
        return self.cursor.fetchall()
    
    def update_enrollment(self, enrollment_id, student_id, course_id):
        # Aktualisiere die Informationen des Kurses
        self.cursor.execute('''
            UPDATE enrollments
            SET studentId = ?,
                courseId = ?
            WHERE enrollmentId = ?
        ''', (student_id, course_id, enrollment_id))
        self.conn.commit()

    def delete_enrollment(self, enrollment_id):
        # Lösche den Kurs
        self.cursor.execute('DELETE FROM enrollments WHERE enrollmentId = ?', (enrollment_id,))
        self.conn.commit()  

    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class Assignments:
    def __init__(self):
        self.assignment_id = None
        self.student_id = None
        self.lecturer_id = None
        self.type = None
        self.topic = None
        self.grade = None
        self.date = None
        self.time = None

        self.connect_to_database()

    def create_assignment(self, student_id, lecturer_id, type, topic, grade, date, time):
        new_assignment = Assignments()
        new_assignment.student_id = student_id
        new_assignment.lecturer_id = lecturer_id
        new_assignment.type = type
        new_assignment.topic = topic
        new_assignment.grade = grade
        new_assignment.date = date
        new_assignment.time = time

        new_assignment.assignment_id = self.write_assignment_to_dB(student_id, lecturer_id, type, topic, grade, date, time)

        return new_assignment
    
    def write_assignment_to_dB(self, student_id, lecturer_id, type, topic, grade, date, time):
        real_grade = str(grade).replace(",",".")
        # Füge das Assignment zur Datenbank hinzu
        self.cursor.execute('''
            INSERT INTO assignments (studentId, lecturerId, type, topic, grade, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, lecturer_id, type, topic, real_grade, date, time))
        self.conn.commit()

        return self.cursor.lastrowid

    def add_student_to_assignment(self, student_id, assignment_id):
        self.cursor.execute('''
            INSERT INTO assignments (studentId)
            VALUES (?)
            WHERE assignmentId = ?
        ''', (student_id, assignment_id))
        self.conn.commit()

    def add_lecturer_to_assignment(self, lecturer_id, assignment_id):
        self.cursor.execute('''
            INSERT INTO assignments (lecturerId)
            VALUES (?)
            WHERE assignmentId = ?
        ''', (lecturer_id, assignment_id))
        self.conn.commit()

    def read_assignment_by_id(self, assignment_id):
        # Daten holen
        assignment_dBDump = self.read_assignment_from_db_by_id(assignment_id)

        if assignment_dBDump:
            return self.create_assignment_from_db_dump(assignment_dBDump)
        else:
            return None

    def read_assignment_from_db_by_id(self, assignment_id):
        self.cursor.execute('SELECT * FROM assignments WHERE assignmentId = ?', (assignment_id,))
        return self.cursor.fetchone()

    def read_assignment_by_student_id_and_type(self, student_id, assignment_type):
        # Daten holen
        assignment_dBDump = self.read_assignment_from_db_by_student_id_and_type(student_id, assignment_type)

        if assignment_dBDump:
            return self.create_assignment_from_db_dump(assignment_dBDump)
        else:
            return None

    def read_assignment_from_db_by_student_id_and_type(self, student_id, assignment_type):
        self.cursor.execute('SELECT * FROM assignments WHERE studentId = ? AND type = ?', (student_id, assignment_type,))
        return self.cursor.fetchone()

    def read_all_assignments(self):
        assignments_dBDump = self.read_all_assignments_from_db()

        assignments_list = []
        for row in assignments_dBDump:
            new_assignment = self.create_assignment_from_db_dump(row)
            assignments_list.append(new_assignment)

        return assignments_list

    def read_all_assignments_from_db(self):
        self.cursor.execute('SELECT * FROM Assignments')
        return self.cursor.fetchall()

    def read_all_assignments_by_student_id(self, student_id):
        assignments_dBDump = self.read_all_assignments_by_student_id_from_db(student_id)

        Assignments_list = []
        for row in assignments_dBDump:
            new_assignment = self.create_assignment_from_db_dump(row)
            Assignments_list.append(new_assignment)

        return Assignments_list
    
    def create_assignment_from_db_dump(self, assignment_dump):
        # Assignment aus DB Dump
        
        new_assignment = Assignments()
        new_assignment.assignment_id = assignment_dump[0]
        new_assignment.student_id = assignment_dump[1]
        new_assignment.lecturer_id = assignment_dump[2]
        new_assignment.type = assignment_dump[3]
        new_assignment.topic = assignment_dump[4]
        if str(assignment_dump[5]) == "None":
            new_assignment.grade = None
        else:
            new_assignment.grade = str(assignment_dump[5]).replace(".",",")
        new_assignment.date = assignment_dump[6]
        new_assignment.time = assignment_dump[7]
        
        return new_assignment

    def read_all_assignments_by_student_id_from_db(self, student_id):
        self.cursor.execute('SELECT * FROM assignments WHERE studentId = ?', (student_id, ))
        return self.cursor.fetchall()

    def update_assignment(self, assignment_id, student_id, lecturer_id, type, topic, grade, date, time):
        # Aktualisiere die Informationen der Arbeit
        real_grade = str(grade).replace(",",".")
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
        ''', (student_id, lecturer_id, type, topic, real_grade, date, time, assignment_id))
        self.conn.commit()

    def delete_assignment(self, assignment_id):
        # Lösche den Kurs
        self.cursor.execute('DELETE FROM assignments WHERE assignmentId = ?', (assignment_id,))
        self.conn.commit()  

    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

class LastUsedItems():
    def __init__(self):
        self.type = None
        self.elements = None
        
        self.connect_to_database()

    def create_last_used_item(self, type, elements):
        new_last_used_item = LastUsedItems()
        new_last_used_item.type = type
        new_last_used_item.elements = elements

        elements_as_string = ','.join(map(str, elements))

        self.write_last_used_item_to_dB(type, elements_as_string)

        return new_last_used_item
    
    def write_last_used_item_to_dB(self, type, elements_string):
        self.cursor.execute('''
            INSERT INTO lastUsedItems (type, elements)
            VALUES (?, ?)
        ''', (type, elements_string, ))
        self.conn.commit() 

    def read_last_used_item_by_type(self, type):
        self.cursor.execute('SELECT * FROM lastUsedItems WHERE type = ?', (type, ))
        last_used_item_dBDump = self.cursor.fetchone()

        if last_used_item_dBDump:
            new_last_used_item = LastUsedItems()
            new_last_used_item.type = last_used_item_dBDump[0]
            new_last_used_item.elements = list(map(str, last_used_item_dBDump[1].split(',')))

            return new_last_used_item
        else: 
            return None
    
    def update_last_used_item(self, type, elements):
        elements_as_string = ','.join(map(str, elements))
        self.cursor.execute('''
            UPDATE lastUsedItems
            SET elements = ?
            WHERE type = ?
        ''', (elements_as_string, type))
        self.conn.commit()

    def delete_all_last_used_elements(self):
        self.cursor.execute('DELETE FROM lastUsedItems')
        self.conn.commit()


    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

