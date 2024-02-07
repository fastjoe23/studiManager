import pytest
from studi_manager_model import Course

@pytest.fixture
def course_instance():
    return Course()

def test_create_course(course_instance):
    # Testet die create_course-Methode
    course = course_instance.create_course("Python Programming", "2024-02-01")
    assert course.course_id is not None
    assert course.course_name == "Python Programming"
    assert course.start_date == "2024-02-01"

def test_read_course_by_id(course_instance):
    # Testet die read_course_by_id-Methode
    new_course = course_instance.create_course("Python Programming", "2025-02-01")
    retrieved_course = course_instance.read_course_by_id(new_course.course_id)
    assert retrieved_course is not None
    assert new_course.course_id == retrieved_course.course_id

def test_read_all_courses(course_instance):
    # Testet die read_all_courses-Methode
    _ = course_instance.create_course("Python Programming", "2024-02-01")
    _ = course_instance.create_course("Java Programming", "2022-02-01")

    courses = course_instance.read_all_courses()
    assert len(courses) > 0

def test_update_course(course_instance):
    # Testet die update_course-Methode
    new_course = course_instance.create_course("Test Programming", "2025-02-01")
    new_course_name = "Updated Python Programming"
    new_start_date = "2024-03-01"
    course_instance.update_course(new_course.course_id, new_course_name, new_start_date)

    # Überprüfe, ob der Kurs aktualisiert wurde
    updated_course = course_instance.read_course_by_id(new_course.course_id)
    assert updated_course is not None
    assert updated_course.course_name == new_course_name
    assert updated_course.start_date == new_start_date

def test_delete_course(course_instance):
    # Testet die delete_course-Methode
    new_course = course_instance.create_course("Delete Test", "2025-02-01")
    course_instance.delete_course(new_course.course_id)

    # Überprüfe, ob der Kurs gelöscht wurde
    deleted_course = course_instance.read_course_by_id(new_course.course_id)
    assert deleted_course is None
