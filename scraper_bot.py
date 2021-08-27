###################################################################
# Importing required modules
import beepy as bp
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from random import randint
import telegram_send


###################################################################
# Defining functions

# Sends a telegram message signalling the start of the script
def telestart(notif=0):
    if notif==1:
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        final_text="The script has started at " + current_time
        telegram_send.send(messages=[final_text])

# Sends a telegram message signalling the end of the script
def telefinish(notif=0):
    if notif==1:
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        final_text="The script has stopped either due to manual override or error at " + current_time
        telegram_send.send(messages=[final_text])

# Sends a telegram message signalling that a possible listing may have been found
def telego(notif=0):
    if notif==1:
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        final_text="Possible listing. GO!!! Time of capture: " + current_time
        telegram_send.send(messages=[final_text])

# Defining the alarm function
def alarm():
    for x in range(5):
        bp.beep(1)

# The extract function outputs all the text from a URL
def extract(url):
    html=requests.get(url).text
    return(' '.join(BeautifulSoup(html, "html.parser").stripped_strings))

# The check function checks if any of the keys are present in the text
def check(keys, text, telegram_notif=0):
    for i in keys:
        if i.upper() in text.upper():
            # What to do if a key has been found
            alarm()
            telego(telegram_notif)
            return(True)
    return(False)    

# This constitutes one full execution
def execution(telegram_notif=0):
    # Extracting and printing the current time
    now=datetime.now()
    current_time=now.strftime("%H:%M:%S")
    print("The current time is ",current_time,"\n")
    
    # The url to be checked
    my_url="https://realestate.xyz.com/xyz-rentals"

    # The keys to be searched. Not case sensitive
    my_keys=["under commitment: no"]

    # The extracted string from the url
    my_text=extract(my_url)
    # Checking the extracted string
    check(my_keys,my_text,telegram_notif)
    
    # The time delay between every run
    # Sleeps for a random interval between 10-15 seconds
    time.sleep(randint(10,15))


###################################################################
# Starting script

# Set notif to be 1 for telegram notifications.
# ONLY set it to 1 if telegram has been configured on your computer
my_telegram_notif=0

# Telegram message indicating that the script has started
telestart(my_telegram_notif)
while True:
    try:
        # Executing on an infinite loop
        execution(my_telegram_notif)
    except:
        # What to do in case of error or manual override
        # First, a telegram message gets sent indicating an error or manual override
        telefinish(my_telegram_notif)
        # Second, gives out a sound to indicate an error or manual override
        bp.beep(2)
        break
    

