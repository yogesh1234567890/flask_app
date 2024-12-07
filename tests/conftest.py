import pytest
from run import app as flask_app, celery_app


@pytest.fixture(scope='session')
def app():
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture(scope='session')
def celery_worker_parameters():
    return {
        'app': celery_app,
        'queues': ['default']
    }
