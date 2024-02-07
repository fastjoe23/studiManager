import pytest
from studi_manager_model import Course, Student, Enrollments

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

def test_create_enrollment(course_instance, student_instance1, student_instance2, enrollments_instance):
    # Kurs erstellen
    course = course_instance.create_course("Enrollment Test_course", "2020-02-01")
    # Studenten erstellen
    student1 = student_instance1.create_student("Rabbit Of", "Enrollland", "rabbit@example.com", "Rabbits n_co", 4567, False)
    student2 = student_instance2.create_student("Isaac", "Enrollton", "isaac@newton.com", "Physics.com", 1, True)

    # Studenten in Kurs einschreiben
    _ = enrollments_instance.add_student_to_course(student1.student_id, course.course_id)
    _ = enrollments_instance.add_student_to_course(student2.student_id, course.course_id)

    # checken ob Studenten im Kurs
    enrolled_students = student_instance1.read_all_students_by_course_id(course.course_id)

    assert isinstance(enrolled_students, list)







