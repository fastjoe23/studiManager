import pytest
from studentModel import Lecturer

@pytest.fixture
def lecturer_instance():
    lecturer = Lecturer()
    return lecturer

def test_create_lecturer(lecturer_instance):
    lecturer = lecturer_instance.createLecturer("Doe", "John", "john.doe@example.com", "ABC Corp")
    assert lecturer is not None
    assert lecturer.lecturerId is not None
    assert lecturer.personId is not None
    assert lecturer.firstName == "John"
    assert lecturer.lastName == "Doe"
    assert lecturer.email == "john.doe@example.com"
    assert lecturer.company == "ABC Corp"

def test_read_lecturer_by_id(lecturer_instance):
    lecturer = lecturer_instance.createLecturer("Doe", "Jane", "jane.doe@example.com", "XYZ Inc")
    retrieved_lecturer = lecturer_instance.readLecturerById(lecturer.lecturerId)
    assert retrieved_lecturer is not None
    assert retrieved_lecturer.lecturerId == lecturer.lecturerId
    assert retrieved_lecturer.firstName == "Jane"
    assert retrieved_lecturer.lastName == "Doe"
    assert retrieved_lecturer.email == "jane.doe@example.com"
    assert retrieved_lecturer.company == "XYZ Inc"

def test_read_all_lecturers(lecturer_instance):
    lecturer_instance.createLecturer("Johnson", "Alice", "alice@example.com", "ABC University")
    lecturer_instance.createLecturer("Smith", "Bob", "bob@example.com", "XYZ Institute")

    lecturers = lecturer_instance.readAllLecturers()
    assert isinstance(lecturers, list)

    # You can perform additional assertions based on your data

def test_update_lecturer(lecturer_instance):
    lecturer = lecturer_instance.createLecturer("Williams", "Mark", "mark@example.com", "Tech Solutions")
    new_person_id = lecturer.personId
    new_first_name = "Mark Updated"
    new_last_name = "Williams Updated"
    new_email = "mark.updated@example.com"
    new_company = "New Tech Solutions"

    lecturer_instance.updateLecturer(lecturer.lecturerId, new_person_id, new_last_name, new_first_name, new_email, new_company)

    updated_lecturer = lecturer_instance.readLecturerById(lecturer.lecturerId)
    assert updated_lecturer is not None
    assert updated_lecturer.firstName == new_first_name
    assert updated_lecturer.lastName == new_last_name
    assert updated_lecturer.email == new_email
    assert updated_lecturer.company == new_company

def test_delete_lecturer(lecturer_instance):
    lecturer = lecturer_instance.createLecturer("Emily", "Clark", "emily@example.com", "Education Hub")
    lecturer_id = lecturer.lecturerId

    lecturer_instance.deleteLecturer(lecturer_id)
    deleted_lecturer = lecturer_instance.readLecturerById(lecturer_id)
    assert deleted_lecturer is None
