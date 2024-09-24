import mmap
import concurrent.futures
from file_reading import normal_open, mmap_open
import bisect
import time
import os
from concurrent.futures import ThreadPoolExecutor


# 1. Searching using `in`
def search_line_in_file(search_line: str, list_file: list) -> bool:
    """
    Searches for a line in a list using the `in` keyword.

    Args:
        search_line (str): The line to search for.
        list_file (list): The list of lines to search within.

    Returns:
        str: Prints the matching line(s) or indicates no matches found.
    """
    if type(search_line) != str:
        raise ValueError('Search term should be a string')
    try:
        matching_lines = [line.strip() for line in
                          list_file if line.strip() == search_line]
        if matching_lines:
            return True
        else:
            return False
    except TypeError:
        raise TypeError('Ensure search line is a string\
                         or list_file is a list')
    except AttributeError:
        raise AttributeError('There is an integer in the list')


# 2. Binary Search
def binary_search(search_line: str, list_file: list) -> bool:
    """
    Performs binary search on a sorted list to find the search line.

    Args:
        search_line (str): The line to search for.
        list_file (list): The list of lines to search within.

    Returns:
        bool: True if the line is found, otherwise False.
    """
    if type(search_line) != str:
        raise ValueError('Search term should be a string')
    try:
        lines = sorted([line.strip() for line in list_file])
        low, high = 0, len(lines) - 1
        while low <= high:
            mid = (low + high) // 2
            if lines[mid] == search_line:
                return True
            elif lines[mid] < search_line:
                low = mid + 1
            else:
                high = mid - 1
        return False
    except TypeError:
        raise TypeError('Ensure search line is a string\
                         or list_file is a list')
    except AttributeError:
        raise AttributeError('There is an integer in the list')


# 3. Fibonacci Search
def fibonacci_search(search_line: str, sorted_lines: list) -> int:
    """
    Performs Fibonacci search on a sorted list to find the search line.

    Args:
        search_line (str): The line to search for.
        sorted_lines (list): A sorted list of lines to search within.

    Returns:
        int: The index of the found line, or -1 if not found.
    """
    if type(search_line) != str:
        raise ValueError('Search term should be a string')
    try:
        sorted_lines = sorted(sorted_lines)
        n = len(sorted_lines)

        fib2 = 0  # (m-2)'th Fibonacci number
        fib1 = 1  # (m-1)'th Fibonacci number
        fibM = fib1 + fib2  # m'th Fibonacci number

        while fibM < n:
            fib2 = fib1
            fib1 = fibM
            fibM = fib1 + fib2

        offset = -1

        while fibM > 1:
            i = min(offset + fib2, n - 1)
            if sorted_lines[i].strip() < search_line:
                fibM = fib1
                fib1 = fib2
                fib2 = fibM - fib1
                offset = i
            elif sorted_lines[i].strip() > search_line:
                fibM = fib2
                fib1 = fib1 - fib2
                fib2 = fibM - fib1
            else:
                return i

        if fib1 and offset + 1 < n and\
                sorted_lines[offset + 1].strip() == search_line:
            return offset + 1

        return -1
    except TypeError as e:
        raise TypeError('Second argument should be a list of strings')


# 4. Ternary Search
def ternary_search(search_line: str, lines: list) -> int:
    """
    Performs ternary search on a sorted list to find the search line.

    Args:
        search_line (str): The line to search for.
        lines (list): The list of lines to search within.

    Returns:
        int: The index of the found line, or -1 if not found.
    """
    if type(search_line) != str:
        raise ValueError('Search term should be a string')
    try:
        sorted_lines = sorted(lines)
        left = 0
        right = len(sorted_lines) - 1

        while right >= left:
            mid1 = left + (right - left) // 3
            mid2 = right - (right - left) // 3

            if sorted_lines[mid1].strip() == search_line:
                return mid1
            if sorted_lines[mid2].strip() == search_line:
                return mid2

            if search_line < sorted_lines[mid1].strip():
                right = mid1 - 1
            elif search_line > sorted_lines[mid2].strip():
                left = mid2 + 1
            else:
                left = mid1 + 1
                right = mid2 - 1

        return -1
    except TypeError:
        raise TypeError('Second argument should be a list of strings')
    except AttributeError:
        raise AttributeError('There is an integer in the list')


# 6. Hashing with Dictionary
def hashing_search(search_line: str, line_file: list) -> bool:
    """
    Searches for a line using a dictionary (hashmap) for fast lookup.

    Args:
        search_line (str): The line to search for.
        line_file (list): The list of lines to search within.

    Returns:
        bool: True if the line is found, otherwise False.
    """
    if type(search_line) != str:
        raise ValueError('Search term should be a string')
    try:
        line_dict = {line.strip(): True for line in line_file}
        return search_line in line_dict
    except TypeError:
        raise TypeError('Ensure search line is a string\
                        or list_file is a list')
    except AttributeError:
        raise AttributeError('There is an integer in the list')


