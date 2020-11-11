import requests
import os
import smtplib
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup


URL = "https://www.amazon.de/-/en/Apple-MacBook-16GB-512GB-memory/dp/B081FW6TPQ?pd_rd_w=p4mOY&pf_rd_p=26a69915-0c81-42f1-9f66-a70330ba3e45&pf_rd_r=GWE50XWXV2EKQCRGNW46&pd_rd_r=a738284b-259e-4dfa-af29-5ef9a43895c8&pd_rd_wg=aWVMO"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

load_dotenv()


def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text()
    p = soup.find(id="priceblock_ourprice").get_text()
    price = p[1:-3]
    converted_price = float(price.replace(",", ""))

    if converted_price < 2300:
        send_mail()

    print(converted_price)
    print(title.strip())

    if converted_price < 2300:
        send_mail()


def send_mail():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    subject = "Amazon item Price reduction"
    body = "Check the Amazon Link: https://www.amazon.de/-/en/Apple-MacBook-16GB-512GB-memory/dp/B081FW6TPQ?pd_rd_w=p4mOY&pf_rd_p=26a69915-0c81-42f1-9f66-a70330ba3e45&pf_rd_r=GWE50XWXV2EKQCRGNW46&pd_rd_r=a738284b-259e-4dfa-af29-5ef9a43895c8&pd_rd_wg=aWVMO"
    msg = f"Subject: {subject}\n\n{body} "

    server.sendmail(EMAIL_USERNAME, "luke.mjn@gmail.com", msg)

    print("Hey, email has been sent")

    server.quit()


check_price()

while True:
    check_price()
    # pauses execution and runs every hour
    time.sleep(60 * 60)
