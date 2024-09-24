from configparser import ConfigParser

config = ConfigParser()

config['DEFAULT'] = {
    'SSL': 'False',
    'REREAD_ON_QUERY': 'False',
    'port': '6281',
    'linuxpath': 'Large.txt',
    'BUFFER_SIZE': '1024',
    'min_allowable_search': '10',
    'cert': 'server.crt',
    'key': 'server.key'
}


def write_file(file: str = 'config.ini') -> None:
    """
    Writes configuration data to the specified file.

    Args:
        file (str): The file name or path where the
        configuration will be written. Defaults to 'config.ini'.
    """
    try:
        with open(file, 'w') as f:
            config.write(f)
    except OSError:
        raise OSError("Could not write configuration file")


if __name__ == '__main__':
    write_file(file='config.ini')
