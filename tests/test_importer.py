import pytest
from studentModel import Model
from studentController import StudentController

@pytest.fixture
def model():
    return Model()

@pytest.fixture
def student_controller():
    return StudentController(model)

def test_save_course_list_to_file(student_controller, tmpdir):
    parsed_data = "Nachname,Vorname,Firma,Mat-Nr,Email\nDoe,John,Doe GmbH,12345,john.doe@lehre.dhbw-stuttgart.de"
    save_path = str(tmpdir)
    
    student_controller.saveListToFile(parsed_data, save_path, "Kursliste", "WWI2022")
    
    file_path = tmpdir / "WWI2022Kursliste.csv"
    assert file_path.read_text('utf-8') == parsed_data

def test_parse_function(student_controller):
    text_content = "wi12345 (Doe, John)\nwi23456 (Smith, Alice)"
    expected_result = "Nachname,Vorname,Firma,Mat-Nr,Email\nDoe,John,,,wi12345@lehre.dhbw-stuttgart.de\nSmith,Alice,,,wi23456@lehre.dhbw-stuttgart.de\n"

    result = student_controller.parseFunction(text_content)

    assert result == expected_result

def test_import_students_from_csv_into_course(student_controller, tmpdir):
    csv_data = "Nachname,Vorname,Firma,Mat-Nr,Email\nDoe,John,Stadtwerke,wi12345,john.doe@lehre.dhbw-stuttgart.de\nSmith,Alice,Smithians,wi23456,alice.smith@lehre.dhbw-stuttgart.de"
    csv_file_path = tmpdir / "test.csv"
    csv_file_path.write_text(csv_data, 'utf-8')
    model = Model()
    student_controller = StudentController(model)
    course =student_controller.addCourse("Import Test Kurs","2024-03-10")

    student_controller.importStudentsFromCsvIntoCourse(str(csv_file_path), course.courseId)

    studentslist = student_controller.readAllStudentsByCourseId(course.courseId)

    assert len(studentslist) == 2
