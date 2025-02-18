import sys
import os  
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tabulate import tabulate  # Required for printing tables
from selenium.common.exceptions import SessionNotCreatedException

# 1️⃣ Configuration
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://selenium-chrome:4444/wd/hub")
HEADLESS_MODE = True  # If set to False, Windowed mode will be enabled

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  
options.add_argument("--allow-insecure-localhost")  
options.add_argument("--incognito")  

if HEADLESS_MODE:
    options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 2. Steps

## Step 1: Visit the Home page and verify it loads
def visit_home_page():
    retries = 3
    for attempt in range(retries):
        try:
            log_message("🔄 Opening Home page...")
            driver.get("https://useinsider.com/")
            wait_for_page_load(driver, timeout=10)  # Wait for the page to fully load
            accept_cookies()  # Call the function to accept cookies
            assert "Insider" in driver.title  # Verify that the title is correct
            log_message("✅ Home page successfully loaded.")
            break
        except Exception as e:
            if attempt < retries - 1:
                log_message(f"⚠️ Retry {attempt + 1} failed, retrying...")
                time.sleep(2)
            else:
                log_message(f"❌ Home page loading failed after {retries} attempts: {e}")
                
# Step 2: Navigate to the "Careers" page
def navigate_to_careers_page():
    retries = 3
    for attempt in range(retries):
        try:
            log_message("🔄 Navigating to Careers page...")
            
            # Click on the "Company" dropdown menu
            company_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='#'][contains(text(), 'Company')]"))
            )
            company_menu.click()  # Click on the dropdown menu
            time.sleep(2)  # Wait for the menu to open
            
            # Click on the "Careers" link from the dropdown
            careers_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Careers')]"))
            )
            careers_link.click()  # Click on the "Careers" link
            
            # Wait for the page to load
            wait_for_page_load(driver, timeout=5)

            # Verify that the Careers page has fully loaded
            log_message("✅ Careers page successfully loaded.")
            break
        except Exception as e:
            if attempt < retries - 1:
                log_message(f"⚠️ Retry {attempt + 1} failed, retrying...")
                time.sleep(2)
            else:
                log_message(f"❌ Failed to navigate to Careers page: {e}")

# Step 3: Verify required elements on the Careers page
def verify_required_elements():
    retries = 3
    for attempt in range(retries):
        try:
            log_message("🔄 Verifying required elements on the Careers page...")

            # Step 1: Ensure the page is fully loaded
            wait_for_page_load(driver, timeout=10)
            time.sleep(1)  # Give it an additional second for stability

            # Step 2: Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the scroll to finish
            
            # Step 3: Verify the "See all teams" button is present
            teams_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all teams')]"))
            )
            assert teams_button.is_displayed(), "'See all teams' button is not visible"
            log_message("✅ 'See all teams' button is visible.")

            time.sleep(0.5)  # Wait 0.5 seconds before moving to the next element

            # Step 4: Verify "Our Locations" is present
            locations_header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Our Locations')]"))
            )
            assert locations_header.is_displayed(), "'Our Locations' header is not visible"
            log_message("✅ 'Our Locations' header is visible.")

            time.sleep(0.5)  # Wait 0.5 seconds before moving to the next element

            # Step 5: Verify "Life at Insider" is present
            life_header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Life at Insider')]"))
            )
            assert life_header.is_displayed(), "'Life at Insider' header is not visible"
            log_message("✅ 'Life at Insider' header is visible.")

            time.sleep(0.5)  # Wait 0.5 seconds after verification

            log_message("✅ All required elements are visible on the Careers page.")
            break
        except Exception as e:
            if attempt < retries - 1:
                log_message(f"⚠️ Retry {attempt + 1} failed, retrying...")
                time.sleep(2)
            else:
                log_message(f"❌ Failed to verify elements: {e}")

# Step 4: Go to 'See all QA jobs' page
def navigate_to_qa_jobs():
    retries = 3
    for attempt in range(retries):
        try:
            log_message("🔄 Navigating to QA Jobs page...")

            # Go to the Quality Assurance careers page
            driver.get("https://useinsider.com/careers/quality-assurance/")
            wait_for_page_load(driver, timeout=10)
            time.sleep(0.5)  # Allow time for page load

            log_message("🔄 Clicking 'See all QA jobs' button...")

            # Click the 'See all QA jobs' button
            see_all_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
            )
            see_all_button.click()  # Click the button

            log_message("✅ 'See all QA jobs' button clicked. Waiting for the new page to load...")

            # Wait for the new page to load (new page with jobs list)
            wait_for_page_load(driver, timeout=10)
            time.sleep(0.5)  # Allow time for page load

            log_message("✅ Successfully navigated to the QA jobs list page.")
            break
        except Exception as e:
            if attempt < retries - 1:
                log_message(f"⚠️ Retry {attempt + 1} failed, retrying...")
                time.sleep(2)
            else:
                log_message(f"❌ Failed to navigate to 'See all QA jobs' page: {e}")

