import requests
import json
from Utils.config import *
VENUE_DETAILS={
    'venue':"venue",
    'location':"location",
    'timing':'timing'
}

def send_message_on_completion(data):
    logger.info("==========================send messge with qr==========================",)
    qr_link=data.get("link",'')
    mobile_no= data.get("mobile_number")
    name= data.get("name")
    signature= data.get("signature", "Team Digipass")


    url = "https://dev.api.dolphinchat.ai/v2/messaging/whatsapp/a2d75083a653441c8541c4de8c0e3088"

    payload = json.dumps({
    "to": mobile_no,
    "type_of_message": "template",
    "template_id": "900587925254084",
    "payload": {
        "body": [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": name
                    },{
                        "type": "text",
                        "text": signature
                    }
                ]                
            },
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {
                            "link": qr_link
                        }
                    }
                ]
            }
        ]
    }
})
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer c167a76eddda4be489f0fe373eb75bb5'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    logger.info("send_message_with_qr RESPONSE: %s", response.json())
    return response.json()


def send_notification_message(data):

    booking_id=data.get("booking_id")
    event_id=data.get("event_id")
    mobile_no= data.get("mobile_number")
    name= data.get("name")

    link =f"booking-verification?booking_id={booking_id}&event_id={event_id}"
    logger.info(f"SEND NOTIFICATION MESSAGE- Booking ID: {data}, LINK: {link} mobile_no:{mobile_no}, name: {name}, event_id: {event_id}")

    url = "https://dev.api.dolphinchat.ai/v2/messaging/whatsapp/a2d75083a653441c8541c4de8c0e3088"

    payload = json.dumps({
    "to": mobile_no,
    "type_of_message": "template",
    "template_id": "1204444080760774",
    "payload": {
        "body": [
        {
            "type": "body",
            "parameters": [
            {
                "type": "text",
                "text": name
            }
            ]
        },
        {
            "type": "button",
            "sub_type": "url",
            "index": "0",
            "parameters": [
            {
                "type": "text",
                "text": link
            }]
        }]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer c167a76eddda4be489f0fe373eb75bb5'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    logger.info("send_notification_message STATUS CODE: %s", response.status_code)
    if response.status_code==200:
        logger.info("send_notification_message RESPONSE: %s", response.json())
        return response.json()
    return {}


# data={
#     'name':"pooja",
#     'qr_link':"https://dc-chat-media.s3.ap-south-1.amazonaws.com/JBNMKNGP009981718353579.741477.png",
#     'venue':"venue",
#     'location':"location",
#     'timing':'timing'
# }

# print(send_message_with_qr(data))