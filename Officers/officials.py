from Utils.config import *

def register_officials(officer_details: dict):
    try:
        telephone = officer_details.get("phone_number", " ")
        existing_officer = db.officials.find_one({"telephone": telephone})

        if existing_officer:
            message = "Officer already exists"
            return {
                "data": {},
                "status": False,
                "code": READ_CODE,
                "errorMessage": "",
                "message": message
            }

        user_data = {
            "_id": unique_id(),
            "name": officer_details.get("name", " "),
            "email": officer_details.get("email", " "),
            "telephone": telephone,
            "designation": officer_details.get("designation", " "),
            "last_login": "",
            "login_count": 0,
            "password": "",
            "is_active": True,
            "is_deleted": False,
            "qualification": officer_details.get("qualification", " "),
            "officer_id": None,
            "created_at": current_timestamp(),
            "sub_department_id": officer_details.get("sub_department_id", " ")
        }

        last_officer = db.officials.find_one(sort=[("officer_id", -1)]) 
        new_officer_id = last_officer["officer_id"] + 1 if last_officer else 1
        user_data["officer_id"] = new_officer_id

        db.officials.insert_one(user_data)

        message = "Official added successfully."
        return {
            "data": {},
            "status": True,
            "code": READ_CODE,
            "errorMessage": "",
            "message": message
        }
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {
            "code": EXCEPTION_CODE,
            "data": {},
            "message": EXCEPTION_MESSAGE,
            "errorMessage": str(e),
            "status": False
        }

def add_managers(officer_id, manager_details: list):
    try:
        if len(manager_details) > 6:
            message = "Cannot assign more than 4 managers."
            return {
                "data": {},
                "status": False,
                "code": READ_CODE,
                "errorMessage": "",
                "message": message
            }

        existing_telephones = set()
        
        for manager in manager_details:
            telephone = manager.get("phone_number", " ")
            existing_manager = db.managers.find_one({"officer_id": int(officer_id), "telephone": telephone})

            if existing_manager:
                existing_telephones.add(telephone)
                print(existing_telephones)

        for manager in manager_details:
            telephone = manager.get("phone_number", " ")
            
            if telephone in existing_telephones:
                message = f"Manager already exists for this officer."
                return {
                    "data": {},
                    "status": False,
                    "code": READ_CODE,
                    "errorMessage": "",
                    "message": message
                }

            manager_data = {
                "_id": unique_id(),
                "officer_id": officer_id,
                "name": manager.get("name", ""),
                "telephone": telephone,
                "email": manager.get("email", ""),
                "created_at":current_timestamp()
            }
            db.managers.insert_one(manager_data)

        message = "Managers added successfully."
        return {
            "data": {},
            "status": True,
            "code": READ_CODE,
            "errorMessage": "",
            "message": message
        }
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {
            "code": EXCEPTION_CODE,
            "data": {},
            "message": EXCEPTION_MESSAGE,
            "errorMessage": str(e),
            "status": False
        }
