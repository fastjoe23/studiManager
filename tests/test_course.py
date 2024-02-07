import pytest
from studentModel import Course

@pytest.fixture
def course_instance():
    return Course()

def test_create_course(course_instance):
    # Testet die createCourse-Methode
    course = course_instance.createCourse("Python Programming", "2024-02-01")
    assert course.courseId is not None
    assert course.courseName == "Python Programming"
    assert course.startDate == "2024-02-01"

def test_read_course_by_id(course_instance):
    # Testet die readCourseById-Methode
    newCourse = course_instance.createCourse("Python Programming", "2025-02-01")
    retrievedCourse = course_instance.readCourseById(newCourse.courseId)
    assert retrievedCourse is not None
    assert newCourse.courseId == retrievedCourse.courseId

def test_read_all_courses(course_instance):
    # Testet die readAllCourses-Methode
    _ = course_instance.createCourse("Python Programming", "2024-02-01")
    _ = course_instance.createCourse("Java Programming", "2022-02-01")

    courses = course_instance.readAllCourses()
    assert len(courses) > 0

def test_update_course(course_instance):
    # Testet die updateCourse-Methode
    newCourse = course_instance.createCourse("Test Programming", "2025-02-01")
    new_course_name = "Updated Python Programming"
    new_start_date = "2024-03-01"
    course_instance.updateCourse(newCourse.courseId, new_course_name, new_start_date)

    # Überprüfe, ob der Kurs aktualisiert wurde
    updated_course = course_instance.readCourseById(newCourse.courseId)
    assert updated_course is not None
    assert updated_course.courseName == new_course_name
    assert updated_course.startDate == new_start_date

def test_delete_course(course_instance):
    # Testet die deleteCourse-Methode
    newCourse = course_instance.createCourse("Delete Test", "2025-02-01")
    course_instance.deleteCourse(newCourse.courseId)

    # Überprüfe, ob der Kurs gelöscht wurde
    deleted_course = course_instance.readCourseById(newCourse.courseId)
    assert deleted_course is None
