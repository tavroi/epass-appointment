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

def get_departments():
    try:
        result=list(db.departments.find({}))
        return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "Departments list"}
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}
    
def get_sub_departments(department_id):
    try:
        result=list(db.sub_departments.find({"department_id":int(department_id)}))
        return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "Sub department list"}
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}
    
def get_officials():
    try:
        result=list(db.officials.find({"is_active":True}))
        return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "Officials list"}
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}
    
def get_status():
    try:
        result=list(db.appointment_status.find({}))
        return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "status list"}
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}
    

def get_time_slots(officer_id, department_id, date, day):
    try:
        date_obj = datetime.fromtimestamp(int(date))

        now = datetime.now()
        today = now.date()

        # Check if the officer_id exists and get available slot_ids
        officer_availability = db.officers_availability.find_one({"officer_id": int(officer_id), "day": int(day)})
        print("officer_availability:",officer_availability)

        if officer_availability:
            slot_ids = officer_availability.get("slot", [])
            print(slot_ids)
            # Fetch the relevant slots for the officer
            slots = list(db.slots.find({"slot_id": {"$in": slot_ids}}))
            print("slots:",slots)

            # Immediately return officer's available slots if they exist
            if slots:
                available_slots = {slot['slot_time'] for slot in slots}
                sorted_available_slots = sorted(available_slots, key=lambda x: datetime.strptime(x.split(" - ")[0], '%H:%M'))
                return {"data": list(sorted_available_slots), "status": True, "code": READ_CODE,
                        "errorMessage": "", "message": "Available time slots for officer"}

        # If officer_id does not exist or has no slots, proceed with the original flow
        slots = list(db.slots.find({}))

        departments = list(db.department_roster.find({"department_id": int(department_id)}))

        if not departments:
            return {"data": [], "status": False, "code": READ_CODE, 
                    "errorMessage": "Department not found", "message": ""}

        available_slots = set()  

        for department in departments:
            if date_obj.weekday() in [6, 7]: 
                if "saturday" in department.get("week_off", []) or "sunday" in department.get("week_off", []):
                    continue  

            dept_start_time = department.get("start_time", 0)  
            dept_end_time = department.get("end_time", 86400)  
            lunch_start_time = department.get("lunch_start_time", 46800) 
            lunch_end_time = department.get("lunch_end_time", 48600) 

            dept_start = seconds_to_time(dept_start_time)
            dept_end = seconds_to_time(dept_end_time)
            lunch_start = seconds_to_time(lunch_start_time)
            lunch_end = seconds_to_time(lunch_end_time)

            for slot in slots:
                slot_time_str = slot['slot_time']  
                start_time_str, end_time_str = slot_time_str.split(" - ")

                slot_start = datetime.strptime(start_time_str, '%H:%M').time()
                slot_end = datetime.strptime(end_time_str, '%H:%M').time()

                # Create a datetime object for today's date with the slot start time
                slot_start_datetime = datetime.combine(now.date(), slot_start)

                if (dept_start <= slot_start < dept_end) and not (lunch_start < slot_start < lunch_end or lunch_start < slot_end <= lunch_end):
                    if date_obj.date() == today:
                        if slot_start_datetime > now:  # Compare with datetime object
                            available_slots.add(slot_time_str) 
                    else:
                        available_slots.add(slot_time_str)  

        sorted_available_slots = sorted(available_slots, key=lambda x: datetime.strptime(x.split(" - ")[0], '%H:%M'))
                       
        return {"data": list(sorted_available_slots), "status": True, "code": READ_CODE, 
                "errorMessage": "", "message": "Available time slots"}

    except Exception as e:
        logger.error(f"Exception Message: {traceback.format_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, 
                "errorMessage": str(e), "status": False}
