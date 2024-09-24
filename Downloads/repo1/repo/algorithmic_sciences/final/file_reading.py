import mmap
import time
from typing import Callable, Tuple
import os
import pandas as pd
import numpy as np
import locale
import matplotlib.pyplot as plt


# Reads a file using open in python
def normal_open(file_name: str) -> list:
    """
    Reads and returns a file.

    Args:
        file_name (str): The path to the file.

    Returns:
        list: The file as a list of strings.
    """
    assert isinstance(file_name, str), "Filename must be a string"
    if not file_name.endswith(".txt"):
        raise TypeError("Filename must end with .txt extension")

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    except FileNotFoundError:
        raise FileNotFoundError("The file is not found in the directory.")
    except IsADirectoryError:
        raise IsADirectoryError("Oops, you provided a directory.")
    except PermissionError:
        raise PermissionError("You do not have permission to read this file.")


# Reads a file using mmap
def mmap_open(file_name: str) -> mmap.mmap:
    """
    Opens a file and returns its content as a string.

    Args:
        file_name (str): The path to the file.

    Returns:
        str: The file content as a string.
    """
    assert isinstance(file_name, str), "Filename must be a string"
    if not file_name.endswith(".txt"):
        raise TypeError("Filename must end with .txt extension")

    try:
        with open(file_name, mode="rb") as file:
            mmap_obj = mmap.mmap(
                file.fileno(), length=0, access=mmap.ACCESS_READ
            )

            return mmap_obj
    except FileNotFoundError:
        raise FileNotFoundError("The file is not found in the directory.")
    except IsADirectoryError:
        raise IsADirectoryError("Oops, you provided a directory.")
    except PermissionError:
        raise PermissionError("You do not have permission to read this file.")
    except OSError as e:
        raise OSError(f"An OS error occurred: {e}")


# Create a function to evaluate speeds
def time_evaluator(ftn: Callable, file: str):
    """
    Returns the time in milliseconds a function takes to open a file.

    Args:
        ftn (Callable): A function to read a file.
        file (str): The file name or path.

    Returns:
        float: The time it has taken to read the file.
    """
    assert isinstance(file, str), "Filename must be a string"
    assert callable(ftn), "Ftn must be a function!"
    if not file.endswith(".txt"):
        raise TypeError("Filename must end with .txt extension")

    try:
        start = time.time()
        ftn(file)
        end = time.time()
        return (end - start) * 1000
    except FileNotFoundError:
        raise FileNotFoundError("The file is not found in the directory.")
    except IsADirectoryError:
        raise IsADirectoryError("Oops, you provided a directory.")
    except OSError:
        raise OSError("Could not write configuration file")
    except PermissionError:
        raise PermissionError("You do not have permission to read this file.")


# File list and functions
files = ["10k.txt", "200k.txt", '500k .txt', 'Large.txt']
functions = [normal_open, mmap_open]
# time evaluator
tt = time_evaluator(mmap_open, '10k.txt')
# print(tt)

# Run evaluations and store results in DataFrame
results = {"algorithms": ["normal_open", "mmap"]}

for file in files:
    normal_time = time_evaluator(normal_open, file)
    mmap_time = time_evaluator(mmap_open, file)
    results[f"{file}_time"] = [normal_time, mmap_time]

df = pd.DataFrame(results)
df.to_csv('file_reading.csv')


def plot_and_save_comparison(df: pd.DataFrame, filename: str):
    """
    Plots a bar chart comparing execution times of different
    algorithms and saves it as a file.

    Args:
        df (pd.DataFrame): DataFrame containing algorithms and execution times.
        The DataFrame should have 'algorithms' as one of its columns.
        filename (str): Name of the file to save the plot.

    Returns:
        None
    """
    df.set_index('algorithms').plot(kind='bar', figsize=(10, 6))
    plt.title('Execution Time Comparison for Different Algorithms')
    plt.xlabel('Algorithm')
    plt.ylabel('Execution Time (Seconds)')
    plt.legend(title='File Size')
    plt.tight_layout()
    plt.savefig(filename)


# Create and save the plot
plot_and_save_comparison(df, 'algorithm_comparison.png')
