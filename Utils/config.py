import inspect
import logging
import os
import urllib
import traceback
import uuid
import json
import requests
import time
from datetime import time
import regex as re
import pandas as pd
from io import BytesIO
import hashlib
import pytz
from threading import Thread
# import cv2
# from pyzbar.pyzbar import decode
# import qrcode
# import boto3
# import base64
# from PIL import Image
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# import numpy as np

from datetime import datetime, timedelta

from fastapi import FastAPI, APIRouter, Request, File, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel 
from starlette.responses import JSONResponse, Response
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from Utils.status_codes import *
from Utils.return_message import *
from Utils.database import *
import threading
from fastapi import FastAPI, Request,Header
from fastapi import Depends
from pymongo.errors import DuplicateKeyError
from Utils.token_bucket import TokenBucket
from starlette.middleware.base import BaseHTTPMiddleware

from typing import Text, Dict, Optional
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from dotenv import load_dotenv
from Utils.code import *

load_dotenv(".env")



app = FastAPI()

# class RateLimiterMiddleware(BaseHTTPMiddleware):
#     def __init__(self,app,bucket: TokenBucket):
#         super().__init__(app)
#         self.bucket =bucket

#     async def dispatch(self,request:Request,call_next):
#         if self.bucket.take_token():
#             return await call_next(request)
        
#         return Response("Rate limit exceeded", status_code=HTTP_429_TOO_MANY_REQUESTS)

# bucket = TokenBucket(capacity=29,refill_rate=3)

# app.add_middleware(RateLimiterMiddleware,bucket=bucket)

origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
VERSION = "v1"

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

IS_LOCAL = True
BASE_ENDPOINT = f"/{VERSION}/appointment"
MONGODB_CON_STR = os.getenv("MONGODB_CON_STR")
DB_NAME = os.getenv("MONGODB_DB")
DB_NAME_DOLPHIN_CHAT=os.getenv("MONGODB_DB_DOLPHIN_CHAT")
DASHBOARD_URL= "https://digipass.verismart.ai"
RP_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RP_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
WHATSAPP_BASE_URL = "https://media.smsgupshup.com/GatewayAPI/rest"
USERID = "2000194912"
PASSWORD = "8%23Ag6766"
# Dolphinchat Creds
ACCESS_TOKEN='c167a76eddda4be489f0fe373eb75bb5'
AGENT_ID="a2d75083a653441c8541c4de8c0e3088"
DC_BASE_URL = "https://dev.api.dolphinchat.ai"
DC_API_VERSION = "v2"
JWT_ALGORITHM = 'HS256'
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_DAYS = 3
DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
EMPTY_LIST = ["", " ", None, "null"]

db_obj = Dbconnect(db_name=DB_NAME, db_url=MONGODB_CON_STR)
db_obj_dolphinchat=Dbconnect(db_name=DB_NAME_DOLPHIN_CHAT,db_url=MONGODB_CON_STR)

db = db_obj.db
if os.getenv("is_local"):
    IS_LOCAL = False

db_dolphinchat = db_obj_dolphinchat.db
if os.getenv("is_local"):
   IS_LOCAL = False


def unique_id():
    return uuid.uuid4().hex


def current_timestamp():
    return datetime.now().timestamp()

def get_request_data(request):
    return request.method, request.url.path, request.client.host

def sha256_encode(value):
    return hashlib.sha256(value.encode()).hexdigest()

def error_handler(data_type=None):
    if data_type is None:
        data_type = {}

    def decorator_function(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                exception = e.__str__()
                logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                             f"Method-Name: {inspect.stack()[0][3]}")
                logger.info(20 * "....")
                return {"code": EXCEPTION_CODE, "data": data_type,
                        "message": EXCEPTION_MESSAGE,
                        "errorMessage": exception,
                        "status": False}

        return wrapper

    return decorator_function   

def create_logs(input_data, response, file_name, ip, method_name, method, module_name, request_path, member_id=None,
                logs_type='access'):
    # control_obj = get_control_detail()
    request_data = {}
    # if not control_obj or control_obj.get('is_logs_allowed', False):
    request_data = {
        "_id": unique_id(),
        "active_member_id": member_id,
        "request": input_data,
        "response": response,
        "created_at": current_timestamp(),
        "file_name": file_name,
        "ip": ip,
        "api_name": method_name,
        "module_name": module_name,
        "method": method,
        "request_path": request_path,
        "logs_type": logs_type
    }
    db.logs.insert_one(request_data)
    return request_data


def place_return_value_return_payload(traceID="", errorMessage="", displayMessage="", status=False, data={}, code=""):
    return {
        "data": data,
        "status": status,
        "code": code,
        "message": {
            "displayMessage": displayMessage,
            "errorMessage": errorMessage,
            "traceID": traceID
        }
    }


