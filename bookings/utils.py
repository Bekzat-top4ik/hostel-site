import requests
from django.conf import settings


def send_telegram_message(text: str):
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")

    print("TOKEN EXISTS:", bool(token))
    print("CHAT ID:", chat_id)

    if not token:
        print("TELEGRAM_BOT_TOKEN not found")
        return

    if not chat_id:
        print("TELEGRAM_CHAT_ID not found")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        print("Telegram status:", response.status_code)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram error:", str(e))