from Utils.config import *
from Utils.send_mail import EmailUtility

Email_obj = EmailUtility

def appointment_booking_id():
    return f'DIGI{uuid.uuid4().hex[:12].upper()}'

def book_appointment(appointment_details: dict):
    try:
        logger.info("appointment_obj %s", appointment_details)
        mobile_no = appointment_details.get("mobile_no", " ")

        visitors = appointment_details['visitors']
        if not visitors:
            return {
                "data": {},
                "status": False,
                "code": READ_CODE,
                "errorMessage": "",
                "message": "No visitors provided."
            }

        reference_id = appointment_booking_id()

        for index, visitor in enumerate(visitors):
            mobile_no = visitor.get("phone_number")[-12:]
            name_parts = visitor.get("name").strip().split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])   
            visitor_id = unique_id() 

            existing_visitor = db.visitors.find_one({"phone_number": mobile_no})

            if existing_visitor is None:
                visitor_data = {
                    "_id": visitor_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "gender": visitor.get("gender"),
                    "phone_number": mobile_no,
                    "email_id": visitor.get("email_id"),
                    "created_at": current_timestamp()
                }
                db.visitors.insert_one(visitor_data)
            else:
                first_name = existing_visitor.get("first_name", "")
                last_name = existing_visitor.get("last_name", "")
                visitor_id = existing_visitor.get("_id")

            appointment_date = visitor.get("appointment_date", " ")
            slot_id = visitor.get("slot_id", " ")

            existing_appointments = list(db.appointment_bookings.find({
                "visitor_id": visitor_id,
                "appointment_date": int(appointment_date),
                "slot_id": slot_id,
                "officer_id": visitor.get('officer_id', '')
            }))

            if existing_appointments:
                message = "Appointment request already submitted for this visitor."
                return {
                    "data": {},
                    "status": False,
                    "code": READ_CODE,  
                    "errorMessage": "",
                    "message": message
                }

            appointment_id = reference_id if index == 0 else appointment_booking_id()

            appointment_data = {
                "_id": unique_id(),
                "visitor_id": visitor_id,
                "phone_number": mobile_no,
                "dept_id": visitor.get('dept_id', ''),
                "officer_id": visitor.get('officer_id', ''),
                "purpose": visitor.get('purpose', ''),
                "slot_id": slot_id,
                "first_name": first_name,
                "last_name": last_name,
                "email_id": visitor.get("email_id", " "),
                "gender": visitor.get("gender", " "),
                "sub_department_id": visitor.get('sub_department_id', ''),
                "reference_appointment_id": reference_id,
                "state_id": visitor.get('state_id', ''),
                "district_id": visitor.get('district_id', ''),
                "designation": visitor.get('designation', ''),
                "appointment_date": appointment_date,
                "organization_name": visitor.get('organization_name', ''),
                "appointment_id": appointment_id, 
                "created_at": current_timestamp(),
                "appointment_status": "pending"
            }

            db.appointment_bookings.insert_one(appointment_data)

            visitor_obj = db.visitors.find_one({"_id":visitor_id})
                    
            event_id = "5f39de7305624e33a02fcc0c874b1ac7" 
            email_obj = db.email_content.find_one({"event_id":event_id,"type_id": 7})
            print(email_obj)
                    
            email = visitor.get("email_id")
            officer_id = visitor.get('officer_id',' ')
            name = first_name + " " + last_name
            campaing_type = "auto"
            body = email_obj.get("body")
            subject = email_obj.get("subject")
            official_obj = db.officials.find_one({"officer_id":int(officer_id)})
            
            appointment_date_visitor = convert_datetime(appointment_date)
            appointment_time= get_slot_times(slot_id)
            mail_template_body = format_invite_mail(body, name,official_obj,appointment_date_visitor,appointment_time)
            mail_invite_subject = subject
            if email: 
                msg_data = {
                    "recipient": email,
                    "subject": mail_invite_subject,
                    "message": mail_template_body
                }
            email_response = Email_obj.SendEmailToDistrictUser(msg_data,[email],event_id,1,name,campaing_type)
            logger.info("email_response----->>>",email_response)

            if visitor_obj.get("on_whatsapp"):
                    type_id = 1
                    mobile_no= str(visitor_obj.get("phone_number"))[-12:]
                    template_id = "1270452274119007"
                    campaing_id=" "
                    redirect_url = " "
                    response = send_whatsapp_message(template_id, mobile_no,officer_id,appointment_date_visitor,appointment_time,type_id,name,campaing_type,campaing_id,redirect_url)
                    print( response)

        message = "Appointment request submitted successfully."
        return {
            "data":appointment_data,
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
    
def check_appointment(details: dict):
    try:
        phone_number = details.get("phone_number", '')
        officer_id = details.get("officer_id", '')
        slot_ids = details.get('slot_ids', '')
        appointment_date = details.get("appointment_date", '')

        visitor_obj = db.visitors.find_one({"phone_number": phone_number})
        if not visitor_obj:
            return {
                "data": {},
                "status": False,
                "code": READ_CODE,
                "errorMessage": "Visitor not found.",
                "message": ""
            }

        visitor_id = visitor_obj.get("_id")
        verified = visitor_obj.get("is_verified", False)

        existing_appointments = db.appointment_bookings.find_one({
            "visitor_id": visitor_id,
            "appointment_date": int(appointment_date),
            "slot_id": slot_ids,
            "officer_id": officer_id
        })

        if existing_appointments:
            appointment_reference_id = existing_appointments.get("appointment_reference_id")
            all_appointments = db.appointment_bookings.find({"appointment_reference_id": appointment_reference_id})

            appointment_data = []
            for appointment in all_appointments:
                other_visitor = db.visitors.find_one({"_id": appointment.get("visitor_id")})
                time_diff=(appointment.get('appointment_date',0)-current_timestamp())/3600
                logger.info("time_diff  %s", time_diff)

                if time_diff<24:
                    send_consent = True
                else :
                    send_consent = False
                appointment_info = {
                    "_id": appointment.get("_id"),
                    "visitor_id": appointment.get("visitor_id"),
                    "phone_number": appointment.get("phone_number"),
                    "dept_id": appointment.get("dept_id"),
                    "officer_id": appointment.get("officer_id"),
                    "purpose": appointment.get("purpose"),
                    "slot_id": appointment.get("slot_id"),
                    "first_name": appointment.get("first_name"),
                    "last_name": appointment.get("last_name"),
                    "email_id": appointment.get("email_id"),
                    "sub_department_id": appointment.get("sub_department_id"),
                    "reference_appointment_id": appointment.get("reference_appointment_id"),
                    "state_id": appointment.get("state_id"),
                    "district_id": appointment.get("district_id"),
                    "designation": appointment.get("designation"),
                    "appointment_date": appointment.get("appointment_date"),
                    "organization_name": appointment.get("organization_name"),
                    "appointment_id": appointment.get("appointment_id"),
                    "created_at": appointment.get("created_at"),
                    "appointment_status": appointment.get("appointment_status"),
                    "send_consent": send_consent,
                    "visitor_verified": other_visitor.get("is_verified", False) if other_visitor else None
                }
                appointment_data.append(appointment_info)

            return {
                "data": {
                    "appointment_data": appointment_data,
                },
                "status": True,
                "code": READ_CODE,
                "errorMessage": "",
                "message": ""
            }

        if verified:
            return {
                "data": {"visitor_verified": verified},
                "status": True,
                "code": READ_CODE,
                "errorMessage": "",
                "message": "User is already verified."
            }

        return {
            "data": {},
            "status": True,
            "code": READ_CODE,
            "errorMessage": "",
            "message": ""
        }

    except Exception as e:
        logger.error(f"Exception Message: {traceback.format_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {
            "code": EXCEPTION_CODE,
            "data": {},
            "message": EXCEPTION_MESSAGE,
            "errorMessage": str(e),
            "status": False
        }