def return_process(data, response, method, path, ip, member_id, method_name, file_name, module_name, code):
    # Create logs
    logs_obj = create_logs(input_data=data, response=response, file_name=file_name, ip=ip,
                           method_name=method_name, method=method, request_path=path, member_id=member_id,
                           logs_type="access" if not response.get("is_exception", False) else "error",
                           module_name=module_name)
    print(method_name)
    # Return Message
    return_response = place_return_value_return_payload(
        displayMessage=response['message'], errorMessage=response['errorMessage'] if not response['status'] else "",
        status= response.get("status", False), traceID=logs_obj['_id'], code=code,
        data=response['data'] if 'data' in response else {})
    return return_response


def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')

        return True
    except ValueError:
        return False

def validate_boolean_field(field_name, field_value):
    """
    Validate that a field value is a boolean.
    """
    if field_value is not None and not isinstance(field_value, bool):
        error_message = f"{field_name} must be a boolean."
        logger.error(f"{field_name} is not a boolean: {field_value}")
        return {"status": False, "data": {}, "message": error_message, "errorMessage": error_message, "code": READ_CODE}
    return {"status": True}

def date_to_epoch(date_str):
    """
    Convert a date string in 'YYYY-MM-DD' format to an epoch timestamp.

    Parameters:
    date_str (str): The date string in 'YYYY-MM-DD' format.

    Returns:
    int: The corresponding epoch timestamp.
    """
    try:
        # Parse the date string into a datetime object
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        # Convert the datetime object to a Unix epoch timestamp
        epoch = int(time.mktime(dt.timetuple()))
        return epoch
    except ValueError:
        # Handle the case where the date string is invalid
        print(f"Invalid date format: {date_str}. Please use 'YYYY-MM-DD'.")
        return None
    
def convert_datetime(event_start_timestamp):
   
    timezone = pytz.timezone('Asia/Kolkata')  

    event_datetime = datetime.fromtimestamp(event_start_timestamp, tz=pytz.utc)

    event_datetime = event_datetime.astimezone(timezone)
    
    event_date = event_datetime.strftime("%d-%b-%Y")
    event_time = event_datetime.strftime("%H:%M")

    return event_date

def get_slot_times(slot_ids):
    slots = list(db.slots.aggregate([
        {
            '$match': {
                'slot_id': {'$in': slot_ids}
            }
        },
        {
            '$project': {
                'startTime': {'$arrayElemAt': [{'$split': ['$slot_time', ' - ']}, 0]},
                'endTime': {'$arrayElemAt': [{'$split': ['$slot_time', ' - ']}, 1]}
            }
        }
    ]))
    times = []
    for slot in slots:
        start_time = datetime.strptime(slot['startTime'], '%H:%M')
        end_time = datetime.strptime(slot['endTime'], '%H:%M')
        times.append((start_time, end_time))
    if times:
            min_time = min(t[0] for t in times)
            max_time = max(t[1] for t in times)
            return f"{min_time.strftime('%H:%M')} - {max_time.strftime('%H:%M')}"
    else:
        return None, None

def is_valid_email(email):
    if pd.isna(email):
        return False
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(email_regex, email) is not None

def is_valid_mobile(mobile):
    if pd.isna(mobile):
        return False
    try:
        mobile_str = str(int(mobile))  
    except ValueError:
        return False
    return len(mobile_str) == 10

def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return time(hour=hours, minute=minutes)


