import random
from tqdm import tqdm


def generate_line():
    """
    Generates a line string made up of numbers.
    Returns:
        string similar to a line in 200k.txt
    """
    line = (
        f'{random.randint(1, 25)};0;'
        f'{random.randint(1, 23)};'
        f'{random.randint(6, 28)};0;'
        f'{random.randint(5, 24)};'
        f'{random.randint(3, 5)};0;'
    )
    return line


def generate_dataset(num_lines, output_file, batch_size=10000):
    """
    Takes a number of lines and generates a txt file with
    the same number of lines.

    Args:
        num_lines (int): the number of lines the txt file
                         should have.
        output_file: the file name to save the strings.
        batch_size: number of lines to write at once (default: 10k).
    Returns:
        A txt file with the file name output_file.
    """
    unique_lines = set()  # Using a set for faster lookups
    if output_file.split('.')[-1] != 'txt':
        print('Invalid type file. Use only .txt files')
    else:
        with open(output_file, 'w') as file:
            try:
                buffer = []  # Temporary buffer for batch writing
                for _ in tqdm(range(num_lines)):
                    while True:
                        line = generate_line()
                        if line not in unique_lines:
                            unique_lines.add(line)
                            buffer.append(line)
                            break
                    if len(buffer) >= batch_size:
                        file.write("\n".join(buffer) + "\n")
                        buffer = []
                if buffer:
                    file.write("\n".join(buffer) + "\n")
            except (IOError, OSError):
                print("Error writing to file")


# Generate a million rows of data
generate_dataset(2000000, 'Million_rows.txt')

# Generate 10k rows of data
generate_dataset(10000, '10k.txt')
