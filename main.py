import bs4 as bs
import smtplib
import ssl
import time
import urllib.request
import pandas as pd
import tkinter as tk
from tkinter import simpledialog
import urllib.parse as urlparse
from urllib.parse import parse_qs
ROOT = tk.Tk()
ROOT.withdraw()
pw = simpledialog.askstring(
    title="License Key", prompt="Enter License Key:")
time_to_sleep_between_searches = 30
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "tamriel.trade.bot@gmail.com"
receiver_email = simpledialog.askstring(
    title="Notification E-Mail", prompt="Enter the e-mail address you would like notifications sent to:")
password = pw
message = """\
blank message."""

# the input dialog
urls = []

while True:
    URL_INPUT = simpledialog.askstring(
        title="Enter URL", prompt="Enter URL from us.tamrieltradecentre.com (press 'ok' to finish):")
    if URL_INPUT == "":
        break
    elif URL_INPUT is None:
        break
    urls.append(str(URL_INPUT))

try:
    while True:
        for url in urls:
            dfs = pd.read_html(url)
            # print(len(dfs))
            # If dfs >= 1 continue
            if (len(dfs)) > 1:
                # More than 1 table on website means we got data!
                getItemFromUrl = urlparse.urlparse(url)
                itemname = parse_qs(getItemFromUrl.query)['ItemNamePattern']
                print("Item Found: " + str(itemname))
                item = dfs[1][['Item', 'Location', 'Price']]
                # send email
                message = 'Subject: We found an Item! \n\nTamriel-Trade-Bot\n\nSearch URL: {searchurl}\n\n\n{items}\n\nYou will no longer get e-mails about this item unless you restart the application'.format(
                    items=item, emailurl=url)
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
                print("E-Mail sent for {item}.".format(item=str(itemname)))
                # remove URL
                print("Removing item from search.")
                urls.remove(url)
                print("Waiting {time} seconds until next search".format(
                    time=time_to_sleep_between_searches))
                time.sleep(time_to_sleep_between_searches)
            elif (len(dfs)) <= 1:
                getItemFromUrl = urlparse.urlparse(url)
                itemname = parse_qs(getItemFromUrl.query)['ItemNamePattern']
                print("No deals found for {item}".format(item=str(itemname)))
                # less than 1 table on website means we have NO DATA
                # print("less than or equal to 1")
                # wait before searching next item.
                print("Waiting {time} seconds until next search".format(
                    time=time_to_sleep_between_searches))
                time.sleep(time_to_sleep_between_searches)
except KeyboardInterrupt:
    pass
