"""
Data validation functions.
"""

# Example function to implement:
def validate_isbn(isbn):
    """Validate ISBN-13 format.

    Args:
        isbn (str): ISBN string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not isbn:
        return False

    # Remove hyphens
    isbn = isbn.replace('-', '')

    # Check length
    if len(isbn) != 13:
        return False

    # Check if all digits
    if not isbn.isdigit():
        return False

    return True