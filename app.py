import os
import sys
import json
from datetime import datetime
from wit import Wit

client = Wit(os.environ["WIT_TOKEN"])

import requests
from flask import Flask, request, send_from_directory

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    wit_response = client.message(message_text)
                    send_message(sender_id, "Juuuust a bit outside...",wit_response)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200




def send_message(recipient_id, message_text,wit_response):

    dprice_msg = """
    I once sat next to David Price on a flight from Toronto. 
    He got hammered on those little nips they give you, you know? 
    Booted in the little baggie. I've had better flights, I'll tell you that.
    David Price is probably going to get hammered in Yankee Stadium.
    You can expect that he'll only score about 0.78 points through 18 batters.
    """

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    intent = wit_response["entities"]["intent"][0]["value"]
    player = wit_response["entities"]["player"][0]["value"]

    urlMap = {
        "David Price": {
            "url": "https://www.facebook.com/FantasyColorGuy/videos/158181388231729/",
            "message": dprice_msg
        },
        "Jose Altuve": {
            "url": "https://www.facebook.com/FantasyColorGuy/videos/158180031565198/",
            "message": "I dunno, something about altuve..."
        },
        "Clayton Kershaw": {
            "url": "https://www.facebook.com/FantasyColorGuy/videos/158181204898414/",
            "message": "He is good you should play him or something like that"
        }
    }

    if urlMap[player]:

        url = urlMap[player]["url"]
        message = urlMap[player]["message"]

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        message = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message
            }
        })

        video = json.dumps(
            {
                "recipient":{
                    "id": recipient_id
                },
                "message":{
                    "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                            "media_type": "video",
                            "url": url
                            }
                        ]
                    }
                    }    
                }
            })

        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=video)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)
    
        r2 = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=message)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)
    else:
        message = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "I don't know that person :("
            }
        })


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
