import pytest
from src.data_processing.validation import (
validate_isbn
)

def test_validate_isbn():
    assert validate_isbn('978-0-123456-78-9') == True
    assert validate_isbn('invalid') == False
    assert validate_isbn('123') == False  # Too short
    assert validate_isbn('') == False
    assert validate_isbn(None) == False
