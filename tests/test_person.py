# Beispiel: tests/test_person.py

import pytest
from studi_manager_model import Person  # Achte darauf, den korrekten Pfad zu verwenden

@pytest.fixture
def person_instance():
    return Person()

def test_create_person(person_instance):
    # Teste die Methode create_person
    first_name = "John"
    last_name = "Doe"
    email = "john.doe@example.com"

    person_id = person_instance.create_person(first_name, last_name, email)

    assert person_id is not None

def test_read_all_persons(person_instance):
    # Teste die Methode read_all_persons
    persons = person_instance.read_all_persons()

    assert isinstance(persons, list)

def test_read_person_by_id(person_instance):
    # Teste die Methode read_person_by_id
    person = person_instance.create_person("Wonderland", "Alice", "alice@example.com")

    retrieved_person = person_instance.read_person_by_id(person.person_id)

    assert retrieved_person is not None
    assert isinstance(retrieved_person, Person)
    assert retrieved_person.person_id == person.person_id
    assert retrieved_person.first_name == "Alice"
    assert retrieved_person.last_name == "Wonderland"
    assert retrieved_person.email == "alice@example.com"

def test_update_person(person_instance):
    # Teste die Methode update_person
    person = person_instance.create_person("Wonderland", "Alice", "alice@example.com")

    person_instance.update_person(person.person_id, "New_lastname", "New_name", "newemail@example.com")

    updated_person = person_instance.read_person_by_id(person.person_id)

    assert updated_person.first_name == "New_name"
    assert updated_person.last_name == "New_lastname"
    assert updated_person.email == "newemail@example.com"

def test_delete_person(person_instance):
    # Teste die Methode delete_person
    person = person_instance.create_person("Bob", "Builder", "bob@example.com")

    person_instance.delete_person(person.person_id)

    person = person_instance.read_person_by_id(person.person_id)

    assert person == None

def test_read_person_by_name(person_instance):
    # Teste die Methode read_person_by_name
    first_name = "Fritz"
    last_name = "Mueller"
    email = "fritz@mueller.com"

    person_instance.create_person(last_name, first_name, email)

    retrieved_person = person_instance.read_person_by_name(last_name, first_name)

    assert retrieved_person is not None
    assert isinstance(retrieved_person, Person)
    assert retrieved_person.first_name == first_name
    assert retrieved_person.last_name == last_name
    assert retrieved_person.email == email
