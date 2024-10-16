from Utils.config import *
from Officers.officials import register_officials,add_managers

MODULE_NAME = "officials"
FILE_NAME = os.path.basename(__file__)

router = APIRouter(
    prefix=f'/{MODULE_NAME}',
    tags=[MODULE_NAME],
    responses={404: {"description": "Not found"}}
)

@router.post("/register-officer")
async def register_officers_api(request: Request) -> JSONResponse:
    """
    
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    data = await request.json()
    try:
        response = register_officials(data)
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
    
@router.post("/add-manager")
async def add_manager_api(request: Request,officer_id:int) -> JSONResponse:
    """
    
    """
    method_name = inspect.stack()[0][3]
    method, path, ip = get_request_data(request)
    data = await request.json()
    try:
        response = add_managers(officer_id,data)
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