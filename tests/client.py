import tempfile
import pytest

import os
import sys
sys.path.append(os.path.abspath('../application'))

import server


@pytest.fixture
def client():
    db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(server.app.config['DATABASE'])
