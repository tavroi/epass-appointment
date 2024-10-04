from Utils.config import *

def create_login_logs(status, agent_name):
    """Log the login attempt."""
    log_entry = {
        "_id": unique_id(),
        "agent_name": agent_name,
        "status": status,
        "timestamp": current_timestamp()
    }
    db.login_logs.insert_one(log_entry)


def create_notify_logs(booking_id,name,mobile_no=None, email=None, notification_sent=None, is_verified=None,request=None,response=None, agent_name=None ):
    obj={
        '_id': unique_id(),
        'booking_id':booking_id,
        'name':  name,
        "mobile_no":mobile_no,
        "email": email,
        'notification_sent':notification_sent,
        "is_verified":is_verified,
        "request": request,
        "response": response,
        "created_at":current_timestamp(),
        "created_by": agent_name
    }

    db.logs.insert_one(obj)


def create_user_logs(booking_id,notification_link_sent=False, verification_done=False, main_checkin=False,machine_id=None, dome_checkin=False, dome_id='', agent_name='', request={}, response={},method_name=" ", stage=0 ):
    
    stage=db.event_stage.find_one({'method_name':method_name})
    if not stage:
        stage={}

    obj={
        '_id': unique_id(),
        'booking_id':booking_id,
        'notification_link_sent':notification_link_sent,
        'verification_done': verification_done,
        'main_checkin':main_checkin,
        'dome_checkin': dome_checkin,
        'dome_id': dome_id,
        'machine_id':machine_id,
        'stage':stage.get('stage_id'," "),
        'method_name':method_name,
        "request": request,
        "response": response,
        "created_at":current_timestamp(),
        "created_by": agent_name
    }

    db.user_journey_logs.insert_one(obj)