def call_api(method, url, headers=None, payload=None):
    if not headers:
        headers = {'Content-Type': 'application/json'}
    payload = {} if not payload else payload
    response = requests.request(method=method, url=url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_data = response.json()
        # response_data["status_code"]
    else:
        response_data = response.text
    return response_data

def fetch_template_details(template_id):
    """Fetch template details from DolphinChat API."""
    url = f"{DC_BASE_URL}/{DC_API_VERSION}/admin/wa/template/{AGENT_ID}?template_id={template_id}"
    headers = {
        'Authorization': 'Bearer c167a76eddda4be489f0fe373eb75bb5',
        'Content-Type': 'application/json'
    }
    return call_api("GET", url, headers=headers)

def fetch_payload(template_id):
    api_response = fetch_template_details(template_id)

    api_status = True if isinstance(api_response, dict) and api_response.get("status") else False
    if not api_status:
            return {
                "code": INVALID_CODE,
                "status": True,
                "message": "Unable to fetch template details",
                "errorMessage": ""
            }
        
    is_header_image = api_response.get("data", {}).get("template_header", {}).get("type") == "image"
    variable_count = api_response.get("data", {}).get("template_body", {}).get("count_of_variable", 0)
    buttons_count = api_response.get("data", {}).get("template_buttons", {}).get("count_of_variable", 0)
    

    return {
        "is_header_image":is_header_image,
        "variable_count":variable_count,
        "buttons_count":buttons_count
    }


def generate_payload(name,officer_id,appointment_date,appointment_time,template_id,button_url:Optional[str]=""):

    template_obj = db.event_template.find_one({"template_id": template_id})
    officer_obj = db.officials.find_one({"officer_id":int(officer_id)})
    officer_name = officer_obj.get("name"," ")
    is_header_image = template_obj.get("is_header_image",False)
    print("image:",is_header_image)
    print("button_url:",button_url)

    variable_count = template_obj.get("template_body").get("count_of_variable")
    variables = template_obj.get("template_body").get("body")
    print(variables,"variables")

    buttons_count = template_obj.get("template_buttons").get("count_of_buttons")
    buttons = template_obj.get("template_buttons").get("buttons")
    banner_image = "https://dolphinchat-chat.s3.ap-south-1.amazonaws.com/mpsedc/digipass/events1723553117931_1723553119631_Zqd9yx5LeNNTxj_L_SQUARECLEAN.png"
    if buttons_count and buttons_count >0:
        url_types = [item['url_type'] for item in buttons if 'url_type' in item]
    
    send_payload = {"body": []}

    if is_header_image:
        send_payload["body"].append({
            "type": "header",
            "parameters": [
                {
                    "type": "image",
                    "image": {
                        "link": banner_image
                    }
                }
            ]
        })

    if variable_count >0:
        parameters = []
        for i in variables:
            param = {"type": "text", "text": ""}
            if i == "user":
                param["text"] = name
            elif i == "officer":
                param["text"] = officer_name
            elif i == "date":
                param["text"] = appointment_date
            elif i == "time":
                param["text"] = appointment_time

            parameters.append(param)

        send_payload["body"].append({
            "type": "body",
            "parameters": parameters
        })

    if buttons_count and buttons_count >0:
        if buttons_count == 1:
            if url_types and url_types[0] == "dynamic":
                param = {
                "type": 'button',
                "sub_type": "url",
                "index": "0",  
                "parameters": [
                    {
                        "type": "text",
                        "text": button_url
                    }
                ]
            }
                send_payload["body"].append(param)

        else:  
            for index in range(buttons_count):
                if index < len(url_types):
                    if url_types[index] == "dynamic":
                        param = {
                            "type": 'button',
                            "sub_type": "url",
                            "index": str(index),  
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": button_url  
                                }
                            ]
                        }
                    elif url_types[index] == "static":
                        param = {
                            "type": 'button',
                            "sub_type": "url",
                            "index": str(index),
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": " "
                                }
                            ]
                        }
                    send_payload["body"].append(param)


    print("Generated Payload:", send_payload)  
    return send_payload

def send_whatsapp_message( template_id, mobile_no,officer_id,appointment_date,appointment_time,type_id,name,campaing_type,campaing_id:Optional[str]="",button_url:Optional[str]=""):
    """Send WhatsApp message via DolphinChat API."""
    payload_data = generate_payload(name,officer_id,appointment_date,appointment_time,template_id,button_url)
    url = f"{DC_BASE_URL}/{DC_API_VERSION}/messaging/whatsapp/{AGENT_ID}"
    headers = {
        'Authorization': 'Bearer c167a76eddda4be489f0fe373eb75bb5',
        'Content-Type': 'application/json'
    }
    payload = {
        "to": mobile_no,
        "type_of_message": "template",
        "template_id": template_id,
        "payload": payload_data
    }
    response = call_api("POST", url, headers=headers, payload=payload)
    response_status = True if isinstance(response, dict) and response.get("status") else False
    wa_invites_id =unique_id()
    event_id = "appointment_id"
    db.broadcast_list.insert_one(
                        {"_id": wa_invites_id,
                         "name":name,
                         "email": "",
                         "mobile": mobile_no,
                         "created_at": current_timestamp(),
                         "message_status": True if response_status else False,
                         "response": response,
                         "message_payload":payload_data,
                         "message_type": type_id,
                         "campaing_type": campaing_type,
                         "channel":"whatsapp",
                         "campaing_id":campaing_id,
                         "event_id":event_id
                        }
                    )
    db.wa_message_status.insert_one(
        {"_id":unique_id(),
         "created_at":current_timestamp(),
         "delivery_status":"Initiated",
         "mobile":mobile_no,
         "event_id":event_id,
         "campaing_id":campaing_id,
         "message_id":response.get("data", {}).get("mid")})
    
    print(response)
    return response


def format_invite_mail(body, name, official_obj, appointment_date, appointment_time):
    return body.format(
        guest_name=name,
        officer_name=official_obj.get("name", "").title(),
        appointment_date=appointment_date,
        appointment_time=appointment_time
    )
