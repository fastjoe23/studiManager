import pytest
from studentModel import Course, Student, Enrollments

@pytest.fixture
def course_instance():
    return Course()

@pytest.fixture
def student_instance1():
    return Student()

@pytest.fixture
def student_instance2():
    return Student()

@pytest.fixture
def enrollments_instance():
    return Enrollments()

def test_createEnrollment(course_instance, student_instance1, student_instance2, enrollments_instance):
    # Kurs erstellen
    course = course_instance.createCourse("Enrollment TestCourse", "2020-02-01")
    # Studenten erstellen
    student1 = student_instance1.createStudent("Rabbit Of", "Enrollland", "rabbit@example.com", "Rabbits nCo", 4567, False)
    student2 = student_instance2.createStudent("Isaac", "Enrollton", "isaac@newton.com", "Physics.com", 1, True)

    # Studenten in Kurs einschreiben
    _ = enrollments_instance.addStudentToCourse(student1.studentId, course.courseId)
    _ = enrollments_instance.addStudentToCourse(student2.studentId, course.courseId)

    # checken ob Studenten im Kurs
    enrolledStudents = student_instance1.readAllStudentsByCourseId(course.courseId)

    assert isinstance(enrolledStudents, list)







