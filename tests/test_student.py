import pytest
from studentModel import Student

@pytest.fixture
def student_instance():
    return Student()

def test_create_student(student_instance):
    student = student_instance.createStudent("JohnStudentTest", "Doe", "john.doe@example.com", "Google", 12345, True)

    assert student.studentId is not None
    assert student.matNumber == 12345
    assert student.enrolled is True

def test_read_all_students(student_instance):
    students = student_instance.readAllStudents()

    assert isinstance(students, list)

def test_read_student_by_id(student_instance):
    student = student_instance.createStudent("AliceStudentTest", "Wonderland", "alice@example.com", "Daimler", 54321, False)
    retrieved_student = student_instance.readStudentById(student.studentId)

    assert retrieved_student is not None
    assert retrieved_student.studentId == student.studentId
    assert retrieved_student.lastName == "AliceStudentTest"
    assert retrieved_student.firstName == "Wonderland"
    assert retrieved_student.email == "alice@example.com"
    assert retrieved_student.company == "Daimler"
    assert retrieved_student.matNumber == 54321
    assert retrieved_student.enrolled is False

def test_update_student(student_instance):
    student = student_instance.createStudent("BobStudentTest", "Builder", "bob@example.com", "Bompany", 67890, True)
    student_instance.updateStudent(student.studentId, student.personId, "NewLastname", "NewNameStudentTest", "newemail@example.com", "NewCompany", 98765, False)

    updated_student = student_instance.readStudentById(student.studentId)

    assert updated_student.firstName == "NewNameStudentTest"
    assert updated_student.lastName == "NewLastname"
    assert updated_student.email == "newemail@example.com"
    assert updated_student.company == "NewCompany"
    assert updated_student.matNumber == 98765
    assert updated_student.enrolled is False

def test_delete_student(student_instance):
    student = student_instance.createStudent("EveStudentTest", "Evil", "eve@example.com", "Devils GmbH", 11111, True)
    student_instance.deleteStudent(student.studentId)

    deleted_student = student_instance.readStudentById(student.studentId)

    assert deleted_student is None
