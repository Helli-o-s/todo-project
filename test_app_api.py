# test_app_api.py

import random
import re
import string

# Define the base URL of the running application.
BASE_URL = "http://127.0.0.1:5000"

def create_test_task(requests_session, title):
    """Helper function to create a task via API and return its data."""
    payload = {
        "title": title,
        "due_date": "", 
        "priority": "Medium"
    }
    # THE FIX: Disable redirects to check the initial 302 response.
    response = requests_session.post(f"{BASE_URL}/add", data=payload, allow_redirects=False)
    assert response.status_code == 302 # Ensure setup task was created
    return payload

def get_task_id(requests_session, title):
    """Helper function to find a task's ID from the homepage."""
    response = requests_session.get(BASE_URL)
    match = re.search(fr'<p class="task-title">{title}</p>.*?/(?:update|delete)/(\d+)', response.text, re.DOTALL)
    assert match, f"Could not find the task ID for '{title}' on the page"
    return match.group(1)


def test_add_task_api(requests_session):
    """Tests the /add endpoint to ensure a task can be created with full details."""
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    task_title = f"My Full API Task_{random_suffix}"

    payload = {"title": task_title, "due_date": "2025-12-31", "priority": "High"}
    # THE FIX: Disable redirects here as well.
    add_response = requests_session.post(f"{BASE_URL}/add", data=payload, allow_redirects=False)

    assert add_response.status_code == 302
    
    # This part remains the same, as we still need to check the final state.
    get_response = requests_session.get(BASE_URL)
    assert get_response.status_code == 200
    assert task_title in get_response.text

def test_update_task_api(requests_session):
    """Tests the /update endpoint."""
    task_title = "My task to complete_" + ''.join(random.choices(string.ascii_letters, k=5))
    create_test_task(requests_session, task_title)
    task_id = get_task_id(requests_session, task_title)

    # THE FIX: The update link also redirects, so disable it here.
    update_response = requests_session.get(f"{BASE_URL}/update/{task_id}", allow_redirects=False)

    assert update_response.status_code == 302

    final_response = requests_session.get(BASE_URL)
    completed_section_match = re.search(r'<div class="task-list completed-tasks">.*?</div>', final_response.text, re.DOTALL)
    assert completed_section_match and task_title in completed_section_match.group(0)

def test_delete_task_api(requests_session):
    """Tests the /delete endpoint."""
    task_title = "My task to delete_" + ''.join(random.choices(string.ascii_letters, k=5))
    create_test_task(requests_session, task_title)
    task_id = get_task_id(requests_session, task_title)
    
    # THE FIX: The delete link also redirects, so disable it here.
    delete_response = requests_session.get(f"{BASE_URL}/delete/{task_id}", allow_redirects=False)
    
    assert delete_response.status_code == 302
    
    final_response = requests_session.get(BASE_URL)
    assert task_title not in final_response.text