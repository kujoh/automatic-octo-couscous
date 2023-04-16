import os
import json
import requests
import random
from flask import Flask, request

token = os.getenv("Token")
bot_id = os.getenv("BotID")  # os.getenv("TEST_BOT_ID")
app = Flask(__name__)

url = "https://api.groupme.com/v3/bots/post"
img_url = "https://image.groupme.com"


@app.route("/", methods=["GET"])
def home():
    return "https://automaticoctocouscous.onrender.com"


@app.route("/", methods=["POST"])
def receive():
    mat_names = ["mat", "matt", "matthew"]
    rand_num = random.randint(-100, 100)
    bas_rand = random.randint(0, 1000)

    data = request.get_json()
    print("Incoming Msg: ")
    print(data)

    # Prevent self-reply
    if data["sender_type"] != "bot":
        if data["text"].startswith("/ping"):
            send(data["name"] + " pinged me!")
        if data["name"] == "Basith Penna-Hakkim" and bas_rand <= 5:
            send(
                "oh my dear basith\nmy heart yearns for your friendship\nlet’s be friends basith")
            post_img_to_groupme("./bas.jpg")
        if "ok" in data["text"].lower():
            post_img_to_groupme("./ok.jpg")
        if "ayo" in data["text"].lower():
            send(
                "sup")

        # check if mat, matt, or matthew exists in string (case insensitive)
        # RNG send different pictures
        if any(x in data["text"].lower() for x in mat_names):
            if rand_num >= 50:
                post_img_to_groupme("./mat.jpeg")
            elif rand_num >= 0:
                post_img_to_groupme("./bucket.jpg")
            elif rand_num < 0:
                post_img_to_groupme("./baby_bucket.jpg")

    return "ok", 200


def send(msg):
    json = {
        "bot_id": bot_id,
        "text": msg
    }
    req = requests.post(url, json=json)
    print("send complete: ", req)


def post_img_to_groupme(img):
    image = open(img, "rb").read()
    req = requests.post(
        url='https://image.groupme.com/pictures',
        data=image,
        headers={
            'Content-Type': 'image/jpeg',
            'X-Access-Token': token
        }
    )

    d = json.loads(req.text)
    picture_url = d["payload"]["picture_url"]

    send_json = {
        "bot_id": bot_id,
        "attachments": [
            {
                "type": "image",
                "url": picture_url
            }
        ]
    }

    r = requests.post(url=url, json=send_json)
    print("post_img_to_groupme complete: ", r)
