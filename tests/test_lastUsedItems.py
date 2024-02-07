import pytest
from studentModel import LastUsedItems


@pytest.fixture
def lastUsedItems_instance():
    lastUsedItems = LastUsedItems()
    

    yield (lastUsedItems)  # Gibt das Tuple (lastUsedItems, created_assignment_ids) zurück

    # Cleanup: Lösche die erzeugten lastUsedItems
    # Da hier nur Dummy lastUsedItems ohne zugehoerige Studenten und Gutachter erstellt werden löschen wir diese am Ende lieber wieder
    lastUsedItems.deleteAllLastUsedElements()

def test_create_and_read_last_used_item(lastUsedItems_instance):
    # Testet das Erstellen und Lesen eines letzten verwendeten Elements
    
    created_item = lastUsedItems_instance.createLastUsedItem("example_type", ['1', '2', '3'])

    # Überprüfe, ob das erstellte Element korrekt in die Datenbank geschrieben wurde
    fetched_item = lastUsedItems_instance.readLastUsedItemByType("example_type")
    assert fetched_item.type == created_item.type
    assert fetched_item.elements == created_item.elements

def test_update_last_used_item(lastUsedItems_instance):
    # Testet das Aktualisieren eines letzten verwendeten Elements
    lastUsedItems_instance.createLastUsedItem("example_type", ['1', '2', '3'])

    # Aktualisiere das Element und überprüfe die Aktualisierung
    lastUsedItems_instance.updateLastUsedItem("example_type", ['4', '5', '6'])
    updated_item = lastUsedItems_instance.readLastUsedItemByType("example_type")
    assert updated_item.elements == ['4', '5', '6']

def test_read_nonexistent_last_used_item(lastUsedItems_instance):
    # Testet das Lesen eines nicht vorhandenen Elements
    
    # Überprüfe, dass das Lesen eines nicht vorhandenen Elements None zurückgibt
    fetched_item = lastUsedItems_instance.readLastUsedItemByType("nonexistent_type")
    assert fetched_item is None

