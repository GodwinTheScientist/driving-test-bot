import time
import yagmail
import schedule
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# === USER CONFIG ===
LICENSE_NUMBER = 'UMEAK905191GC9TK'
BOOKING_REFERENCE = '66384654'
CURRENT_TEST_DATE = datetime(2025, 8, 28, 8, 57)
CUTOFF_DATE = datetime(2025, 6, 30)
TEST_CENTRES = ['Bredbury', 'Macclesfield', 'East Didsbury']
EMAIL_RECEIVER = 'eumeaka@gmail.com'
EMAIL_SENDER = 'eumeaka@gmail.com'
EMAIL_PASSWORD = 'jetg ekza sklc kkhe'
# ====================

def send_email_notification(date_found, centre_name):
    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
    subject = f"Earlier Test Available at {centre_name}!"
    body = f"A new test date was found: {date_found.strftime('%d %B %Y %I:%M %p')} at {centre_name}.\nVisit DVSA to reschedule it."
    yag.send(EMAIL_RECEIVER, subject, body)
    print(f"Email sent for {date_found} at {centre_name}")

def check_for_earlier_test():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless (no browser window)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.gov.uk/change-driving-test")
    
    driver.find_element(By.ID, "driving-licence-number").send_keys(LICENSE_NUMBER)
    driver.find_element(By.ID, "application-reference-number").send_keys(BOOKING_REFERENCE)
    driver.find_element(By.ID, "booking-login-button").click()
    time.sleep(3)

    try:
        driver.find_element(By.LINK_TEXT, "Change your test").click()
    except:
        pass
    time.sleep(2)

    for centre in TEST_CENTRES:
        try:
            driver.find_element(By.LINK_TEXT, "Change test centre").click()
            time.sleep(2)
            search_box = driver.find_element(By.ID, "test-centre-search")
            search_box.clear()
            search_box.send_keys(centre)
            driver.find_element(By.ID, "search-button").click()
            time.sleep(3)
            driver.find_element(By.XPATH, f"//*[contains(text(), '{centre}')]/ancestor::a").click()
            time.sleep(3)
            date_element = driver.find_element(By.CLASS_NAME, "BookingCalendar-day--bookable")
            available_date = datetime.strptime(date_element.text, "%A %d %B %Y at %I:%M%p")
            if CUTOFF_DATE >= available_date < CURRENT_TEST_DATE:
                send_email_notification(available_date, centre)
        except Exception as e:
            print(f"No date found at {centre} or error: {e}")

    driver.quit()

# Schedule the check every 15 minutes
schedule.every(15).minutes.do(check_for_earlier_test)

print("Bot started. Checking every 15 minutes...")
while True:
    schedule.run_pending()
    time.sleep(1)
