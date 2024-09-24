import pandas as pd

# URL for the Dropbox file (replace with the actual URL)
url = 'https://www.dropbox.com/scl/fi/ripx1gu2s5w48pklln75f/200k.txt?' \
      'rlkey=j7l29szvqw0hlyyfhw4i4b1on&e=1&st=wfkjn1sr&dl=1'

# Local filename for the downloaded data (modify as needed)
output_filename = '200k.txt'

try:
    # Read the TSV file using pandas.read_table
    data = pd.read_table(url)
    print("File read successfully!")

    data_string = data.to_string(index=False)
    data_string = '\n'.join(line.lstrip()
                            for line in data_string.splitlines())

    # Save the string to a text file
    with open(output_filename, 'w') as f:
        f.write(data_string)
        print(f"Data saved to '{output_filename}'.")

except Exception as e:
    print(f"Error reading or saving file: {e}")