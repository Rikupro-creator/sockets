# Importing pytest
import pytest
import config


# Tests permission errors
def test_write_file():
    with pytest.raises(OSError) as err:
        config.write_file('etc/systemd/config.ini')
    assert str(err.value) == "Could not write configuration file"
