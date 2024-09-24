import pytest
import string_search
import os
import mmap


# Testing search_line_in_file
def test_search_line_in_file_search_list():
    """Test TypeError when search line is not a
    string or list_file is not a list.
    """
    with pytest.raises(TypeError) as err:
        string_search.search_line_in_file('h', 10)
    assert str(err.value) == 'Ensure search line is a string\
                         or list_file is a list'


def test_search_line_in_file_arguments():
    """Test ValueError when search term is not a string."""
    with pytest.raises(ValueError) as err:
        string_search.search_line_in_file(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


def test_search_line_in_file_list_int():
    """Test AttributeError when list contains an integer."""
    with pytest.raises(AttributeError) as err:
        string_search.search_line_in_file('h', ['h', 4, 'k'])
    assert str(err.value) == "There is an integer in the list"


# Binary search test
def test_binary_search_list():
    """Test TypeError when list_file is not a list."""
    with pytest.raises(TypeError) as err:
        string_search.binary_search('h', 10)
    assert str(err.value) == 'Ensure search line is a string\
                         or list_file is a list'


def test_binary_search_arguments():
    """Test ValueError when search term is not a string."""
    with pytest.raises(ValueError) as err:
        string_search.binary_search(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


def test_binary_search_line_int():
    """Test AttributeError when list contains an integer."""
    with pytest.raises(AttributeError) as err:
        string_search.binary_search('k', ['o', 9, 'k'])
    assert str(err.value) == 'There is an integer in the list'


# Fibonacci search
def test_fibonacci_search_list():
    """Test TypeError when second argument is not a list of strings."""
    with pytest.raises(TypeError) as err:
        string_search.fibonacci_search('h', 10)
    assert str(err.value) == 'Second argument should be a list of strings'


def test_fibonacci_search_line():
    """Test ValueError when search term is not a string."""
    with pytest.raises(ValueError) as err:
        string_search.fibonacci_search(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


def test_fibonacci_search_line_type():
    """Test TypeError when list contains an integer."""
    with pytest.raises(TypeError) as err:
        string_search.fibonacci_search('k', ['o', 9, 'k'])
    assert str(err.value) == 'Second argument should be a list of strings'


# Ternary search
def test_ternary_search_list():
    """Test TypeError when second argument is not a list of strings."""
    with pytest.raises(TypeError) as err:
        string_search.ternary_search('h', 10)
    assert str(err.value) == 'Second argument should be a list of strings'


def test_ternary_search_line_type():
    """Test TypeError when list contains an integer."""
    with pytest.raises(TypeError) as err:
        string_search.ternary_search('k', ['o', 9, 'k'])
    assert str(err.value) == 'Second argument should be a list of strings'


# Hashing search
def test_hashing_search_list():
    """Test TypeError when list_file is not a list."""
    with pytest.raises(TypeError) as err:
        string_search.hashing_search('h', 10)
    assert str(err.value) == 'Ensure search line is a string\
                        or list_file is a list'


def test_hashing_search_line():
    """Test ValueError when search term is not a string."""
    with pytest.raises(ValueError) as err:
        string_search.hashing_search(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


def test_hashing_search_line_type():
    """Test AttributeError when list contains an integer."""
    with pytest.raises(AttributeError) as err:
        string_search.hashing_search('k', ['o', 9, 'k'])
    assert str(err.value) == 'There is an integer in the list'


# Bisect search
def test_bisect_search_list():
    """Test bisect_search raises TypeError for non-list second argument."""
    with pytest.raises(TypeError) as err:
        string_search.bisect_search('h', 10)
    assert str(err.value) == 'Second argument should be a list of strings'


def test_bisect_search_line():
    """Test bisect_search raises ValueError for non-string search term."""
    with pytest.raises(ValueError) as err:
        string_search.bisect_search(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


def test_bisect_search_line_type():
    """Test bisect_search raises TypeError
     for non-string items in list.
     """
    with pytest.raises(TypeError) as err:
        string_search.bisect_search('k', ['o', 9, 'k'])
    assert str(err.value) == 'Second argument should be a list of strings'


# Search with "in"
def test_search_chunk_with_in_list():
    """Test search_chunk_with_in raises TypeError for
    non-string search term or non-list second argument.
    """
    with pytest.raises(TypeError) as err:
        string_search.search_chunk_with_in('h', 10)
    assert str(err.value) == 'Ensure search line is a string\
                        or list_file is a list of strings'


def test_search_chunk_with_in_line():
    """Test search_chunk_with_in raises ValueError
    for non-string search term.
    """
    with pytest.raises(ValueError) as err:
        string_search.search_chunk_with_in(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


# Search with "find"
def test_search_chunk_with_find():
    """Test search_chunk_with_find raises ValueError
    for incorrect chunk or search term types.
    """
    with pytest.raises(ValueError) as err:
        string_search.search_chunk_with_find("Hello, world!", b"world")
    assert str(err.value) == 'Chunk should be mmap object'

    with pytest.raises(ValueError) as err:
        string_search.search_chunk_with_find(b"Hello, world!", "world")
    assert str(err.value) == 'Search term should be a bytes'

    with pytest.raises(ValueError) as err:
        string_search.search_chunk_with_find(b"Hello, world!", 10)
    assert str(err.value) == 'Search term should be a bytes'


def test_boyer_list():
    """Test boyer_moore_search_list raises
    TypeError for non-list second argument.
    """
    with pytest.raises(TypeError) as err:
        string_search.boyer_moore_search_list('h', 10)
    assert str(err.value) == 'Second argument should be a list'


def test_boyer_line():
    """Test boyer_moore_search_list raises
    ValueError for non-string search term.
    """
    with pytest.raises(ValueError) as err:
        string_search.boyer_moore_search_list(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'


def test_rubin_list():
    """Test rabin_karp_search_list raises TypeError
    for non-list second argument.
    """
    with pytest.raises(TypeError) as err:
        string_search.rabin_karp_search_list('h', 10)
    assert str(err.value) == 'Second argument should be a list'


def test_rubin_type():
    """Test rabin_karp_search_list raises
    TypeError for non-string items in list.
    """
    with pytest.raises(TypeError) as err:
        string_search.rabin_karp_search_list('k', [9, 9])
    assert str(err.value) == 'Second argument should be a list'


def test_rubin_prime():
    """Test rabin_karp_search_list raises
    ValueError for non-positive prime value.
    """
    with pytest.raises(ValueError) as err:
        string_search.rabin_karp_search_list('k', ['9', '9'], -1)
    assert str(err.value) == 'Prime must be a positive integer'


def test_rubin_line():
    """Test rabin_karp_search_list raises
    ValueError for non-string search term.
    """
    with pytest.raises(ValueError) as err:
        string_search.rabin_karp_search_list(10, ['h', 'k'])
    assert str(err.value) == 'Search term should be a string'
