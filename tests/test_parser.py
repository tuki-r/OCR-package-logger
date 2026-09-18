import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse_courier_text

# Test 1: standard courier format
def test_standard_format():
    """
    Test parsing a standard courier text format.
    """
    text = """
    Ship To:
    John Doe
    Richwood street
    Unit 12
    Milnerton
    0123456789
    """
    result = parse_courier_text(text)
    assert result['name'] == 'John Doe', f"Expected 'John Doe', but got {result['name']}"
    assert result['unit'] == 12
    assert result['phone'] == '0123456789', f"Expected '0123456789', but got {result['phone']}"
    print("Test 1 PASSED — standard format")


# Test 2: missing phone number
def test_missing_phone():
    """
    Test parsing a courier text format with missing phone number. Phone number should return None
    """
    text = """
    Ship To:
    Mia Louw
    28 Ocean View Drive
    Unit 457
    Cape Town
    """
    result = parse_courier_text(text)
    assert result['name'] == 'Mia Louw', f"Expected 'Mia Louw', but got {result['name']}"
    assert result['unit'] == 457, f"Expected 457, but got {result['unit']}"
    assert result['phone'] is None, f"Expected None for phone, but got {result['phone']}"
    print("Test 2 PASSED — missing phone")


# Test 3: empty string (edge case)
def test_empty_string():
    """
    Test parsing an empty string. All fields should return None.
    """
    result = parse_courier_text("")

    assert result['name'] is None, f"Expected None for name, but got {result['name']}"
    assert result['unit'] is None, f"Expected None for unit, but got {result['unit']}"
    assert result['phone'] is None, f"Expected None for phone, but got {result['phone']}"
    print("Test 3 PASSED — empty string")

if __name__ == "__main__":
    print("Running parser unit tests...\n")
    test_standard_format()
    test_missing_phone()
    test_empty_string()
    print("\nAll tests completed successfully.")
