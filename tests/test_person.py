# Beispiel: tests/test_person.py

import pytest
from studentModel import Person  # Achte darauf, den korrekten Pfad zu verwenden

@pytest.fixture
def person_instance():
    return Person()

def test_create_person(person_instance):
    # Teste die Methode createPerson
    first_name = "John"
    last_name = "Doe"
    email = "john.doe@example.com"

    person_id = person_instance.createPerson(first_name, last_name, email)

    assert person_id is not None

def test_read_all_persons(person_instance):
    # Teste die Methode readAllPersons
    persons = person_instance.readAllPersons()

    assert isinstance(persons, list)

def test_read_person_by_id(person_instance):
    # Teste die Methode readPersonById
    person = person_instance.createPerson("Wonderland", "Alice", "alice@example.com")

    retrieved_person = person_instance.readPersonById(person.personId)

    assert retrieved_person is not None
    assert isinstance(retrieved_person, Person)
    assert retrieved_person.personId == person.personId
    assert retrieved_person.firstName == "Alice"
    assert retrieved_person.lastName == "Wonderland"
    assert retrieved_person.email == "alice@example.com"

def test_update_person(person_instance):
    # Teste die Methode updatePerson
    person = person_instance.createPerson("Wonderland", "Alice", "alice@example.com")

    person_instance.updatePerson(person.personId, "NewLastname", "NewName", "newemail@example.com")

    updated_person = person_instance.readPersonById(person.personId)

    assert updated_person.firstName == "NewName"
    assert updated_person.lastName == "NewLastname"
    assert updated_person.email == "newemail@example.com"

def test_delete_person(person_instance):
    # Teste die Methode deletePerson
    person = person_instance.createPerson("Bob", "Builder", "bob@example.com")

    person_instance.deletePerson(person.personId)

    person = person_instance.readPersonById(person.personId)

    assert person == None

def test_read_person_by_name(person_instance):
    # Teste die Methode readPersonByName
    first_name = "Fritz"
    last_name = "Mueller"
    email = "fritz@mueller.com"

    person_instance.createPerson(last_name, first_name, email)

    retrieved_person = person_instance.readPersonByName(last_name, first_name)

    assert retrieved_person is not None
    assert isinstance(retrieved_person, Person)
    assert retrieved_person.firstName == first_name
    assert retrieved_person.lastName == last_name
    assert retrieved_person.email == email
