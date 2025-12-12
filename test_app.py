import pytest
import os
os.environ["TEST_DB"] = "test_tasks.db"
from app import app
import database as db

# Use test database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")
    db.create_table()
    with app.test_client() as client:
        yield client
    if os.path.exists("test_tasks.db"):
        os.remove("test_tasks.db")
        
def test_get_tasks_empty(client):
    response = client.get('/api/tasks')
    
    assert response.json == []
    assert response.status_code == 200
def test_create_task(client):
    response = client.post('/api/tasks' , json = {'title' : 'test1st tasks' ,'description' : 'test1st description',
                                           'priority' : 'High','due_date' : 'test1st due_date',
                                           'category' : 'test1st category'})
    
    assert response.status_code == 201
    assert 'Task created successfully' in response.json['message']
def test_get_tasks_with_id(client):
    client.post('/api/tasks', json={'title': 'Old Title', 'category': 'Work'})
    response = client.get('/api/tasks/1')
    assert response.json['id'] == 1
    assert response.status_code == 200   
def test_get_nonexistent_task(client):
    response = client.get('/api/tasks/400')
    assert 'error' in response.json
    assert response.status_code == 404
def test_update_task(client):
    client.post('/api/tasks', json={'title': 'Old Title', 'category': 'Work'})
    
    response = client.put('/api/tasks/1', json={
        'title': 'New Title',
        'status': 'Completed'
    })
    assert response.status_code == 200
    assert 'message' in response.json

    response = client.get('/api/tasks/1')
    
    assert response.json['title'] == 'New Title'
    assert response.json['status'] == 'Completed'
def test_update_nonexistent_task(client):
    response = client.put('/api/tasks/400', json={'title': 'Old Title', 'category': 'Work'})
    assert response.status_code == 404
    assert 'error' in response.json 
def test_delete_task(client):
    client.post('/api/tasks' , json={'title': 'Old Title', 'category': 'Work'})
    
    response = client.delete('/api/tasks/1')
    assert 'message' in response.json
    assert response.status_code == 200
    
    response = client.get('/api/tasks/1')
    assert response.status_code == 404
def test_delete_nonexistent_task(client):
    response = client.delete('/api/tasks/400')
    assert response.status_code == 404
    assert 'error' in response.json
     
    

 
 
    
    
    
            
        
        