# Step 5: Apply filters and check job listings
def filter_jobs():
    log_message("⏳ Waiting 5 seconds before checking department filter...")
    time.sleep(5)  # 🔹 Waiting 5 seconds to ensure the page fully loads

    retries = 7
    for attempt in range(retries):
        try:
            log_message(f"🔄 Checking if Department filter is selected... (Attempt {attempt + 1})")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "select2-filter-by-department-container"))
            )

            # **Read the value of the Department filter**
            department_element = driver.find_element(By.ID, "select2-filter-by-department-container")
            selected_department = department_element.text.strip()

            # **If there is an "×" symbol, clean it**
            if "×" in selected_department:
                selected_department = selected_department.split("×")[-1].strip()

            log_message(f"🔍 Final read from department filter: {selected_department}")  # ✅ DEBUG LOG

            if selected_department == "Quality Assurance":
                log_message("✅ Department filter successfully detected!")
                break  

        except Exception as e:
            log_message(f"⚠️ Department filter not detected yet: {e}")

        time.sleep(2)

    # **✅ Mandatory Manual Application of Location Filter (Based on Previous Experience)**
    log_message("🔄 Ensuring 'Istanbul, Turkiye' appears in the filter...")

    for attempt in range(3):  # Attempt up to 3 times
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-labelledby='select2-filter-by-location-container']"))
        )
        dropdown.click()
        time.sleep(2)

        options = driver.find_elements(By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
        if options:
            log_message("📍 Found option: Istanbul, Turkiye")
            options[0].click()
            log_message("✅ Selected 'Istanbul, Turkiye'.")
            break  # Exit if successful
        else:
            log_message(f"⚠️ Attempt {attempt + 1}: 'Istanbul, Turkiye' not found, retrying...")
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(2)
    else:
        log_message("❌ Failed to select 'Istanbul, Turkiye'.")
        driver.quit()
        exit()

    # **🔄 Wait 5 seconds after applying filters**
    log_message("⏳ Waiting 5 seconds after filters are applied...")
    time.sleep(5)

    # **🔄 Finally, check the 'Showing' section**
    wait_for_valid_showing()

    log_message("✅ Filters applied successfully!")

# Step 6: Verify job list and check positions
def verify_jobs():
    log_message("⏳ Waiting 5 seconds to ensure filters are applied...")
    time.sleep(5)

    # **Step 1: Scroll down and up**
    log_message("🔄 Scrolling down...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    log_message("🔄 Scrolling up...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    # **Step 2: Re-check the 'Showing' section**
    log_message("🔄 Re-checking 'Showing' section after scrolling...")

    showing_valid = False
    showing_text = ""

    for attempt in range(10):  # Attempt up to 10 times
        try:
            showing_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "resultCounter"))
            ).text

            log_message(f"🔍 Attempt {attempt + 1} - Read from 'Showing' section: {showing_text}")

            if "NaN" not in showing_text and "Showing" in showing_text:
                showing_valid = True
                break
        except:
            log_message("⚠️ 'Showing' section not found, retrying...")
        time.sleep(0.5)

    if not showing_valid:
        log_message("❌ 'Showing' section did not resolve after retries!")
        return

    # **Step 3: Collect job listings dynamically into an array**
    log_message("🔄 Checking job listings...")
    
    job_list = []  # Main array where jobs are stored
    job_retries = 10
    for attempt in range(job_retries):
        job_elements = driver.find_elements(By.CLASS_NAME, "position-list-item")
        
        for job in job_elements:
            job_title = job.find_element(By.CLASS_NAME, "position-title").text.strip()
            job_department = job.find_element(By.CLASS_NAME, "position-department").text.strip()
            job_location = job.find_element(By.CLASS_NAME, "position-location").text.strip()

            # **For filtering: Only include locations that contain "Turkey" or "Turkiye"**
            if "Turkey" in job_location or "Turkiye" in job_location:
                job_list.append([job_title, job_department, job_location])  # Store in array format
                log_message(f"✅ Job added: {job_title} | {job_department} | {job_location}")
        
        # **Exit if enough jobs have been found**
        if len(job_list) >= 4:
            break
        else:
            log_message(f"⚠️ Not enough valid jobs found ({len(job_list)}), retrying...")
            time.sleep(0.5)

    if len(job_list) >= 4:
        log_message("✅ Successfully gathered 4 unique jobs!")

        # **📌 PRINT JOB LIST AS A TABLE**
        print("\n📌 Latest found QA jobs in Turkey:\n")
        print(tabulate(job_list[:4], headers=["Job Name", "Department", "Location"], tablefmt="pretty"))

    else:
        log_message("❌ Could not find 4 valid jobs after retries!")
       
