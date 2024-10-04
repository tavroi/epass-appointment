from Utils.config import *
from Appointment.masters import *

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