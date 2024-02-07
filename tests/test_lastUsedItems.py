import pytest
from studi_manager_model import LastUsedItems


@pytest.fixture
def last_used_items_instance():
    last_used_items = LastUsedItems()
    

    yield (last_used_items)  # Gibt das Tuple (last_used_items, created_assignment_ids) zurück

    # Cleanup: Lösche die erzeugten last_used_items
    # Da hier nur Dummy last_used_items ohne zugehoerige Studenten und Gutachter erstellt werden löschen wir diese am Ende lieber wieder
    last_used_items.delete_all_last_used_elements()

def test_create_and_read_last_used_item(last_used_items_instance):
    # Testet das Erstellen und Lesen eines letzten verwendeten Elements
    
    created_item = last_used_items_instance.create_last_used_item("example_type", ['1', '2', '3'])

    # Überprüfe, ob das erstellte Element korrekt in die Datenbank geschrieben wurde
    fetched_item = last_used_items_instance.read_last_used_item_by_type("example_type")
    assert fetched_item.type == created_item.type
    assert fetched_item.elements == created_item.elements

def test_update_last_used_item(last_used_items_instance):
    # Testet das Aktualisieren eines letzten verwendeten Elements
    last_used_items_instance.create_last_used_item("example_type", ['1', '2', '3'])

    # Aktualisiere das Element und überprüfe die Aktualisierung
    last_used_items_instance.update_last_used_item("example_type", ['4', '5', '6'])
    updated_item = last_used_items_instance.read_last_used_item_by_type("example_type")
    assert updated_item.elements == ['4', '5', '6']

def test_read_nonexistent_last_used_item(last_used_items_instance):
    # Testet das Lesen eines nicht vorhandenen Elements
    
    # Überprüfe, dass das Lesen eines nicht vorhandenen Elements None zurückgibt
    fetched_item = last_used_items_instance.read_last_used_item_by_type("nonexistent_type")
    assert fetched_item is None

