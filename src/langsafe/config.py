from pyngrok import ngrok
import os

PORT = 8000


def setup_ngrok():
    NGROK_AUTH_TOKEN = os.getenv("NGROK_API_KEY")
    if NGROK_AUTH_TOKEN:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        url = ngrok.connect(PORT, "http")
        print(f" * ngrok tunnel: {url}")
        return url.public_url
    else:
        print(" * Skipping ngrok, no NGROK_API_KEY set.")
        return ""
