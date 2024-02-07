import pytest
from studentModel import Assignments 

@pytest.fixture
def assignments_instance():
    assignments = Assignments()
    created_assignment_ids = []  # Liste für die erstellten assignmentIds

    yield (assignments, created_assignment_ids)  # Gibt das Tuple (assignments, created_assignment_ids) zurück

    # Cleanup: Lösche die erzeugten Assignments
    # Da hier nur Dummy Assignments ohne zugehoerige Studenten und Gutachter erstellt werden löschen wir diese am Ende lieber wieder
    for assignment_id in created_assignment_ids:
        assignments.deleteAssignment(assignment_id)

def test_create_assignment(assignments_instance):
    assignments, created_assignment_ids = assignments_instance
    assignment = assignments.createAssignment( 2, 3, "Homework", "Python Programming", "1,8", "1.12.2999", "9:00 - 10:00")
    assert assignment.assignmentId is not None
    created_assignment_ids.append(assignment.assignmentId)
    assert assignment.studentId == 2
    assert assignment.lecturerId == 3
    assert assignment.type == "Homework"
    assert assignment.topic == "Python Programming"
    assert assignment.grade == "1,8"
    assert assignment.date == "1.12.2999"
    assert assignment.time == "9:00 - 10:00"

def test_read_assignment_by_id(assignments_instance):
    assignments, created_assignment_ids = assignments_instance
    assignment = assignments.createAssignment( 2, 3, "Homework", "Python Programming", "1,8", "1.12.2999", "9:00 - 10:00")
    created_assignment_ids.append(assignment.assignmentId)
    retrieved_assignment = assignments.readAssignmentById(assignment.assignmentId)
    assert retrieved_assignment is not None
    assert retrieved_assignment.assignmentId == assignment.assignmentId

def test_read_all_assignments(assignments_instance):
    assignments, created_assignment_ids = assignments_instance
    assignment = assignments.createAssignment( 2, 3, "Homework", "Python Programming", "1,8", "1.12.2999", "9:00 - 10:00")
    created_assignment_ids.append(assignment.assignmentId)
    assignments_list = assignments.readAllAssignments()
    assert len(assignments_list) >= 1

def test_update_assignment(assignments_instance):
    assignments, created_assignment_ids = assignments_instance
    assignment = assignments.createAssignment( 2, 3, "Homework", "Python Programming", "1,8", "1.12.2999", "9:00 - 10:00")
    created_assignment_ids.append(assignment.assignmentId)
    assignment_id = assignment.assignmentId
    assignments.updateAssignment(assignment_id, 4, 5,"NewType", "NewTopic", "5,8", "31.12.2999", "10:00 - 11:00")
    updated_assignment = assignments.readAssignmentById(assignment_id)
    assert updated_assignment.studentId == 4
    assert updated_assignment.lecturerId == 5
    assert updated_assignment.type == "NewType"
    assert updated_assignment.topic == "NewTopic"
    assert updated_assignment.grade == "5,8"
    assert updated_assignment.date == "31.12.2999"
    assert updated_assignment.time == "10:00 - 11:00"


def test_delete_assignment(assignments_instance):
    assignments, created_assignment_ids = assignments_instance
    assignment = assignments.createAssignment( 2, 3, "Homework", "Python Programming", "1,8", "1.12.2999", "9:00 - 10:00")
    assignment_id = assignment.assignmentId
    assignments.deleteAssignment(assignment_id)
    deleted_assignment = assignments.readAssignmentById(assignment_id)
    assert deleted_assignment is None

# Weitere Testfälle können entsprechend hinzugefügt werden
