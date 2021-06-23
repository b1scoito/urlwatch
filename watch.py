import requests  # For HTTP requests
import datetime  # For timestamp
import dotenv  # For loading .env files.
import time  # For sleep
import sys  # For exiting
import os  # For getting environment variables

if not os.path.exists(".env"):
    print("Failed to find .env file, sure you created it?")
    sys.exit()

dotenv.load_dotenv()

# Array of URLs to watch
urls_to_watch = ["https://google.com", "https://github.com"]

# How much time to sleep
sleep_for = 5


def send_notification(token, id, msg) -> bool:
    res = requests.get(
        f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={msg}")

    return (res.status_code == 200)


def log(txt, notify=False) -> None:
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime(
        "%H:%M:%S")

    print(f"{timestamp}: {txt}")

    if notify:
        # Send Telegram push notification
        send_notification(
            os.environ['TELEGRAM_BOT_TOKEN'], os.environ['TELEGRAM_USER_ID'], txt)


def main() -> None:
    log(f"Waiting for an update... Retrying every {sleep_for} seconds.")

    while True:
        for url in urls_to_watch[:]:
            res = requests.get(url)

            if res.ok:
                log(f"[{res.status_code}]: {url} is online!", True)
                urls_to_watch.remove(url)

        time.sleep(sleep_for)


if __name__ == '__main__':
    main()
