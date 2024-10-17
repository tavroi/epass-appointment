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

def get_departments(premises):
    try:
        result=list(db.departments.find({"premises_id":int(premises)}))
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
    
def get_officials(sub_department_id):
    try:
        result=list(db.officials.find({"sub_department_id":int(sub_department_id),"is_active":True}))
        print(result)
        if result:
            return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "Officials list"}
        else:
            return {"data": result, "status": True, "code": READ_CODE, "errorMessage": "", "message": "No officials found"}
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
    
def get_time_slots(officer_id, department_id, date):
    try:
        date_obj = datetime.fromtimestamp(int(date))
        now = datetime.now()
        today = now.date()
        day_of_week = date_obj.weekday()
        print("day:", day_of_week)

        officer_availability = db.officers_availability.find_one({
            "officer_id": int(officer_id),
            "day": day_of_week,
            "valid_from": {"$lte": int(date)},
            "valid_to": {"$gte": int(date)}
        })

        available_slots = []  
        seen_slot_ids = set()  # Set to track added slot IDs

        if officer_availability:
            slot_ids = officer_availability.get("slot", [])
            print("Slot IDs:", slot_ids)

            slots = list(db.slots.find({"slot_id": {"$in": slot_ids}}))
            print("Slots:", slots)

            if slots:
                for slot in slots:
                    slot_time_str = slot['slot_time']
                    slot_id = slot['slot_id']  # Get the slot ID
                    start_time_str, end_time_str = slot_time_str.split(" - ")

                    slot_start = datetime.strptime(start_time_str, '%H:%M').time()
                    slot_start_datetime = datetime.combine(now.date(), slot_start)

                    if date_obj.date() == today:
                        if slot_start_datetime > now:  
                            if slot_id not in seen_slot_ids:  # Check for duplicates
                                available_slots.append(slot)
                                seen_slot_ids.add(slot_id)  # Add to seen set
                    else:
                        if slot_id not in seen_slot_ids:  # Check for duplicates
                            available_slots.append(slot)
                            seen_slot_ids.add(slot_id)  # Add to seen set

                if available_slots:
                    available_slots.sort(key=lambda x: datetime.strptime(x['slot_time'].split(" - ")[0], '%H:%M'))
                    return {"data": available_slots, "status": True, "code": READ_CODE,
                            "errorMessage": "", "message": "Available time slots for officer"}

        holiday_obj = db.department_holidays.find_one({"holiday_date": int(date)})
        if holiday_obj:
            holiday_date = [holiday_obj.get("holiday_date", " ")]
            if int(date) in holiday_date:
                return {"data": [], "status": False, "code": READ_CODE,
                        "errorMessage": "", "message": "No available slots on holidays"}

        departments = list(db.department_roster.find({"department_id": int(department_id)}))

        if not departments:
            return {"data": [], "status": False, "code": READ_CODE,
                    "errorMessage": "Department not found", "message": ""}

        slots = list(db.slots.find({}))

        for department in departments:
            week_off_days = [department.get("week_off", [])]
            print("Week off days:", week_off_days)
            if day_of_week in week_off_days:
                return {"data": [], "status": False, "code": READ_CODE,
                        "errorMessage": "No available slots on weekends", "message": ""}

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
                slot_id = slot['slot_id']  # Get the slot ID
                start_time_str, end_time_str = slot_time_str.split(" - ")

                slot_start = datetime.strptime(start_time_str, '%H:%M').time()
                slot_end = datetime.strptime(end_time_str, '%H:%M').time()

                slot_start_datetime = datetime.combine(now.date(), slot_start)

                if (dept_start <= slot_start < dept_end) and not (lunch_start < slot_start < lunch_end or lunch_start < slot_end <= lunch_end):
                    
                    if date_obj.date() == today:
                        if slot_start_datetime > now:  
                            if slot_id not in seen_slot_ids:  # Check for duplicates
                                available_slots.append(slot)
                                seen_slot_ids.add(slot_id)  # Add to seen set
                    else:
                        if slot_id not in seen_slot_ids:  # Check for duplicates
                            available_slots.append(slot)
                            seen_slot_ids.add(slot_id)  # Add to seen set

        available_slots.sort(key=lambda x: datetime.strptime(x['slot_time'].split(" - ")[0], '%H:%M'))

        return {"data": available_slots, "status": True, "code": READ_CODE,
                "errorMessage": "", "message": "Available time slots"}

    except Exception as e:
        logger.error(f"Exception Message: {traceback.format_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE,
                "errorMessage": str(e), "status": False}