import os
import tempfile

import pytest

from project import create_app


@pytest.fixture
def client():
    app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        yield client  # this is where the testing happens!