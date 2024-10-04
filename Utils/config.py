import inspect
import logging
import os
import urllib
import traceback
import uuid
import json
import requests
import time
import regex as re
import pandas as pd
from io import BytesIO
import hashlib
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
    
    event_datetime = datetime.fromtimestamp(event_start_timestamp/1000.0)
    event_date = datetime.strftime(event_datetime, "%d-%b-%Y")
    event_time = datetime.strftime(event_datetime, "%H:%M")

    return(event_date,event_time)

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
