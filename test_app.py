import pytest
from app import create_app, db, Task

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_tasks.db',  # Use a separate test database
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    
    # Create the database tables for testing
    with app.app_context():
        db.create_all()  # Create the tables in the test database
    
    yield app
    
    # Cleanup after tests
    with app.app_context():
        db.drop_all()  # Drop tables after tests are done

@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_task(client):
    """Create a sample task for use in tests."""
    task = Task(task="Sample Task")
    db.session.add(task)
    db.session.commit()
    return task

def test_index(client, sample_task):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Sample Task" in response.data  # Verify task appears on the page

def test_add_task(client):
    response = client.post('/add', data={'task': 'New Task'})
    assert response.status_code == 302  # Expecting a redirect to index
    assert Task.query.filter_by(task='New Task').first()  # Check that the task was added

def test_complete_task(client, sample_task):
    response = client.get(f'/complete/{sample_task.id}')
    assert response.status_code == 302  # Redirect after completion
    task = Task.query.get(sample_task.id)
    assert task.completed is True  # Ensure the task is marked as completed

def test_delete_task(client, sample_task):
    response = client.get(f'/delete/{sample_task.id}')
    assert response.status_code == 302  # Redirect after deletion
    task = Task.query.get(sample_task.id)
    assert task is None  # Ensure the task was deleted

