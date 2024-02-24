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
        self.last_used_items = LastUsedItems()
        self.note = Notes()


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

        new_person.person_id = self.write_person_to_db(last_name, first_name, email)

        return new_person

    def write_person_to_db(self, last_name, first_name, email):
        self.cursor.execute(
            """
            INSERT INTO persons (last_name, first_name, email)
            VALUES (?, ?, ?)
        """,
            (last_name, first_name, email),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def read_all_persons(self):
        persons_dbdump = self.read_all_persons_from_db()

        # baue Liste von Personen aus DB Dump
        persons_list = []
        for row in persons_dbdump:
            new_person = Person()
            new_person.person_id = row[0]
            new_person.first_name = row[1]
            new_person.last_name = row[2]
            new_person.email = row[3]
            new_person.creation_date = row[4]
            persons_list.append(new_person)

        return persons_list

    def read_all_persons_from_db(self):
        self.cursor.execute("SELECT * FROM persons")
        return self.cursor.fetchall()

    def read_person_by_id(self, person_id):
        person = Person()
        person_dbdump = self.read_person_by_person_id_from_db(person_id)

        if person_dbdump:
            person.person_id = person_dbdump[0]
            person.first_name = person_dbdump[1]
            person.last_name = person_dbdump[2]
            person.email = person_dbdump[3]
            person.creation_date = person_dbdump[4]
            return person
        else:
            return None

    def read_person_by_person_id_from_db(self, person_id):
        self.cursor.execute("SELECT * FROM persons WHERE person_id = ?", (person_id,))
        return self.cursor.fetchone()

    def read_person_by_name(self, last_name, first_name):
        person = Person()
        person_dbdump = self.read_person_by_name_from_db(last_name, first_name)

        if person_dbdump:
            person.person_id = person_dbdump[0]
            person.first_name = person_dbdump[1]
            person.last_name = person_dbdump[2]
            person.email = person_dbdump[3]
            person.creation_date = person_dbdump[4]
            return person
        else:
            return None

    def read_person_by_name_from_db(self, last_name, first_name):
        self.cursor.execute(
            "SELECT * FROM persons WHERE first_name = ? AND last_name = ?",
            (
                first_name,
                last_name,
            ),
        )
        return self.cursor.fetchone()

    def update_person(self, person_id, new_last_name, new_first_name, new_email):
        self.cursor.execute(
            """
            UPDATE persons
            SET last_name = ?,
                first_name = ?,
                email = ?
            WHERE person_id = ?
        """,
            (new_last_name, new_first_name, new_email, person_id),
        )
        self.conn.commit()

    def delete_person(self, person_id):
        self.cursor.execute("DELETE FROM persons WHERE person_id = ?", (person_id,))
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
        super().__init__()
        self.student_id = None
        self.company = None
        self.mat_number = None
        self.enrolled = False
        self.connect_to_database()

    def create_student(
        self, last_name, first_name, email, company, mat_number, enrolled
    ):
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
        new_student.student_id = self.write_student_to_db(
            student_person.person_id, company, mat_number, enrolled
        )

        return new_student

    def write_student_to_db(self, person_id, company, mat_number, enrolled):
        # Füge den Studenten hinzu
        self.cursor.execute(
            """
            INSERT INTO students (person_id, company, mat_number, enrolled)
            VALUES (?, ?, ?, ?)
        """,
            (person_id, company, mat_number, enrolled),
        )
        self.conn.commit()

        return self.cursor.lastrowid

    def read_all_students(self):
        students_dbdump = self.read_all_students_from_db()

        # baue Liste von Personen aus DB Dump
        students_list = []
        for row in students_dbdump:
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
        self.cursor.execute('''
            SELECT persons.person_id,
                    persons.first_name,
                    persons.last_name,
                    persons.eMail,
                    students.student_id,
                    students.company,
                    students.mat_number,
                    students.enrolled,
                    students.creation_date FROM persons
                    JOIN students ON persons.person_id = students.person_id
        ''')
        return self.cursor.fetchall()

    def read_all_students_by_course_id(self, course_id):
        students_dbdump = self.read_all_students_by_course_id_from_db(course_id)

        # baue Liste von Personen aus DB Dump
        students_list = []
        for row in students_dbdump:
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
        self.cursor.execute(
            """
            SELECT
                persons.person_id,
                persons.first_name,
                persons.last_name,
                persons.eMail,
                students.student_id,
                students.company,
                students.mat_number,
                students.enrolled,
                students.creation_date
            FROM persons
            JOIN students ON persons.person_id = students.person_id
            WHERE students.student_id IN (SELECT enrollments.student_id FROM enrollments WHERE enrollments.course_id = ?)
            """,
            (course_id,),
        )
        return self.cursor.fetchall()

    def read_student_by_id(self, student_id):
        # Studentendaten holen
        student = Student()
        student_dbdump = self.read_student_from_db(student_id)

        if student_dbdump:
            student.student_id = student_dbdump[0]
            student.person_id = student_dbdump[1]
            student.company = student_dbdump[2]
            student.mat_number = student_dbdump[3]
            student.enrolled = bool(student_dbdump[4])

            # Personendaten ergaenzen
            student_person = self.read_person_by_id(student.person_id)

            student.last_name = student_person.last_name
            student.first_name = student_person.first_name
            student.email = student_person.email

            return student
        else:
            return None

    def read_student_from_db(self, student_id):
        self.cursor.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        )
        return self.cursor.fetchone()

    def read_student_by_person_id(self, person_id):
        # Studentendaten holen
        student = Student()
        student_db_dump = self.read_student_from_db_by_person_id(person_id)

        if student_db_dump:
            student.student_id = student_db_dump[0]
            student.person_id = student_db_dump[1]
            student.company = student_db_dump[2]
            student.mat_number = student_db_dump[3]
            student.enrolled = bool(student_db_dump[4])

            # Personendaten ergaenzen
            student_person = self.read_person_by_id(student.person_id)

            student.last_name = student_person.last_name
            student.first_name = student_person.first_name
            student.email = student_person.email

            return student
        else:
            return None

    def read_student_from_db_by_person_id(self, person_id):
        self.cursor.execute("SELECT * FROM students WHERE person_id = ?", (person_id,))
        return self.cursor.fetchone()

    def read_student_by_name(self, last_name, first_name):
        # zuerst die Person holen:
        person = self.read_person_by_name(last_name, first_name)

        if person:
            # jetzt studentendaten ergänzen
            return self.read_student_by_person_id(person.person_id)
        else:
            return None

    def update_student(
        self,
        student_id,
        person_id,
        new_last_name,
        new_first_name,
        new_email,
        new_company,
        new_mat_number,
        new_enrolled,
    ):
        self.update_person(person_id, new_last_name, new_first_name, new_email)

        # Aktualisiere die Informationen des Studenten
        self.cursor.execute(
            """
            UPDATE students
            SET company = ?,
                mat_number = ?,
                enrolled = ?
            WHERE student_id = ?
        """,
            (new_company, new_mat_number, new_enrolled, student_id),
        )
        self.conn.commit()

    def delete_student(self, student_id):
        # Lösche den Studenten (Person wird automatisch gelöscht durch Fremdschlüsselbeziehung)
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class Lecturer(Person):
    def __init__(self):
        super().__init__()
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
        new_lecturer.lecturer_id = self.write_lecturer_to_db(
            lecturer_person.person_id, company
        )

        return new_lecturer

    def write_lecturer_to_db(self, person_id, company):
        # Füge den Dozenten hinzu
        self.cursor.execute(
            """
            INSERT INTO lecturers (person_id, company)
            VALUES (?, ?)
        """,
            (person_id, company),
        )
        self.conn.commit()

        return self.cursor.lastrowid

    def read_all_lecturers(self):
        lecturers_dbdump = self.read_all_lecturers_from_db()

        # Baue Liste von Dozenten aus DB Dump
        lecturers_list = []
        for row in lecturers_dbdump:
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
        self.cursor.execute(
            '''SELECT persons.person_id,
                      persons.first_name,
                      persons.last_name,
                      persons.eMail,
                      lecturers.lecturer_id,
                      lecturers.company,
                      lecturers.creation_date FROM persons
                      JOIN lecturers ON persons.person_id = lecturers.person_id
        ''')
        return self.cursor.fetchall()

    def read_lecturer_by_id(self, lecturer_id):
        # Dozentendaten holen
        lecturer = Lecturer()
        lecturer_dbdump = self.read_lecturer_from_db(lecturer_id)

        if lecturer_dbdump:
            lecturer.lecturer_id = lecturer_dbdump[0]
            lecturer.person_id = lecturer_dbdump[1]
            lecturer.company = lecturer_dbdump[2]

            # Personendaten ergänzen
            lecturer_person = self.read_person_by_id(lecturer.person_id)

            lecturer.last_name = lecturer_person.last_name
            lecturer.first_name = lecturer_person.first_name
            lecturer.email = lecturer_person.email

            return lecturer
        else:
            return None

    def read_lecturer_from_db(self, lecturer_id):
        self.cursor.execute(
            "SELECT * FROM lecturers WHERE lecturer_id = ?", (lecturer_id,)
        )
        return self.cursor.fetchone()

    def read_lecturer_by_person_id(self, person_id):
        # Dozentendaten holen
        lecturer = Lecturer()
        lecturer_dbdump = self.read_lecturer_from_db_by_person_id(person_id)

        if lecturer_dbdump:
            lecturer.lecturer_id = lecturer_dbdump[0]
            lecturer.person_id = lecturer_dbdump[1]
            lecturer.company = lecturer_dbdump[2]

            # Personendaten ergänzen
            lecturer_person = self.read_person_by_id(lecturer.person_id)

            lecturer.last_name = lecturer_person.last_name
            lecturer.first_name = lecturer_person.first_name
            lecturer.email = lecturer_person.email

            return lecturer
        else:
            return None

    def read_lecturer_from_db_by_person_id(self, person_id):
        self.cursor.execute("SELECT * FROM lecturers WHERE person_id = ?", (person_id,))
        return self.cursor.fetchone()

    def read_lecturer_by_name(self, last_name, first_name):
        # zuerst die Person holen:
        person = self.read_person_by_name(last_name, first_name)

        if person:
            # jetzt Dozentendaten ergänzen
            return self.read_lecturer_by_person_id(person.person_id)
        else:
            return None

    def update_lecturer(
        self,
        lecturer_id,
        person_id,
        new_last_name,
        new_first_name,
        new_email,
        new_company,
    ):
        self.update_person(person_id, new_last_name, new_first_name, new_email)

        # Aktualisiere die Informationen des Dozenten
        self.cursor.execute(
            """
            UPDATE lecturers
            SET company = ?
            WHERE lecturer_id = ?
        """,
            (new_company, lecturer_id),
        )
        self.conn.commit()

    def delete_lecturer(self, lecturer_id):
        # Lösche den Dozenten (Person wird automatisch gelöscht durch Fremdschlüsselbeziehung)
        self.cursor.execute(
            "DELETE FROM lecturers WHERE lecturer_id = ?", (lecturer_id,)
        )
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

    def create_course(self, course_name, start_date):
        new_course = Course()
        new_course.course_name = course_name
        new_course.start_date = start_date

        new_course.course_id = self.write_course_to_db(course_name, start_date)

        return new_course

    def write_course_to_db(self, course_name, start_date):
        # Füge den Kurs zur Datenbank hinzu
        self.cursor.execute(
            """
            INSERT INTO courses (course_name, start_date)
            VALUES (?, ?)
        """,
            (course_name, start_date),
        )
        self.conn.commit()

        return self.cursor.lastrowid

    def read_course_by_id(self, course_id):
        # Kursdaten holen
        course = Course()
        course_dbdump = self.read_course_from_db(course_id)

        if course_dbdump:
            course.course_id = course_dbdump[0]
            course.course_name = course_dbdump[1]
            course.start_date = course_dbdump[2]
            course.creation_date = course_dbdump[3]

            return course
        else:
            return None

    def read_course_from_db(self, course_id):
        self.cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        return self.cursor.fetchone()

    def read_all_courses(self):
        courses_dbdump = self.read_all_courses_from_db()

        # Baue Liste von Dozenten aus DB Dump
        courses_list = []
        for row in courses_dbdump:
            new_course = Course()
            new_course.course_id = row[0]
            new_course.course_name = row[1]
            new_course.start_date = row[2]
            new_course.creation_date = row[3]
            courses_list.append(new_course)

        return courses_list

    def read_all_courses_from_db(self):
        self.cursor.execute("SELECT * FROM courses")
        return self.cursor.fetchall()

    def update_course(self, course_id, course_name, start_date):
        # Aktualisiere die Informationen des Kurses
        self.cursor.execute(
            """
            UPDATE courses
            SET course_name = ?,
                start_date = ?
            WHERE course_id = ?
        """,
            (course_name, start_date, course_id),
        )
        self.conn.commit()

    def delete_course(self, course_id):
        # Lösche den Kurs
        self.cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
        self.conn.commit()

    def read_all_enrolled_students(self):
        # alle enrollenments zum Kurs holen
        enrollments_db_dump = self.cursor.execute(
            "SELECT * FROM enrollments WHERE course_id = ?", (self.course_id,)
        )

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
        self.cursor.execute(
            """
            INSERT INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        """,
            (student_id, course_id),
        )
        self.conn.commit()

    def read_enrollment_by_id(self, enrollment_id):
        # Kursdaten holen
        enrollment = Enrollments()
        enrollment_dbdump = self.read_enrollment_from_db(enrollment_id)

        if enrollment_dbdump:
            enrollment.enrollment_id = enrollment_dbdump[0]
            enrollment.student_id = enrollment_dbdump[1]
            enrollment.course_id = enrollment_dbdump[2]

            return enrollment
        else:
            return None

    def read_enrollment_from_db(self, enrollment_id):
        self.cursor.execute(
            "SELECT * FROM enrollments WHERE enrollment_id = ?", (enrollment_id,)
        )
        return self.cursor.fetchone()

    def read_all_enrollments(self):
        enrollments_dbdump = self.read_all_enrollments_from_db()

        # Baue Liste von Enrollments aus DB Dump
        enrollments_list = []
        for row in enrollments_dbdump:
            new_enrollment = Enrollments()
            new_enrollment.enrollment_id = row[0]
            new_enrollment.student_id = row[1]
            new_enrollment.course_id = row[2]
            enrollments_list.append(new_enrollment)

        return enrollments_list

    def read_all_enrollments_from_db(self):
        self.cursor.execute("SELECT * FROM enrollments")
        return self.cursor.fetchall()

    def read_all_enrollments_by_student_id(self, student_id):
        enrollments_dbdump = self.read_all_enrollments_by_student_id_from_db(student_id)

        # Baue Liste von Enrollments aus DB Dump
        enrollments_list = []
        for row in enrollments_dbdump:
            new_enrollment = Enrollments()
            new_enrollment.enrollment_id = row[0]
            new_enrollment.student_id = row[1]
            new_enrollment.course_id = row[2]
            enrollments_list.append(new_enrollment)

        return enrollments_list

    def read_all_enrollments_by_student_id_from_db(self, student_id):
        self.cursor.execute(
            "SELECT * FROM enrollments WHERE student_id = ?", (student_id,)
        )
        return self.cursor.fetchall()

    def update_enrollment(self, enrollment_id, student_id, course_id):
        # Aktualisiere die Informationen des Kurses
        self.cursor.execute(
            """
            UPDATE enrollments
            SET student_id = ?,
                course_id = ?
            WHERE enrollment_id = ?
        """,
            (student_id, course_id, enrollment_id),
        )
        self.conn.commit()

    def delete_enrollment(self, enrollment_id):
        # Lösche den Kurs
        self.cursor.execute(
            "DELETE FROM enrollments WHERE enrollment_id = ?", (enrollment_id,)
        )
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

    def create_assignment(
        self, student_id, lecturer_id, assignment_type, topic, grade, date, time
    ):
        new_assignment = Assignments()
        new_assignment.student_id = student_id
        new_assignment.lecturer_id = lecturer_id
        new_assignment.type = assignment_type
        new_assignment.topic = topic
        new_assignment.grade = grade
        new_assignment.date = date
        new_assignment.time = time

        new_assignment.assignment_id = self.write_assignment_to_db(
            student_id, lecturer_id, assignment_type, topic, grade, date, time
        )

        return new_assignment

    def write_assignment_to_db(
        self, student_id, lecturer_id, assignment_type, topic, grade, date, time
    ):
        real_grade = str(grade).replace(",", ".")
        # Füge das Assignment zur Datenbank hinzu
        self.cursor.execute(
            """
            INSERT INTO assignments (student_id, lecturer_id, type, topic, grade, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (student_id, lecturer_id, assignment_type, topic, real_grade, date, time),
        )
        self.conn.commit()

        return self.cursor.lastrowid

    def add_student_to_assignment(self, student_id, assignment_id):
        self.cursor.execute(
            """
            INSERT INTO assignments (student_id)
            VALUES (?)
            WHERE assignment_id = ?
        """,
            (student_id, assignment_id),
        )
        self.conn.commit()

    def add_lecturer_to_assignment(self, lecturer_id, assignment_id):
        self.cursor.execute(
            """
            INSERT INTO assignments (lecturer_id)
            VALUES (?)
            WHERE assignment_id = ?
        """,
            (lecturer_id, assignment_id),
        )
        self.conn.commit()

    def read_assignment_by_id(self, assignment_id):
        # Daten holen
        assignment_dbdump = self.read_assignment_from_db_by_id(assignment_id)

        if assignment_dbdump:
            return self.create_assignment_from_db_dump(assignment_dbdump)
        else:
            return None

    def read_assignment_from_db_by_id(self, assignment_id):
        self.cursor.execute(
            "SELECT * FROM assignments WHERE assignment_id = ?", (assignment_id,)
        )
        return self.cursor.fetchone()

    def read_assignment_by_student_id_and_type(self, student_id, assignment_type):
        # Daten holen
        assignment_dbdump = self.read_assignment_from_db_by_student_id_and_type(
            student_id, assignment_type
        )

        if assignment_dbdump:
            return self.create_assignment_from_db_dump(assignment_dbdump)
        else:
            return None

    def read_assignment_from_db_by_student_id_and_type(
        self, student_id, assignment_type
    ):
        self.cursor.execute(
            "SELECT * FROM assignments WHERE student_id = ? AND type = ?",
            (
                student_id,
                assignment_type,
            ),
        )
        return self.cursor.fetchone()

    def read_all_assignments(self):
        assignments_dbdump = self.read_all_assignments_from_db()

        assignments_list = []
        for row in assignments_dbdump:
            new_assignment = self.create_assignment_from_db_dump(row)
            assignments_list.append(new_assignment)

        return assignments_list

    def read_all_assignments_from_db(self):
        self.cursor.execute("SELECT * FROM Assignments")
        return self.cursor.fetchall()

    def read_all_assignments_by_student_id(self, student_id):
        assignments_dbdump = self.read_all_assignments_by_student_id_from_db(student_id)

        assignments_list = []
        for row in assignments_dbdump:
            new_assignment = self.create_assignment_from_db_dump(row)
            assignments_list.append(new_assignment)

        return assignments_list

    def read_all_assignments_by_student_id_from_db(self, student_id):
        self.cursor.execute(
            "SELECT * FROM assignments WHERE student_id = ?", (student_id,)
        )
        return self.cursor.fetchall()

    def read_all_assignments_by_lecturer_id(self, lecturer_id):
        assignments_dbdump = self.read_all_assignments_by_lecturer_id_from_db(
            lecturer_id
        )

        assignments_list = []
        for row in assignments_dbdump:
            new_assignment = self.create_assignment_from_db_dump(row)
            assignments_list.append(new_assignment)

        return assignments_list

    def read_all_assignments_by_lecturer_id_from_db(self, lecturer_id):
        self.cursor.execute(
            "SELECT * FROM assignments WHERE lecturer_id = ?", (lecturer_id,)
        )
        return self.cursor.fetchall()

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
            new_assignment.grade = str(assignment_dump[5]).replace(".", ",")
        new_assignment.date = assignment_dump[6]
        new_assignment.time = assignment_dump[7]

        return new_assignment

    def update_assignment(
        self, assignment_id, student_id, lecturer_id, assignment_type, topic, grade, date, time
    ):
        # Aktualisiere die Informationen der Arbeit
        real_grade = str(grade).replace(",", ".")
        self.cursor.execute(
            """
            UPDATE assignments
            SET student_id = ?,
                lecturer_id = ?,
                type = ?,
                topic = ?,
                grade = ?,
                date = ?,
                time = ?
            WHERE assignment_id = ?
        """,
            (
                student_id,
                lecturer_id,
                assignment_type,
                topic,
                real_grade,
                date,
                time,
                assignment_id,
            ),
        )
        self.conn.commit()

    def delete_assignment(self, assignment_id):
        # Lösche den Kurs
        self.cursor.execute(
            "DELETE FROM assignments WHERE assignment_id = ?", (assignment_id,)
        )
        self.conn.commit()

    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()


class LastUsedItems:
    def __init__(self):
        self.type = None
        self.elements = None

        self.connect_to_database()

    def create_last_used_item(self, item_type, elements):
        new_last_used_item = LastUsedItems()
        new_last_used_item.type = item_type
        new_last_used_item.elements = elements

        elements_as_string = ",".join(map(str, elements))

        self.write_last_used_item_to_db(item_type, elements_as_string)

        return new_last_used_item

    def write_last_used_item_to_db(self, item_type, elements_string):
        self.cursor.execute(
            """
            INSERT INTO lastUsedItems (type, elements)
            VALUES (?, ?)
        """,
            (
                item_type,
                elements_string,
            ),
        )
        self.conn.commit()

    def read_last_used_item_by_type(self, item_type):
        self.cursor.execute("SELECT * FROM lastUsedItems WHERE type = ?", (item_type,))
        last_used_item_dbdump = self.cursor.fetchone()

        if last_used_item_dbdump:
            new_last_used_item = LastUsedItems()
            new_last_used_item.type = last_used_item_dbdump[0]
            new_last_used_item.elements = list(
                map(str, last_used_item_dbdump[1].split(","))
            )

            return new_last_used_item
        else:
            return None

    def update_last_used_item(self, item_type, elements):
        elements_as_string = ",".join(map(str, elements))
        self.cursor.execute(
            """
            UPDATE lastUsedItems
            SET elements = ?
            WHERE type = ?
        """,
            (
                elements_as_string,
                item_type,
            ),
        )
        self.conn.commit()

    def delete_all_last_used_elements(self):
        self.cursor.execute("DELETE FROM lastUsedItems")
        self.conn.commit()

    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()


class Notes:
    def __init__(self):
        self.note_id = None
        self.note_type = None
        self.related_id = None
        self.note_title = None
        self.note = None
        self.creation_date = None
        self.last_modification_date = None
        self.conn = None
        self.cursor = None
        self.connect_to_database()

    def create_note(self, new_note):
        self.cursor.execute(
            """
            INSERT INTO notes (note_type, related_id, note_title, note, last_modification_date)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                new_note.note_type,
                new_note.related_id,
                new_note.note_title,
                new_note.note,
                new_note.last_modification_date,
            ),
        )
        self.conn.commit()

    def read_all_notes(self):
        notes_dbdump = self.read_all_notes_from_db()

        # baue Liste von Notizen aus DB Dump
        notes_list = []
        for row in notes_dbdump:
            new_note = Notes()
            new_note.note_id = row[0]
            new_note.note_type = row[1]
            new_note.related_id = row[2]
            new_note.note_title = row[3]
            new_note.note = row[4]
            new_note.creation_date = row[5]
            new_note.last_modification_date = row[6]
            notes_list.append(new_note)

        return notes_list

    def read_all_notes_from_db(self):
        self.cursor.execute("SELECT * FROM notes")
        return self.cursor.fetchall()

    def read_notes_by_type_and_related_id(self, note_type, related_id):
        self.cursor.execute(
            """
            SELECT * FROM notes
            WHERE note_type = ? AND related_id = ?
        """,
            (
                note_type,
                related_id,
            ),
        )
        notes_db_dump = self.cursor.fetchall()

        notes = []
        for row in notes_db_dump:
            note = Notes()
            note.note_id = row[0]
            note.note_type = row[1]
            note.related_id = row[2]
            note.note_title = row[3]
            note.note = row[4]
            note.creation_date = row[5]
            note.last_modification_date = row[6]
            notes.append(note)

        return notes

    def read_note_by_id(self, note_id):
        self.cursor.execute(
            """
                SELECT * FROM notes
                WHERE note_id = ?
                            """,
            (note_id,),
        )
        note_db_dumb = self.cursor.fetchone()

        note = Notes()
        note.note_id = note_db_dumb[0]
        note.note_type = note_db_dumb[1]
        note.related_id = note_db_dumb[2]
        note.note_title = note_db_dumb[3]
        note.note = note_db_dumb[4]
        note.creation_date = note_db_dumb[5]
        note.last_modification_date = note_db_dumb[6]

        return note

    def update_note_by_id(self, note_id, new_note):
        self.cursor.execute(
            """
            UPDATE notes
            SET note_title = ?,
            note = ?,
            last_modification_date = ?
            WHERE note_id = ?
        """,
            (
                new_note.note_title,
                new_note.note,
                new_note.last_modification_date,
                note_id,
            ),
        )
        self.conn.commit()

    def delete_note_by_id(self, note_id):
        self.cursor.execute(
            """
            DELETE FROM notes
            WHERE note_id = ?
        """,
            (note_id,),
        )
        self.conn.commit()

    def delete_all_notes(self):
        self.cursor.execute("DELETE FROM notes")
        self.conn.commit()

    def connect_to_database(self):
        configs = Config()
        database_name = configs.data_base_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
