import os
import time
import schedule
import yagmail

def check_for_earlier_test():
    yag = yagmail.SMTP(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
    yag.send(os.getenv("EMAIL_RECEIVER"), "Driving Test Bot", "This is a test notification from the cloud!")

schedule.every(5).minutes.do(check_for_earlier_test)

while True:
    schedule.run_pending()
    time.sleep(1)
