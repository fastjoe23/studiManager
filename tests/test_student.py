import pytest
from studi_manager_model import Student

@pytest.fixture
def student_instance():
    return Student()

def test_create_student(student_instance):
    student = student_instance.create_student("John_student_test", "Doe", "john.doe@example.com", "Google", 12345, True)

    assert student.student_id is not None
    assert student.mat_number == 12345
    assert student.enrolled is True

def test_read_all_students(student_instance):
    students = student_instance.read_all_students()

    assert isinstance(students, list)

def test_read_student_by_id(student_instance):
    student = student_instance.create_student("Alice_student_test", "Wonderland", "alice@example.com", "Daimler", 54321, False)
    retrieved_student = student_instance.read_student_by_id(student.student_id)

    assert retrieved_student is not None
    assert retrieved_student.student_id == student.student_id
    assert retrieved_student.last_name == "Alice_student_test"
    assert retrieved_student.first_name == "Wonderland"
    assert retrieved_student.email == "alice@example.com"
    assert retrieved_student.company == "Daimler"
    assert retrieved_student.mat_number == 54321
    assert retrieved_student.enrolled is False

def test_update_student(student_instance):
    student = student_instance.create_student("Bob_student_test", "Builder", "bob@example.com", "Bompany", 67890, True)
    student_instance.update_student(student.student_id, student.person_id, "New_lastname", "New_name_Student_test", "newemail@example.com", "New_company", 98765, False)

    updated_student = student_instance.read_student_by_id(student.student_id)

    assert updated_student.first_name == "New_name_Student_test"
    assert updated_student.last_name == "New_lastname"
    assert updated_student.email == "newemail@example.com"
    assert updated_student.company == "New_company"
    assert updated_student.mat_number == 98765
    assert updated_student.enrolled is False

def test_delete_student(student_instance):
    student = student_instance.create_student("Eve_student_test", "Evil", "eve@example.com", "Devils Gmb_h", 11111, True)
    student_instance.delete_student(student.student_id)

    deleted_student = student_instance.read_student_by_id(student.student_id)

    assert deleted_student is None
