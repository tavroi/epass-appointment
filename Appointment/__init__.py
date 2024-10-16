from Utils.config import *
from Appointment.masters import *
from Appointment.appointment import book_appointment

MODULE_NAME = "appointment"
FILE_NAME = os.path.basename(__file__)

router = APIRouter(
    prefix=f'/{MODULE_NAME}',
    tags=[MODULE_NAME],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-premises")
async def premises_api(request: Request):
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    try:
        response = get_premises()
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: , File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
    return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
    return JSONResponse(content=return_response,
                        status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)

@router.get("/get-departments")
async def department_api(request: Request,premises=" "):
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    
    try:
        response = get_departments(premises)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: , File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
    return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
    return JSONResponse(content=return_response,
                        status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)


@router.get("/get-sub-departments")
async def sub_department_api(request: Request,department_id=" "):
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    try:
        response = get_sub_departments(department_id)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: , File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
    return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
    return JSONResponse(content=return_response,
                        status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)

@router.get("/get-officials")
async def sub_department_api(request: Request,sub_department_id=int):
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    try:
        response = get_officials(sub_department_id)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: , File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
    return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
    return JSONResponse(content=return_response,
                        status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)

@router.get("/get-time-slots")
async def time_slots_api(request: Request,officer_id='',department_id=" ",date=int):
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    try:
        response = get_time_slots(officer_id,department_id,date)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: , File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
    return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
    return JSONResponse(content=return_response,
                        status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)

@router.get("/get-status")
async def time_slots_api(request: Request):
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    try:
        response = get_status()
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: , File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
    return_response = return_process(data={}, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
    return JSONResponse(content=return_response,
                        status_code=HTTP_400_BAD_REQUEST if response.get("is_exception", False) else HTTP_200_OK)

@router.post("/book-appointment")
async def book_appointment_api(request: Request) -> JSONResponse:
    """
    
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    data = await request.json()
    try:
        response = book_appointment(data)
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        return JSONResponse(return_response, status_code=HTTP_200_OK if response['status'] else HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, Input-Data: {data}, File-Name: {FILE_NAME}, "
                     f"Method-Name: {method_name}")
        logger.info(20 * "====")
        response = {"message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(), "status": False, "is_exception": True}
        return_response = return_process(data=data, response=response, method=method, path=path, ip=ip,
                                         member_id=None, method_name=method_name, file_name=FILE_NAME,
                                         module_name=MODULE_NAME.capitalize(), code=response['code'])
        return JSONResponse(content=return_response, status_code=HTTP_400_BAD_REQUEST)
    