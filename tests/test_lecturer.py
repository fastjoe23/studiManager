import pytest
from studi_manager_model import Lecturer

@pytest.fixture
def lecturer_instance():
    lecturer = Lecturer()
    return lecturer

def test_create_lecturer(lecturer_instance):
    lecturer = lecturer_instance.create_lecturer("Doe", "John", "john.doe@example.com", "ABC Corp")
    assert lecturer is not None
    assert lecturer.lecturer_id is not None
    assert lecturer.person_id is not None
    assert lecturer.first_name == "John"
    assert lecturer.last_name == "Doe"
    assert lecturer.email == "john.doe@example.com"
    assert lecturer.company == "ABC Corp"

def test_read_lecturer_by_id(lecturer_instance):
    lecturer = lecturer_instance.create_lecturer("Doe", "Jane", "jane.doe@example.com", "XYZ Inc")
    retrieved_lecturer = lecturer_instance.read_lecturer_by_id(lecturer.lecturer_id)
    assert retrieved_lecturer is not None
    assert retrieved_lecturer.lecturer_id == lecturer.lecturer_id
    assert retrieved_lecturer.first_name == "Jane"
    assert retrieved_lecturer.last_name == "Doe"
    assert retrieved_lecturer.email == "jane.doe@example.com"
    assert retrieved_lecturer.company == "XYZ Inc"

def test_read_all_lecturers(lecturer_instance):
    lecturer_instance.create_lecturer("Johnson", "Alice", "alice@example.com", "ABC University")
    lecturer_instance.create_lecturer("Smith", "Bob", "bob@example.com", "XYZ Institute")

    lecturers = lecturer_instance.read_all_lecturers()
    assert isinstance(lecturers, list)

    # You can perform additional assertions based on your data

def test_update_lecturer(lecturer_instance):
    lecturer = lecturer_instance.create_lecturer("Williams", "Mark", "mark@example.com", "Tech Solutions")
    new_person_id = lecturer.person_id
    new_first_name = "Mark Updated"
    new_last_name = "Williams Updated"
    new_email = "mark.updated@example.com"
    new_company = "New Tech Solutions"

    lecturer_instance.update_lecturer(lecturer.lecturer_id, new_person_id, new_last_name, new_first_name, new_email, new_company)

    updated_lecturer = lecturer_instance.read_lecturer_by_id(lecturer.lecturer_id)
    assert updated_lecturer is not None
    assert updated_lecturer.first_name == new_first_name
    assert updated_lecturer.last_name == new_last_name
    assert updated_lecturer.email == new_email
    assert updated_lecturer.company == new_company

def test_delete_lecturer(lecturer_instance):
    lecturer = lecturer_instance.create_lecturer("Emily", "Clark", "emily@example.com", "Education Hub")
    lecturer_id = lecturer.lecturer_id

    lecturer_instance.delete_lecturer(lecturer_id)
    deleted_lecturer = lecturer_instance.read_lecturer_by_id(lecturer_id)
    assert deleted_lecturer is None
