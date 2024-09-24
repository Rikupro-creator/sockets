import pytest
import file_reading
from unittest.mock import MagicMock


def test_normal_open_file_nonexistent():
    """Test FileNotFoundError when file does not exist."""
    # Ensure that FileNotFoundError is raised
    # When attempting to open a non-existent file.
    with pytest.raises(FileNotFoundError) as err:
        file_reading.normal_open("tests.txt")
    assert str(err.value) == "The file is not found in the directory."


def test_normal_open_file_integer():
    """Test AssertionError for non-string filename."""
    # Ensure that passing an integer as a filename
    # Raises an AssertionError.
    with pytest.raises(AssertionError) as err:
        file_reading.normal_open(9054)
    assert str(err.value) == "Filename must be a string"


def test_normal_open_file_extension():
    """Test TypeError for non-txt file extension."""
    # Ensure that trying to open a non-txt file raises a TypeError.
    with pytest.raises(TypeError) as err:
        file_reading.normal_open("test_file.pdf")
    assert str(err.value) == "Filename must end with .txt extension"


def test_mmap_open_file_nonexistent():
    """Test FileNotFoundError when file does not exist in mmap_open."""
    # Ensure that FileNotFoundError is raised
    # When attempting to open a non-existent file using mmap_open.
    with pytest.raises(FileNotFoundError) as err:
        file_reading.mmap_open("tests.txt")
    assert str(err.value) == "The file is not found in the directory."


def test_mmap_open_file_integer():
    """Test AssertionError for non-string filename in mmap_open."""
    # Ensure that passing an integer as a filename to mmap_open
    # Raises an AssertionError.
    with pytest.raises(AssertionError) as err:
        file_reading.mmap_open(9054)
    assert str(err.value) == "Filename must be a string"


def test_mmap_open_file_extension():
    """Test TypeError for non-txt file extension in mmap_open."""
    # Ensure that trying to open a non-txt file
    # Using mmap_open raises a TypeError.
    with pytest.raises(TypeError) as err:
        file_reading.mmap_open("test_file.pdf")
    assert str(err.value) == "Filename must end with .txt extension"


def test_time_evaluator_file_nonexistent():
    """Test FileNotFoundError in time_evaluator when file doesn't exist."""
    # Ensure that FileNotFoundError is raised when
    # Time_evaluator is called with a non-existent file.
    with pytest.raises(FileNotFoundError) as err:
        file_reading.time_evaluator(file_reading.normal_open, "tests.txt")
    assert str(err.value) == "The file is not found in the directory."


def test_time_evaluator_file_integer():
    """Test AssertionError for non-string filename in time_evaluator."""
    # Ensure that passing an integer as a filename to time_evaluator
    # Raises an AssertionError.
    with pytest.raises(AssertionError) as err:
        file_reading.time_evaluator(file_reading.mmap_open, 9054)
    assert str(err.value) == "Filename must be a string"


def test_time_evaluator_file_extension():
    """Test TypeError for non-txt file extension in time_evaluator."""
    # Ensure that trying to use a non-txt file
    # With time_evaluator raises a TypeError.
    with pytest.raises(TypeError) as err:
        file_reading.time_evaluator(file_reading.mmap_open, "test_file.pdf")
    assert str(err.value) == "Filename must end with .txt extension"


def test_time_evaluator_callable_ftn():
    """Test AssertionError for non-callable function in time_evaluator."""
    # Ensure that passing a non-function value as the function
    # Argument raises an AssertionError.
    with pytest.raises(AssertionError) as err:
        file_reading.time_evaluator("somftns", "10k.txt")
    assert str(err.value) == "Ftn must be a function!"


def test_time_evaluator_callable_ftn_integer_test():
    """Test AssertionError for non-function integer in time_evaluator."""
    # Ensure that passing an integer instead of a function
    # Raises an AssertionError.
    with pytest.raises(AssertionError) as err:
        file_reading.time_evaluator(20, "10k.txt")
    assert str(err.value) == "Ftn must be a function!"
