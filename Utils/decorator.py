import inspect
from typing import Optional

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from Utils.config import (
    os,
    db,
    Request,
    JWT_ALGORITHM,
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_DAYS,
    UNAUTHORIZE_ACCESS_CODE,
    get_request_data, logger, current_timestamp
)


SECRET_KEY = SECRET_KEY
ALGORITHM = JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = ACCESS_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_access_token_detail(access_token):
    return db.member_login_history.find_one({"access_token": access_token, "is_active": True})

def get_lead(sender_id: str):
    lead_obj = db.users.find_one({"sender_id": sender_id})
    return lead_obj

def authenticate_lead(sender_id: str):
    lead = get_lead(sender_id)
    if not lead:
        return False
    return lead

def get_label(label_id: str):
    label_obj = db.labels.find_one({"_id": label_id})
    return label_obj

def authenticate_label(label_id: str):
    label = get_label(label_id)
    if not label:
        return False
    return label

def get_member(memeber_id: str):
    member_obj = db.members.find_one({"_id": memeber_id, "is_active": 1, "is_deleted": False})
    return member_obj


def authenticate_user(memeber_id: str):
    user = get_member(memeber_id)
    if not user:
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token(member_id, expiry_day=ACCESS_TOKEN_EXPIRE_DAYS):
    access_token_expires = timedelta(days=expiry_day)
    access_token = create_access_token(
        data={"sub": member_id}, expires_delta=access_token_expires
    )
    return access_token


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    detail = {
        "data": {},
        "status": False,
        "code": UNAUTHORIZE_ACCESS_CODE,
        "message": {
            "displayMessage": "Could not validate credentials",
            "errorMessage": "Un-Authorize User",
            "traceID": ""
        }
    }
    method, path, ip = get_request_data(request)
    print(method)
    try:
        agent_obj = db.agents.find_one({"access_token": token})
        if agent_obj:
            return agent_obj
        member_obj = db.member_access_token.find_one({"access_token_id": token, "is_active": True})
        if member_obj:
            user = get_member(memeber_id=member_obj['member_id'])
            return user
        access_token = get_access_token_detail(token)
        if not access_token:
            pass
            # logs_obj = create_logs(input_data={"access_token": token}, response=detail,
            #                        file_name=os.path.basename(__file__), ip=ip, method_name=inspect.stack()[0][3],
            #                        method=method, request_path=path, member_id=token, logs_type="access",
            #                        module_name="Authorize")
            # detail['message']['traceID'] = logs_obj['_id']
            # logger.error(f"Authorization error: {detail}, token: {token}, File-Name: {os.path.basename(__file__)}, "
            #              f"Method-Name: {inspect.stack()[0][3]}, IP: {ip}, API-Path: {path}")
            # logger.info(20*"^^^^^")
            # raise HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED,
            #         detail=detail,
            #         headers={"WWW-Authenticate": "Bearer"},
            #     )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        memeber_id: str = payload.get("sub")
        
        if memeber_id is None:
            pass
            logs_obj = create_logs(input_data={"access_token": token}, response=detail,
                                   file_name=os.path.basename(__file__), ip=ip, method_name=inspect.stack()[0][3],
                                   method=method, request_path=path, member_id=token, logs_type="access",
                                   module_name="Authorize")
            detail['message']['traceID'] = logs_obj['_id']
            logger.error(f"Authorization error: {detail}, token: {token}, File-Name: {os.path.basename(__file__)}, "
                         f"Method-Name: {inspect.stack()[0][3]}, IP: {ip}, API-Path: {path}")
            logger.info(20 * "^^^^^")
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=detail,
                    headers={"WWW-Authenticate": "Bearer"},
                )
    except JWTError as e:
        pass
        # logs_obj = create_logs(input_data={"access_token": token}, response=detail,
        #                        file_name=os.path.basename(__file__), ip=ip, method_name=inspect.stack()[0][3],
        #                        method=method, request_path=path, member_id=token, logs_type="access",
        #                        module_name="Authorize")
        # detail['message']['traceID'] = logs_obj['_id']
        # detail['message']['errorMessage'] = e.__str__()
        # db.member_login_history.update_one({"access_token": token}, {"$set": {"is_active": False,
        #                                                                       "logout_timestamp": current_timestamp()}})
        # logger.error(f"Authorization error: {detail}, token: {token}, File-Name: {os.path.basename(__file__)}, "
        #              f"Method-Name: {inspect.stack()[0][3]}, IP: {ip}, API-Path: {path}")
        # logger.info(20 * "^^^^^")
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=detail,
                    headers={"WWW-Authenticate": "Bearer"},
                )
    user = get_member(memeber_id=memeber_id)
    if user is None:
        pass
        # logs_obj = create_logs(input_data={"access_token": token}, response=detail,
        #                        file_name=os.path.basename(__file__), ip=ip, method_name=inspect.stack()[0][3],
        #                        method=method, request_path=path, member_id=access_token, logs_type="access",
        #                        module_name="Authorize")
        # detail['message']['traceID'] = logs_obj['_id']
        # detail['message']['errorMessage'] = "User is not found or may not active"
        # logger.error(f"Authorization error: {detail}, token: {token}, File-Name: {os.path.basename(__file__)}, "
        #              f"Method-Name: {inspect.stack()[0][3]}, IP: {ip}, API-Path: {path}")
        # logger.info(20 * "^^^^^")
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=detail,
                    headers={"WWW-Authenticate": "Bearer"},
                )
    return user

