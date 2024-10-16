from Utils.config import *
from Verify.verify import update_verification_details, check_verification_status, update_visitor_details, visitor_details, get_face_match_percentage
from Utils.logging import create_user_logs

MODULE_NAME = "verify"
FILE_NAME = os.path.basename(__file__)

router = APIRouter(
    prefix=f'/{MODULE_NAME}',
    tags=[MODULE_NAME],
    responses={404: {"description": "Not found"}}
)


@router.post("/booking")
async def booking_verification_api(request: Request) -> JSONResponse:
    """
        # verfiy the booking when first time mking entry in system
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    data = await request.json()
    try:    
        response = update_verification_details(data)
        # logger.info("Verification Response %s", response)
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        create_user_logs(data.get('booking_id',''),agent_name='user', verification_done=True if response['status'] else False, 
                         stage=2, request=data,response=response )
        return JSONResponse(return_response, status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: {data}, File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        create_user_logs(data.get('booking_id',''),agent_name='user', verification_done=False, stage=2, request=data,response=response )
        return JSONResponse(content=return_response, status_code=HTTP_400_BAD_REQUEST)
    

@router.post("/booking-status")
async def check_verification_api(request: Request) -> JSONResponse:
    """
        # verfiy the booking when first time making entry in system
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    data = await request.json()
    try:    
        response = check_verification_status(data)
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        return JSONResponse(return_response, status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: {data}, File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        return JSONResponse(content=return_response, status_code=HTTP_400_BAD_REQUEST)
    


@router.get("/visitor-details/{booking_id}")
async def visitor_details_api(booking_id:str, request: Request) -> JSONResponse:
    """
    Get Visitor details for manual verififcation
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    # data = await request.json()
    try:
        token = request.headers.get("authorization")

        if token == "9beaa95b-c59f-4ec9-bb60-5f4ee1986311":
            response = visitor_details(booking_id)
        else:
            response= {'status':False,"message": "unauthorized access", "code":UNAUTHORIZED_ACCESS_CODE, "errorMessage":"" }

        return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        return JSONResponse(return_response, status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: {{}}, File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
        return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        return JSONResponse(content=return_response, status_code=HTTP_400_BAD_REQUEST)
  


@router.post("/update-visitor-details")
async def manual_verification_api(request: Request) -> JSONResponse:
    """
    update verification manually
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    data = await request.json()
    try:
        token = request.headers.get("authorization")

        if token == "9beaa95b-c59f-4ec9-bb60-5f4ee1986311":
            response = update_visitor_details(data)
        else:
            response= {'status':False,"message": "unauthorized access", "code":UNAUTHORIZED_ACCESS_CODE, "errorMessage":"" }

        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        create_user_logs(data.get('booking_id', ''), agent_name=data.get('agent_name',''), verification_done= True if response['code']=='202' else False,
                         stage=2, request=data, response=response )
        return JSONResponse(return_response, status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: {data}, File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        create_user_logs(data.get('booking_id', ''), agent_name=data.get('agent_name',''), verification_done= True if response['code']=='202' else False,
                         stage=2, request=data, response=response )
        return JSONResponse(content=return_response, status_code=HTTP_400_BAD_REQUEST)
    


get_face_match_percentage
@router.post("/face")
async def face_match_api(request: Request) -> JSONResponse:
    """
    update verification manually
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    user_agent = request.headers.get("user-agent", "unknown")
    data = await request.json()
    try:
        token = request.headers.get("authorization")

        if token == "9beaa95b-c59f-4ec9-bb60-5f4ee1986311":
            response = get_face_match_percentage(data)
        else:
            response= {'status':False,"message": "unauthorized access", "code":UNAUTHORIZED_ACCESS_CODE, "errorMessage":"" }

        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'],user_agent=user_agent)
        create_user_logs(data.get('booking_id', ''), agent_name=data.get('agent_name',''), verification_done= True if response['code']=='202' else False,
                         stage=2, request=data, response=response )
        return JSONResponse(return_response, status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: {data}, File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        create_user_logs(data.get('booking_id', ''), agent_name=data.get('agent_name',''), verification_done= True if response['code']=='202' else False,
                         stage=2, request=data, response=response )
        return JSONResponse(content=return_response, status_code=HTTP_400_BAD_REQUEST)

