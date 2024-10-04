from dotenv import load_dotenv
from Utils.config import *
import requests
    

load_dotenv('.env')

def send_otp(mobile_no,otp_length=4):

    auth_key="218456A48acSW4Fmb609a6f8fP1"

    url = f"""https://api.msg91.com/api/v5/otp?authkey={auth_key}&template_id=60f525dfc4fb7847c70a3987&mobile={mobile_no}&otp_length={otp_length}"""
    print(url)

    payload = {}
    headers = {
      'Cookie': 'PHPSESSID=ipufr2ach87u62l0f6jmjljhs1'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


    logger.info(response.status_code)
    logger.info(response.text)
    if response.status_code == 200:
        return True
    else:
        return False
    

def verify_otp(mobile_no,otp):

    
    auth_key="218456A48acSW4Fmb609a6f8fP1"

    url = f"""https://api.msg91.com/api/v5/otp/verify?mobile={mobile_no}&otp={otp}&authkey={auth_key}"""

    payload = {}
    headers = {
      'Cookie': 'PHPSESSID=ipufr2ach87u62l0f6jmjljhs1'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    logger.info(response.status_code)
    logger.info(response.text)
    response_obj= response.json()
    if response.status_code == 200 and response_obj.get('type','')=="error":
        return False, response_obj.get('message','')
    else:
        return True, "OTP verified successfully"
  



