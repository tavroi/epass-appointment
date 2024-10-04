from Utils.config import *

def get_premises():
    try:
        result=list(db.premises.find({}))
        return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "premises list"}
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}
