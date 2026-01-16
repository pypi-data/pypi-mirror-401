import pytest
from packaging_workshop_pmat import greet

def test_greet_happy_path():
    assert greet("World") == "Hello, World!"

def test_greet_rejects_empty():
    with pytest.raises(ValueError):
        greet("   ")
