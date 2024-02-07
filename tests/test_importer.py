import pytest
from studi_manager_model import Model
from studi_manager_controller import StudentManagerController

@pytest.fixture
def model():
    return Model()

@pytest.fixture
def student_controller():
    return StudentManagerController(model)

def test_save_course_list_to_file(student_controller, tmpdir):
    parsed_data = "Nachname,Vorname,Firma,Mat-Nr,Email\n_doe,John,Doe Gmb_h,12345,john.doe@lehre.dhbw-stuttgart.de"
    save_path = str(tmpdir)
    
    student_controller.save_list_to_file(parsed_data, save_path, "Kursliste", "WWI2022")
    
    file_path = tmpdir / "WWI2022Kursliste.csv"
    assert file_path.read_text('utf-8') == parsed_data

def test_parse_function(student_controller):
    text_content = "wi12345 (Doe, John)\nwi23456 (Smith, Alice)"
    expected_result = "Nachname,Vorname,Firma,Mat-Nr,Email\nDoe,John,,,wi12345@lehre.dhbw-stuttgart.de\nSmith,Alice,,,wi23456@lehre.dhbw-stuttgart.de\n"

    result = student_controller.parse_function(text_content)

    assert result == expected_result

def test_import_students_from_csv_into_course(student_controller, tmpdir):
    csv_data = "Nachname,Vorname,Firma,Mat-Nr,Email\nDoe,John,Stadtwerke,wi12345,john.doe@lehre.dhbw-stuttgart.de\n_smith,Alice,Smithians,wi23456,alice.smith@lehre.dhbw-stuttgart.de"
    csv_file_path = tmpdir / "test.csv"
    csv_file_path.write_text(csv_data, 'utf-8')
    model = Model()
    student_controller = StudentManagerController(model)
    course =student_controller.add_course("Import Test Kurs","2024-03-10")

    student_controller.import_students_from_csv_into_course(str(csv_file_path), course.course_id)

    studentslist = student_controller.read_all_students_by_course_id(course.course_id)

    assert len(studentslist) == 2
