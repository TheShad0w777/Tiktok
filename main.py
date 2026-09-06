from flask import Flask, request
import requests

app = Flask(__name__)

WA_TOKEN = "BURAYA_WA_TOKEN"
PHONE_ID = "BURAYA_PHONE_ID"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == "mytoken123":
        return request.args.get("hub.challenge")
    return "Error", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = msg["text"]["body"]
        phone = msg["from"]
        
        if "tiktok.com" not in text:
            return "ok"
        
        send_message(phone, "⏳ Yüklənir...")
        
        r = requests.get(f"https://www.tikwm.com/api/?url={text}")
        video_url = r.json()["data"]["play"]
        
        send_video(phone, video_url)
    except:
        pass
    return "ok"

def send_message(phone, text):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages",
        headers={"Authorization": f"Bearer {WA_TOKEN}"},
        json={"messaging_product": "whatsapp", "to": phone,
              "type": "text", "text": {"body": text}}
    )

def send_video(phone, url):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages",
        headers={"Authorization": f"Bearer {WA_TOKEN}"},
        json={"messaging_product": "whatsapp", "to": phone,
              "type": "video", "video": {"link": url}}
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
