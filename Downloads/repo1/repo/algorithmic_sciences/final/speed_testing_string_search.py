import mmap
import os
import pandas as pd
import time
import file_reading
import string_search
import matplotlib.pyplot as plt

# Listing the files used
files = ['10k.txt', '200k.txt', '500k .txt', 'Large.txt']
# Let's define the search_line.
search_line = '25;0;23;20;0;11;5;0;'

# There are six functions in string_search.
# Let's store them into a list.
ftns = [
    string_search.binary_search,
    string_search.fibonacci_search,
    string_search.hashing_search,
    string_search.ternary_search,
    string_search.bisect_search,
    string_search.search_chunk_with_in,
    string_search.rabin_karp_search_list,
    string_search.boyer_moore_search_list,

]


def time_evaluator(ftns: list, search_line: str, lst: list,
                   reread: bool, file: str) -> pd.DataFrame:
    """
    Evaluates the time taken by different search functions to find a
    search line within a list or a file.

    Args:
        ftns (list): List of search functions to evaluate.
        search_line (str): The line to search for.
        lst (list): The list of strings in which the search is performed.
        reread (bool): Whether to reread from the file for each function.
        file (str, optional): The file path if reread is True.

    Returns:
        pd.DataFrame: A DataFrame containing the function names and the
                      time taken (in milliseconds) by each function.
    """
    times_dict = {}

    for function in ftns:
        start = time.time()
        try:
            if reread:
                if not file:
                    raise ValueError("File path must be\
                                     provided when reread is True.")
                file_ = file_reading.normal_open(file)
                data = list(file_)
            else:
                data = lst

            function(search_line, data)
        except Exception as e:
            time_taken = None
        else:
            end = time.time()
            time_taken = (end - start) * 1000  # Convert to milliseconds

        times_dict[function.__name__] = time_taken

    return pd.DataFrame(
        list(times_dict.items()), columns=['Function', 'Time (ms)']
    )


def search_chunk_with_find_time(file: str, search_term: str,
                                reread: bool) -> pd.DataFrame:
    """
    Measures the time taken by the 'search_chunk_with_find' function.

    Args:
        file (str): Path to the file to be searched.
        search_term (bytes): The term to search for in the file.
        reread (bool): Whether to reread the file content before searching.

    Returns:
        pd.DataFrame: A DataFrame containing the function name and
                      the time taken (in milliseconds).
    """
    searchterm = b'\n' + search_term.encode('utf-8') + b'\n'

    file_data = file_reading.mmap_open(file)
    start_time = time.time()

    if reread:
        file_data = file_reading.mmap_open(file)

    result = string_search.search_chunk_with_find(file_data, searchterm)

    end_time = time.time()

    return pd.DataFrame({
        'Function': ['search_chunk_with_find'],
        'Time (ms)': [(end_time - start_time) * 1000]
    })


search_lines = ['p', '12;0;13;22;0;17;5;0;',
                '22;0;2;15;0;14;5;0;',
                '14;0;4;17;0;22;3;0;',
                '14;0;4;17;0;22;3;0']


def handle_multiple(ftns: list, search_line: list[str], lst: list[str],
                    file: str, reread: bool = True) -> pd.DataFrame:
    """
    Evaluates the performance of multiple search functions
    with/without rereading a file.

    Args:
        ftns (list): List of search functions to evaluate.
        search_line (str): The line to search for.
        lst (list): The list of strings in which the search is performed.
        reread (bool): Whether to reread the file content
        before each function call.
        file (str): Path to the file if reread is True.

    Returns:
        pd.DataFrame: A DataFrame containing average execution times.
    """
    df_main = []

    for i in range(5):
        if reread:
            df = time_evaluator(
                ftns, search_line[i], lst, reread=True, file=file)
            df1 = search_chunk_with_find_time(
                        file=file, search_term=search_line[i], reread=True)
        else:
            df = time_evaluator(
                ftns, search_line[i], lst, reread=False, file=file)
            df1 = search_chunk_with_find_time(
                file, search_term=search_line[i], reread=False)

        # Concatenate the two DataFrames (df and df1) for each iteration
        dfs = pd.concat([df, df1])
        df_main.append(dfs)

    # Create the final DataFrame using the first result for the function names
    df = pd.DataFrame({
        'Function': df_main[0]['Function']
    })

    # Add each iteration's time to the DataFrame
    for i in range(5):
        df[f'attempt {i}'] = df_main[i]['Time (ms)']

    # Calculate the average time across all attempts
    df['Average time'] = df[[f'attempt {i}' for i in range(5)]].mean(axis=1)

    return df.round(4)


def create_df(
        ftns: list, search_line: list[str],
        lst: list[list], file: list[str]) -> dict:
    """
    Creates and returns a dictionary of DataFrames by running the
    `handle_multiple` functionfor each combination of list (`lst`)
    and file (`file`), with both reread=True and reread=False.

    For each file in the `file` list, it calculates performance
    metrics for search functionswith and without rereading the
    file content. The results are stored in a dictionary where
    the keys are the file names appended with '_reread_false'
    or '_reread_true', and the values are the corresponding DataFrames.

    Args:
        ftns (list): List of search functions to evaluate.
        search_line (str): The search line to be used in the functions.
        lst (list[list]): A list of lists, where each inner list
        represents a dataset to be searched.
        file (list[str]): A list of file paths corresponding to each dataset.

    Returns:
        dict: A dictionary where each key is a string
        combining the file name with either'_reread_false' or '_reread_true',
        and each value is a DataFrame containing the results of the
        `handle_multiple` function for that configuration.
    """

    df = {}
    for i in range(len(lst)):
        df[f'{file[i]}_reread_false'] = handle_multiple(ftns,
                                                        search_line, lst[i],
                                                        reread=False,
                                                        file=file[i])
        df[f'{file[i]}_reread_true'] = handle_multiple(ftns,
                                                       search_line,
                                                       lst[i],
                                                       reread=True,
                                                       file=file[i])
    return df


# lets create a list of lists
lst = [file_reading.normal_open(i) for i in files]

trial = create_df(ftns, search_lines, lst,
                  files)
print(trial.keys())


# Function to plot and save average time for a given dataframe
def plot_and_save(df, title, filename):
    """
    Creates a horizontal bar plot for average execution
    times and saves it as a file.

    Args:
        df (pd.DataFrame): DataFrame containing average times for functions.
        title (str): Title of the plot.
        filename (str): File name to save the plot.

    Returns:
        None
    """
    plt.figure(figsize=(12, 8))
    sorted_df = df.sort_values(by='Average time')
    plt.barh(sorted_df['Function'],
             sorted_df['Average time'], color='skyblue')
    plt.title(title)
    plt.xlabel('Average time')
    plt.ylabel('Function')
    plt.tight_layout()
    plt.savefig(filename)  # Save the plot as a PNG file
    plt.show()  # Display the plot


for i, j in trial.items():
    plot_and_save(j, f'{i} time taken', f'{i}.png')
    j.to_csv(f'{i}.csv')