# Step 7: Click "View Role" button and verify redirection
def click_view_role_button():
    log_message("🔄 Hovering over the first job to activate 'View Role' button...")
    
    try:
        # Locate the first job listing element
        first_job = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "position-list-item"))
        )

        # Perform a mouse hover to activate the 'View Role' button
        ActionChains(driver).move_to_element(first_job).perform()
        time.sleep(1)

        # Locate the 'View Role' button
        view_role_button = first_job.find_element(By.XPATH, ".//a[contains(text(), 'View Role')]")

        # Click using JavaScript (as a precaution)
        log_message("🔄 Clicking 'View Role' for the first job...")
        driver.execute_script("arguments[0].click();", view_role_button)
        time.sleep(3)  # Wait for the new page to load

        # Wait for the new tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        log_message("✅ Switched to the new tab.")

        # Wait for the redirected page to fully load
        wait_for_page_load(driver, timeout=10)

        # Validate the URL
        current_url = driver.current_url
        assert "jobs.lever.co" in current_url, f"❌ Unexpected URL: {current_url}"
        log_message(f"✅ Successfully redirected to Lever job page: {current_url}")

    except Exception as e:
        log_message(f"❌ Failed to click 'View Role' and verify redirection: {e}")

# 3. Mechanisms and Helper Functions

# Accept cookies
def accept_cookies():
    try:
        log_message("🔄 Checking for cookie popup...")
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
        )
        accept_button.click()
        log_message("✅ Accepted cookies.")
        time.sleep(5)
    except:
        log_message("⚠️ No cookie banner found or already accepted.")
        
# Page loading check function
def wait_for_page_load(driver, timeout=10):
    """Waits for the page to fully load"""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    log_message("✅ Page fully loaded.")
    time.sleep(2)  # Wait for 2 seconds after full page load

# Log message function
def log_message(message):
    """Logs each step with a timestamp"""
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def wait_for_valid_showing():
    retries = 5
    for attempt in range(retries):
        try:
            showing_text = driver.find_element(By.ID, "resultCounter").text.strip()
            log_message(f"🔍 Read from 'Showing' section: {showing_text}")

            # Check for NaN values
            if "NaN" not in showing_text and "Showing" in showing_text:
                log_message(f"✅ 'Showing' section is valid: {showing_text}")
                return  # If a valid value appears, terminate the process

        except Exception as e:
            log_message(f"⚠️ 'Showing' section not found yet: {e}")

        log_message(f"⚠️ 'Showing' section invalid (Attempt {attempt + 1}), retrying...")
        time.sleep(2)

    log_message("❌ 'Showing' section still invalid after retries.")



# 4. Test Completion
log_message("✅ Test completed successfully.")
log_message("🔄 Keeping browser open for further inspection...")

# Run steps sequentially
# 🔄 **Infinite loop - test sequence runs continuously inside the same browser session**

max_retries = 5
retry_delay = 10

while True:
    print("🔄 Starting a new test session...")

    retries = 0
    while retries < max_retries:
        try:
            driver = webdriver.Remote(command_executor=SELENIUM_REMOTE_URL, options=options)
            print("✅ WebDriver session created successfully.")
            break
        except SessionNotCreatedException as e:
            print(f"⚠️ Session creation failed. Retrying in {retry_delay} seconds... ({retries+1}/{max_retries})")
            retries += 1
            time.sleep(retry_delay)
    else:
        print("❌ Maximum retries reached. Restarting loop...")
        continue  # Yeni loop iterasiyasına başla

    try:
        # Testləri icra et
        visit_home_page()
        navigate_to_careers_page()
        verify_required_elements()
        navigate_to_qa_jobs()
        filter_jobs()
        verify_jobs()
        click_view_role_button()
        print("✅ Test session completed successfully.")
        driver.quit()
    except Exception as e:
        print(f"❌ Test session failed: {e}")

    print("⏳ Waiting 10 seconds before restarting the test...")
    time.sleep(10)
