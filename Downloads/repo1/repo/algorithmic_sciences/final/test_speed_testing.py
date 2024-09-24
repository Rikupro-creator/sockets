import pytest
import pandas as pd
import file_reading
import string_search
from speed_testing_string_search import (
    time_evaluator, search_chunk_with_find_time,
    handle_multiple, create_df, plot_and_save
    )

# Sample test data
search_line = '25;0;23;20;0;11;5;0;'
files = ['10k.txt', 'Million_rows.txt']
lst = [file_reading.normal_open(f) for f in files]


# Test the time_evaluator function, ensuring it returns a DataFrame
def test_time_evaluator():
    """Test time_evaluator function."""
    ftns = [string_search.binary_search]
    df = time_evaluator(ftns, search_line,
                        lst[0], reread=False, file=None)
    assert isinstance(df, pd.DataFrame)
    assert 'Function' in df.columns
    assert 'Time (ms)' in df.columns


# Test the search_chunk_with_find_time function,
# ensuring it returns a DataFrame
def test_search_chunk_with_find_time():
    """Test search_chunk_with_find_time function."""
    df = search_chunk_with_find_time(files[0], search_line, reread=False)
    assert isinstance(df, pd.DataFrame)
    assert 'Function' in df.columns
    assert 'Time (ms)' in df.columns


# Test the handle_multiple function,
# ensuring it returns a DataFrame
def test_handle_multiple():
    """Test handle_multiple function."""
    df = handle_multiple([string_search.binary_search],
                         search_line, lst[0], files[0])
    assert isinstance(df, pd.DataFrame)
    assert 'Function' in df.columns
    assert 'Average time' in df.columns


# Test the create_df function, ensuring it returns a dictionary
def test_create_df():
    """Test create_df function."""
    df_dict = create_df([string_search.binary_search],
                        search_line, lst, files)
    assert isinstance(df_dict, dict)
    for key, df in df_dict.items():
        assert isinstance(df, pd.DataFrame)
        assert 'Function' in df.columns
        assert 'Average time' in df.columns


# Test the plot_and_save function, ensuring it saves a plot.
def test_plot_and_save(tmp_path):
    """Test plot_and_save function."""
    df = pd.DataFrame({
        'Function': ['test_func'],
        'Average time': [123.45]
    })
    filename = tmp_path / 'test_plot.png'
    plot_and_save(df, 'Test Plot', filename)
    assert filename.exists()
