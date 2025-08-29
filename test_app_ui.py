# test_app_ui.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Define the base URL of the application.
BASE_URL = "http://127.0.0.1:5000"

def test_add_new_task(driver):
    """
    Test Case TC-001: Verify adding a new task with all details.
    """
    # 1. Navigate to the homepage
    driver.get(BASE_URL)

    # 2. Find the input elements
    title_input = driver.find_element(By.NAME, "title")
    date_input = driver.find_element(By.NAME, "due_date")
    priority_select_element = driver.find_element(By.NAME, "priority")
    add_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    # 3. Enter the task details
    task_title = "Pay electricity bill"
    title_input.send_keys(task_title)
    date_input.send_keys("15-09-2025") # DD-MM-YYYY format

    # Use the Select class for dropdowns
    priority_select = Select(priority_select_element)
    priority_select.select_by_visible_text("High Priority")

    # 4. Click the "Add" button
    add_button.click()

    # 5. Verify the result
    active_tasks_list = driver.find_element(By.XPATH, "//h2[text()='Active Tasks']/following-sibling::div")
    assert task_title in active_tasks_list.text


def test_mark_task_complete(driver):
    """
    Test Case TC-002: Verify marking a task as complete.
    """
    driver.get(BASE_URL)

    # --- Setup: Add a task to be completed ---
    task_title = "Water the plants"
    driver.find_element(By.NAME, "title").send_keys(task_title)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # --- Action: Find the task and click the complete button ---
    active_tasks_list = driver.find_element(By.XPATH, "//h2[text()='Active Tasks']/following-sibling::div")
    task_card = active_tasks_list.find_element(By.XPATH, f".//p[text()='{task_title}']/ancestor::div[@class='task-card']")
    task_card.find_element(By.CSS_SELECTOR, "a[title='Mark as Complete']").click()

    # --- Assertion: Verify the task is in the completed list ---
    completed_list = driver.find_element(By.CSS_SELECTOR, ".completed-tasks")
    assert task_title in completed_list.text


def test_delete_task(driver):
    """
    Test Case TC-003: Verify deleting a task.
    """
    driver.get(BASE_URL)

    # --- Setup: Add a task to be deleted ---
    task_title = "Clean the garage"
    driver.find_element(By.NAME, "title").send_keys(task_title)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # --- Action: Find the task and click the delete button ---
    active_tasks_list = driver.find_element(By.XPATH, "//h2[text()='Active Tasks']/following-sibling::div")
    task_card = active_tasks_list.find_element(By.XPATH, f".//p[text()='{task_title}']/ancestor::div[@class='task-card']")
    task_card.find_element(By.CSS_SELECTOR, "a[title='Delete Task']").click()

    # --- Assertion: Verify the task is no longer on the page ---
    page_content = driver.find_element(By.TAG_NAME, 'body').text
    assert task_title not in page_content