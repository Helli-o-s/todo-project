# test_app_api.py

import random
import re
import string

def create_test_task(client, title):
    """Helper function to create a task using the test client."""
    payload = {"title": title, "due_date": "", "priority": "Medium"}
    # Use client.post; follow_redirects=False is the new allow_redirects
    response = client.post("/add", data=payload, follow_redirects=False)
    assert response.status_code == 302
    return payload

def get_task_id(client, title):
    """Helper function to find a task's ID from the homepage."""
    response = client.get("/")
    # response.text becomes response.data.decode()
    html_content = response.data.decode()
    match = re.search(fr'<p class="task-title">{title}</p>.*?/(?:update|delete)/(\d+)', html_content, re.DOTALL)
    assert match, f"Could not find the task ID for '{title}' on the page"
    return match.group(1)

def test_add_task_api(client):
    """Tests the /add endpoint."""
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    task_title = f"My Full API Task_{random_suffix}"
    payload = {"title": task_title, "due_date": "2025-12-31", "priority": "High"}
    
    add_response = client.post("/add", data=payload, follow_redirects=False)
    assert add_response.status_code == 302
    
    get_response = client.get("/")
    assert get_response.status_code == 200
    assert task_title in get_response.data.decode()

def test_update_task_api(client):
    """Tests the /update endpoint."""
    task_title = "My task to complete_" + ''.join(random.choices(string.ascii_letters, k=5))
    create_test_task(client, task_title)
    task_id = get_task_id(client, task_title)

    update_response = client.get(f"/update/{task_id}", follow_redirects=False)
    assert update_response.status_code == 302

    final_response = client.get("/")
    html_content = final_response.data.decode()
    completed_section_match = re.search(
    r'<div class="task-list completed-tasks">.*?<h2>Completed Tasks</h2>(.*?)</div>\s*</div>',
    html_content.text,
    re.DOTALL,)
    assert completed_section_match and task_title in completed_section_match.group(1)

def test_delete_task_api(client):
    """Tests the /delete endpoint."""
    task_title = "My task to delete_" + ''.join(random.choices(string.ascii_letters, k=5))
    create_test_task(client, task_title)
    task_id = get_task_id(client, task_title)
    
    delete_response = client.get(f"/delete/{task_id}", follow_redirects=False)
    assert delete_response.status_code == 302
    
    final_response = client.get("/")
    assert task_title not in final_response.data.decode()