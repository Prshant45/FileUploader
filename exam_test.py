import pytest
import mock
from exam import get_storage_config

@mock.patch('builtins.input', side_effect=['', 's3.txt',
 '', 'gcloud.txt'])
def test_get_storage_config(self):
    assert get_storage_config()