# 8. Bisect Search
def bisect_search(item_to_search: str, lst: list) -> str:
    """
    Performs binary search on a sorted list to find the target value.

    Args:
        item_to_search (str): The item to search for.
        lst (list): A sorted list.

    Returns:
        str: "STRING EXISTS" if the item is found,
             otherwise "STRING NOT FOUND".
    """
    if type(item_to_search) != str:
        raise ValueError('Search term should be a string')
    try:
        index = bisect.bisect_left(lst, item_to_search)
        if index != len(lst) and lst[index] == item_to_search:
            return "STRING EXISTS\n"
        return "STRING NOT FOUND\n"
    except TypeError as e:
        raise TypeError('Second argument should be a list of strings')


# 9. Search Chunks Using `in`
def search_chunk_with_in(search_term: str, chunk: list) -> bool:
    """
    Searches for a search_term in a given chunk of data using `in`.

    Args:
        chunk (list): A chunk of file data.
        search_term (str): The term to search for.

    Returns:
        bool: True if the search term is found, False otherwise.
    """
    if type(search_term) != str:
        raise ValueError('Search term should be a string')
    try:
        return search_term in chunk
    except TypeError:
        raise TypeError('Ensure search line is a string\
                        or list_file is a list of strings')


# 10. Search Chunks Using `find` (Best for mmap objects)
def search_chunk_with_find(chunk: mmap.mmap, search_term: bytes) -> int:
    """
    Searches for a search_term in a given chunk of bytes data.

    Args:
        chunk (bytes): A chunk of file data.
        search_term (bytes): The term to search for.

    Returns:
        bool: True if search term found, otherwise False.
    """
    if type(search_term) != bytes:
        raise ValueError('Search term should be a bytes')
    if type(chunk) != mmap.mmap:
        raise ValueError('Chunk should be mmap object')
    chunk1 = b'\n' + chunk
    return chunk1.find(search_term)


# 11 Boyer_moore
def boyer_moore_search_list(pattern: str, text_list: list) -> int:
    """
    Implements the Boyer-Moore string search algorithm for a list of strings.

    Args:
        text_list (list): The list of strings to search within.
        pattern (str): The pattern to search for.

    Returns:
        int: The starting index of the pattern if found, otherwise -1.
    """
    if type(pattern) != str:
        raise ValueError('Search term should be a string')
    try:
        # Check if all items in text_list can be concatenated (assumed strings)
        text = ''.join(text_list).encode('utf-8')
    except TypeError:
        raise TypeError("Second argument should be a list")

    pattern_bytes = pattern.encode('utf-8')

    m = len(pattern_bytes)
    n = len(text)

    if m > n:
        return -1

    # Bad Character Heuristic
    skip = {pattern_bytes[i]: m - i - 1 for i in range(m - 1)}

    i = m - 1
    while i < n:
        j = m - 1
        while j >= 0 and text[i - m + j + 1] == pattern_bytes[j]:
            j -= 1
        if j < 0:
            return i - m + 1
        i += skip.get(text[i], m)

    return -1


def rabin_karp_search_list(pattern: str, text_list: list, prime=101) -> bool:
    """
    Search for a pattern in a list of strings using the Rabin-Karp algorithm.

    Args:
        text_list (list): The list of strings to search within.
        pattern (str): The pattern to search for.
        prime (int): A prime number used for hashing (default is 101).

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
    """
    if type(pattern) != str:
        raise ValueError('Search term should be a string')
    try:
        # Ensure text_list can be concatenated into a single string
        text = ''.join(text_list).encode('utf-8')
    except TypeError:
        raise TypeError("Second argument should be a list")

    pattern_bytes = pattern.encode('utf-8')

    if prime <= 0:
        raise ValueError("Prime must be a positive integer")

    pattern_len = len(pattern_bytes)
    text_len = len(text)
    if pattern_len > text_len:
        return False

    pattern_hash = 0
    text_hash = 0
    h = pow(256, pattern_len - 1, prime)

    # Calculate the hash value for the pattern and the first window of the text
    for i in range(pattern_len):
        pattern_hash = (256 * pattern_hash + pattern_bytes[i]) % prime
        text_hash = (256 * text_hash + text[i]) % prime

    # Slide the window over the text to find the pattern
    for i in range(text_len - pattern_len + 1):
        # Check if the hash values are the same and verify the actual text
        if pattern_hash == text_hash:
            if text[i:i + pattern_len] == pattern_bytes:
                return True

        # Update the hash value for the next window of text
        if i < text_len - pattern_len:
            text_hash = (256 * (text_hash - text[i] * h) +
                         text[i + pattern_len]) % prime
            if text_hash < 0:
                text_hash += prime

    return False
