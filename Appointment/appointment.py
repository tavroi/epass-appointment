from Utils.config import *

def appointment_id():
    return f'DIGI{uuid.uuid4().hex[:12].upper()}'

def book_appointment(appointment_details: dict):
    try:
        mobile_no = appointment_details.get("phone_number")[-12:]
        name_parts = appointment_details.get("name"," ").strip().split()
        visitor_id = appointment_details.get("visitor_id")
        appointment_date = appointment_details.get("appointment_date", " ")
        slot_id = appointment_details.get("slot_id", " ")

        existing_visitor = db.visitors.find_one({"_id": visitor_id})

        existing_appointment = db.appointment_bookings.find_one({
            "appointment_date": appointment_date,
            "slot_id": slot_id,
            "officer_id": appointment_details.get('officer_id', '')
        })

        if existing_appointment:
            message = "Appointment request already submitted."
            return {
                "data": {},
                "status": False,
                "code": READ_CODE,  
                "errorMessage": "",
                "message": message
            }

        if existing_visitor is None:
            visitor_id = unique_id() 
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) 
            visitor_data = {
                "_id": visitor_id,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": mobile_no,
                "created_at": current_timestamp()
            }
            db.visitors.insert_one(visitor_data)
        else:
            first_name = existing_visitor.get("first_name", "")
            last_name = existing_visitor.get("last_name", "")

        appointment_data = {
            "_id":unique_id(),
            "visitor_id": visitor_id,
            "phone_number": mobile_no,
            "dept_id": appointment_details.get('dept_id', ''),
            "officer_id": appointment_details.get('officer_id', ''),
            "purpose": appointment_details.get('purpose', ''),
            "slot_id": slot_id,
            "first_name": first_name,
            "last_name":last_name,
            "gender": appointment_details.get("gender"," "),
            "sub_department_id": appointment_details.get('sub_department_id', ''),
            "state_id": appointment_details.get('state_id', ''),
            "district_id": appointment_details.get('district_id', ''),
            "designation": appointment_details.get('designation', ''),
            "appointment_date": appointment_date,
            "organization_name": appointment_details.get('organization_name', ''),
            "appointment_id": appointment_id(),
            "created_at": current_timestamp(),
            "appointment_status": "pending"
        }

        db.appointment_bookings.insert_one(appointment_data)
        
        message = "Appointment request submitted successfully."
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
            "errorMessage": e.__str__(),
            "status": False
        }
