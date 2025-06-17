import os
import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv(dotenv_path="Logdaten.env") #Abhängig wo Datei liegt

TARGET_URL = "https://db.jobs/service/search/de-de/5441588?qli=true&query=&queryJoined=&sort=pubExternalDate_tdt&itemsPerPage=20&pageNum=0&country=Deutschland"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " #UserAgent um Nicht als Bot von Website erkannt zu werden
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS"))

last_job_count = None

# Funktionen

def send_email(subject, message):
    try:
        email = MIMEText(message)
        email["Subject"] = subject
        email["From"] = EMAIL_SENDER
        email["To"] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(email)
        print(f"[EMAIL] Gesendet: {subject}")
    except Exception as e:
        print(f"[ERROR] Email fehlgeschlagen: {e}")

def send_pushover_notification(title, message):
    try:
        data = {
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=data)
        if response.status_code == 200:
            print("[PUSHOVER] Nachricht gesendet.")
        else:
            print(f"[PUSHOVER ERROR] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Pushover fehlgeschlagen: {e}")

def get_job_count(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        span = soup.find("span", class_="result-count")
        if span and span.has_attr("data-count"):
            raw_count = span["data-count"].replace(".", "").replace(",", "")
            return int(raw_count)
        else:
            print("[ERROR] <span class='result-count'> nicht gefunden oder missing data-count.")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] While scraping: {e}")
        return None

# main

def main():
    global last_job_count
    print(f"[START] Tracking DB Systel listings on {TARGET_URL}")

    while True:
        current_count = get_job_count(TARGET_URL)

        if current_count is not None:
            if last_job_count is None:
                print(f"[JobAgent] Hat {current_count} Stellenanzeigen gefunden.")
                last_job_count = current_count
            elif current_count != last_job_count:
                change = "zugenommen" if current_count > last_job_count else "abgenommen"
                print(f"[CHANGE] Anzahl hat {change}: {last_job_count} → {current_count}")

                subject = "DB Jobs: Anzahl hat sich geändert!"
                message = f"Die Anzahl der Stellenangebote hat {change} von {last_job_count} auf {current_count}."

                send_email(subject, message)
                send_pushover_notification(subject, message)

                last_job_count = current_count
            else:
                print(f"[NO CHANGE] Immer noch {current_count} Stellenanzeigen.")
        else:
            print("[ERROR] Konnte Anzahl nicht erfassen.")

        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
