import base64
import re
import mimetypes
import time

import requests
from pytz import timezone
from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger('django')


def remove_space(email):
    return "".join(email.split())


def validate_email(email):
    """Validating email"""
    if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
        return True
    else:
        return False


def validate_name(name):
    """Validating name"""
    if name.replace(" ", "").isalpha():
        return True
    else:
        return False


def validate_phone(phone):
    """Validating phone number"""
    if len(phone) < 12 or len(phone) > 12:
        return False
    else:
        return True


def valid_time_diff(start_date, end_date):
    """Validating time difference."""
    if end_date > start_date:
        return True
    else:
        return False


def strip_string(data):
    return data.strip()


def extra_keys_for_filter(request, key_name):
    """
        Extra key for filtering data.
    """
    search = request.GET.get('search[value]')
    draw = int(request.GET.get('draw')) if request.GET.get('draw') else 0
    try:
        page = int(request.GET.get('start')) if request.GET.get('start') else 0
        limit = int(request.GET.get('length')) if request.GET.get('length') else -1
    except ValueError:
        page = 0
        limit = -1
    try:
        order_num = int(request.GET.get("order[0][column]"))
    except:
        order_num = None
    if not order_num:
        order_column_name = key_name
        order_type = -1
    else:
        order_column_name = request.GET.get("columns[{}][data]".format(order_num))
        order_type = 1 if request.GET.get("order[0][dir]") == 'asc' else -1
    return {"search": search, "page": page, "limit": limit, "order_name": order_column_name, "order_type": order_type,
            "draw": draw}


def convert_into_basic(data):
    basic_data = data
    message_bytes = basic_data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def encode_base64(agent_id, business_id):
    data = agent_id + " " + business_id
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode_base64(data):
    base64_bytes = data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message.split(" ")


def validate_date(data, format):
    try:
        date_data = datetime.strptime(data, format)
        timestamp_data = time.mktime(date_data.timetuple())
        return {"status": True, "data": timestamp_data}
    except:
        logger.error(f'Message: Please provide datetime in given format: {format} data: {data} method: validate_data')
        return {"status": False, "message": "Please provide datetime in this " + format + " format"}


def convert_timestamp_datetime(data, format):
    try:
        data = datetime.fromtimestamp(data).strftime(format)
        return data
    except Exception as e:
        return {"message": e.__str__(), "status": False}


def calculate_percentage_amount(data, discount):
    return (data / 100) * discount


# def month_last_and_first_date(date):
#     last_date = date + relativedelta(day=1, months=+1, days=-1)
#     first_day = date + relativedelta(day=1)
#     return {"first_date": first_day, "last_date": last_date}


def week_monday_and_sunday_date(date):
    start = date - timedelta(days=date.weekday())  # monday date
    end = start + timedelta(days=6)  # sunday date
    return {"start": start, "end": end}


def convert_time(time_obj):
    return datetime.strptime(time_obj, '%I:%M %p')


def convert_time_in_24_hour(time_obj):
    return datetime.strptime(time_obj, '%I:%M %p').strftime('%H:%M')


def split_sender_id(sender_id):
    if '*_*' in sender_id:
        return sender_id.split('*_*')[1]
    else:
        return sender_id


def convert_datetime_to_timezone(datetime_obj, timezone_obj):
    """
    Return datetime after conversion
    :param datetime_obj: Datetime data
    :param timezone: timezone
    :return:
    """
    tzinfo = timezone(timezone_obj)
    time_obj = datetime_obj.astimezone(tzinfo)
    return time_obj


def validate_payload(payload, data):
    message_list = []
    for key, value in data.items():
        if key not in payload or payload[key] in ["", None] or type(payload[key]) != value:
            message_list.append({
                "message": key + " is a compulsory field and it must not be empty.",
                "error": key + " is a compulsory field and it must not be empty.",
            })
    return message_list


def get_url_info(url):
    try:
        response = requests.get(url)
        media_extenstion = mimetypes.guess_type(url, strict=True)[0]
        return {"media": response, "media_extenstion": media_extenstion,
                "media_type": media_extenstion.split('/')[0],
                "status": True}
    except Exception as e:
        return {"message": e.__str__(), "status": False}
