from Utils.config import *
import traceback    
from Utils.face_match import *
from Utils.utilities import check_name, generate_qr, is_base64
# import face_recognition
from PIL import Image
import io
from Utils.encryption import  encrypt_base64_string, decrypt_to_base64_string

def check_image_properties(base64_string):

    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(base64_string)
    # Check the file size
    file_size_kb = len(image_bytes) / 1024  # Convert bytes to KB
    print(f"File size: {file_size_kb:.2f} KB")

    # if file_size_kb >= 100:
    if file_size_kb >= 100:
        return False, f"The image file size is 100 KB or more. File size: {file_size_kb:.2f} KB"
    
    # Open the image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size
    print(f"Image resolution: {width}x{height}")

    # Check if the resolution is within the range
    if not (150 <= width <= 500 and 600 <= height <= 1200):
        return False, f"The image resolution is outside the specified range. Resolution is {width}x{height}"
    

    # temporary
    return True, ""

    # Convert the PIL image to a format compatible with face_recognition
    # image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    # face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return False, "No face detected in the image."

    # Get the size of the first detected face
    top, right, bottom, left = face_locations[0]
    face_width = right - left
    face_height = bottom - top

    face_area = face_width * face_height
    image_area = width * height

    face_fraction = face_area / image_area
    print(f"Face fraction of the image: {face_fraction:.2f}")

    # Check if the face takes up more than 1/3 but no more than 2/3 of the image
    if 1/3 < face_fraction <= 2/3:
        return True, f"The face takes up more than 1/3 but no more than 2/3 of the image. Face fraction of the image: {face_fraction:.2f}"  
    else:
        return False, f"The face does not take up more than 1/3 but no more than 2/3 of the image. Face fraction of the image: {face_fraction:.2f}"  
    

# ##########################################################################################################################################

def verify_face(face_from_machine, face_from_id):
    try:
        api_status, match_percentage, api_response = compare_faces_aws(face_from_machine, face_from_id)

        if api_status:
            if match_percentage > 0.90:
                return True, api_response, "Face match successful."
            else:
                return False, api_response, "Face verification failed."
        else:
            raise Exception("API status is false")
    except Exception as e:
        logger.error(f"Exception: {str(e)}, Traceback: {traceback.format_exc()}, File: {os.path.basename(__file__)}, Method: {inspect.stack()[0][3]}")
        return False, {}, "Face verification failed due to some technical issue."

def fetch_db_objects(data):
    # event_id = data.get('event_id','')
    appointment_id = data.get('appointment_id','')
    officials_obj, visitor_obj, appointment_obj=None, None, None
    appointment_obj = db.appointment_bookings.find_one({"appointment_id": appointment_id})

    logger.info("appointment id: %s, obj %s",appointment_id, appointment_obj)
    if appointment_obj:
        officials_obj = db.officials.find_one({"officer_id": int(appointment_obj.get('officer_id',''))})
        visitor_obj = db.visitors.find_one({ "_id":appointment_obj.get('visitor_id','')})

    return officials_obj, visitor_obj, appointment_obj

def create_initial_response():
    return {
        "send_consent": False,
        "encrypted_face_data":"",
        "qr_link": "",
        "data_qr_link": "",
        "is_valid":True
    }

def handle_existing_booking(booking_obj, response_obj):
    if booking_obj:
        response_obj["is_valid"] = False
        return {
            "message": BOOKING_ALREADY_VERIFIED,
            "data": response_obj,
            "status": True,
            "is_exception": False,
            "code": VALIDATION_FAIL_CODE,
            "errorMessage": BOOKING_ALREADY_VERIFIED
        }
    return None

def check_name_match(officials_obj, verification_details, user_obj, response_obj):
    if officials_obj.get('name_match', False):
        result = check_name(verification_details['name'], f"{user_obj.get('first_name','')} {user_obj.get('last_name','')}")
        
        if not result:
            result = check_name(verification_details['name'], f"{user_obj.get('first_name','')} {user_obj.get('first_name','')}")

        logger.info("NAME MATCH Result for %s: %s", verification_details['name'], result)
        
        
        if not result:
            response_obj["name_match"] = False
            return {
                "message": "Name does not match",
                "data": response_obj,
                "status": True,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": "Name does not match"
            }
        
    return None

def check_face_match(officials_obj, verification_details, response_obj):
    if officials_obj.get('face_match', False):
        logger.info("FACE from machine is_base64: %s, face from data is_base64: %s", 
                    is_base64(verification_details['face_data']), 
                    is_base64(verification_details['aadhar_data']['doc_face_image']))

        face_match_status, face_match_response, message = verify_face(
            verification_details['face_data'], 
            verification_details['aadhar_data']['doc_face_image']
        )

        logger.info("FACE MATCH RESPONSE %s", face_match_response)
        
        if not face_match_status:
            response_obj["face_match"] = False
            return {
                "message": "Face details do not match",
                "data": response_obj,
                "status": True,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": "Face details do not match"
            }
        
    return None

def update_verification_details(verification_details={}):
    try:
        logger.info("appointment ID: %s", verification_details.get('appointment_id'))
        appointment_id = verification_details.get('appointment_id')
        # event_id = verification_details.get('event_id')

        officer_obj, visitor_obj, appointment_obj = fetch_db_objects(verification_details)
        verify_response_obj = create_initial_response()
        # logger.info("Booking Info: %s, %s, %s", event_obj, visitor_obj, booking_obj)
        logger.info("Appointment Info: %s",appointment_obj)
        logger.info("VISITOR Info: %s",visitor_obj)

        if verification_details.get('face_data',"") !="":
            verify_response_obj['encrypted_face_data'] = encrypt_base64_string(verification_details['face_data'])

        if not appointment_obj:
            verify_response_obj["is_valid"] = False
            return {
                "message": NO_BOOKING_FOUND,
                "data": verify_response_obj,
                "status": True,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": NO_BOOKING_FOUND
            }
        
        if not visitor_obj:
            verify_response_obj["is_valid"] = False
            return {
                "message": "No visitor found",
                "data": verify_response_obj,
                "status": True,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": NO_BOOKING_FOUND
            }            
        if not officer_obj:
            verify_response_obj["is_valid"] = False
            return {
                "message": NO_OFFICER_FOUND,
                "data": verify_response_obj,
                "status": True,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": NO_OFFICER_FOUND
            }
        # if booking is aleady veriifed then return
        if appointment_obj.get('is_verified',False):
            verify_response_obj["is_valid"] = False
            return {
                "message": BOOKING_ALREADY_VERIFIED,
                "data": verify_response_obj,
                "status": True,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": BOOKING_ALREADY_VERIFIED
            } 
        

        is_valid, err_msg = check_image_properties(verification_details['face_data'])

        if is_valid:

            name_check_response = check_name_match(officer_obj, verification_details, visitor_obj, verify_response_obj)
            if name_check_response:
                return name_check_response
            logger.info("NAME CHAECK")

            face_check_response = check_face_match(officer_obj, verification_details, verify_response_obj)
            if face_check_response:
                return face_check_response

            # # Upload the face to AWS collection
            # AWSFaceMatch_obj = AWSFaceMatch()
            # aws_response = AWSFaceMatch_obj.add_faces_to_collection(booking_id, verification_details['face_data'], event_id)
            # verify_response_obj['encrypted_face_data'] = encrypt_base64_string(verification_details['face_data'])

            if verification_details.get('aadhar_data',{}):
                appointment_obj.update({
                    'doc_type': verification_details['aadhar_data']['doc_type'],
                    
                })
            else:
                appointment_obj.update({
                    'doc_type': 'photo'
                })

            # db.bookings.insert_one(visitor_obj)


            # Generate QR of booking ID
            qr_text = appointment_id
            response = generate_qr(qr_text)
            filepath = response['data'] if response['status'] else ""

            # update booking
            # db.visitors.update_one({"_id":visitor_obj['_id']}, {"$set":{'is_verified':True, 'verified_on':current_timestamp()}})
            db.appointment_bookings.update_one({"appointment_id": appointment_id}, {"$set":{'qr_link': filepath, 
                                                                              'is_verified':True, 
                                                                              'verified_on':current_timestamp(),
                                                                              'doc_type': appointment_obj['doc_type']
                                                                              }})

            verify_response_obj['qr_link'] = filepath
            

        else: 
            verify_response_obj['is_valid']=False
            return {
                "message": err_msg,
                "data": verify_response_obj,
                "status": False,
                "is_exception": False,
                "code": VALIDATION_FAIL_CODE,
                "errorMessage": err_msg
            }

        return {
            "data": verify_response_obj,
            "status": True,
            "code": READ_CODE,
            "errorMessage": "",
            "message": "Booking verified"
        }
    except Exception as e:
        logger.error(f"Exception: {str(e)}, Traceback: {traceback.format_exc()}, File: {os.path.basename(__file__)}, Method: {inspect.stack()[0][3]}")
        return {
            "code": EXCEPTION_CODE,
            "data": {},
            "message": EXCEPTION_MESSAGE,
            "errorMessage": str(e),
            "status": False
        }


def check_verification_status(data={}):
    try:
        appointment_id = data.get('appointment_id')
        logger.info("Booking ID: %s", appointment_id)

        message = "Proceed for verification"
        verify_response_obj = {"is_valid": True, 'is_verified':False, 'send_consent':False}
        code=READ_CODE

        appointment_obj = db.appointment_bookings.find_one({"appointment_id": appointment_id})
        logger.info("Appointment OBJ: %s", appointment_obj)

        # Handle case when booking is not found
        if not appointment_obj:
            # verify_response_obj["is_valid"] = False
            message = NO_BOOKING_FOUND
            return generate_response(message, verify_response_obj, VALIDATION_FAIL_CODE, False)

        # visitor_obj = db.visitors.find_one({"_id": booking_obj.get("visitor_id", '')})
        officials_obj = db.officials.find_one({"officer_id": int(officials_obj.get("officer_id", ''))})

        # Handle case when event is not found
        if not officials_obj:
            # verify_response_obj["is_valid"] = False
            message = NO_OFFICER_FOUND
            code=VALIDATION_FAIL_CODE
            return generate_response(message, verify_response_obj, code, False)
        

        # Handle case when visitor is already verified
        if appointment_obj.get("is_verified", False):                
            verify_response_obj["is_verified"] = True
            message = BOOKING_ALREADY_VERIFIED
            return generate_response(message, verify_response_obj, VALIDATION_FAIL_CODE, True)
        

        return generate_response(message, verify_response_obj, code, True)

    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": str(e),
                "status": False}

def generate_response(message, data, code, status):
    return {
        "message": message,
        "data": data,
        "status": status,
        "is_exception": False,
        "code": code,
        "errorMessage": message
    }



def visitor_details(appointment_id=''):
    try:
        logger.info("Booking ID: %s", appointment_id)
        appointment_obj = db.appointment_bookings.find_one({"appointment_id":appointment_id})

        message="Booking found."
        if not appointment_obj:                
            message = NO_BOOKING_FOUND
            return generate_response(message, {}, VALIDATION_FAIL_CODE, False)
         
        visitor_obj = db.visitors.find_one({"_id": appointment_obj.get("visitor_id", '')})
        
        # Handle case when visitor is already verified
        if visitor_obj.get("consent", False): 
            message = BOOKING_ALREADY_VERIFIED
            return generate_response(message, {}, VALIDATION_FAIL_CODE, False)
        
        # verify_response_obj["appointment_data"]=user_obj
        data=appointment_obj
        data["visitor_info"]= visitor_obj

        return {"message": message, "data": data, "status": True, "code": READ_CODE, "errorMessage": message }
    
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),"is_exception": True,
                "status": False}
    

def update_visitor_details(visitor_data={}):
    try:
        logger.info("Booking ID: %s", visitor_data.get('appointment_id'))
        appointment_id = visitor_data.get('appointment_id', '')
        officer_id = visitor_data.get('officer_id', '')

        verify_response_obj = create_initial_response()

        appointment_obj = db.appointment_bookings.find_one({"appointment_id":appointment_id})
        if not appointment_obj:                
            message = NO_BOOKING_FOUND
            return generate_response(message, verify_response_obj, VALIDATION_FAIL_CODE, False)
         
        visitor_obj = db.visitors.find_one({"_id": appointment_obj.get("visitor_id", '')})

        if not visitor_obj:
            return generate_response(NOT_FOUND.replace('{name}', "Visitor"), {}, VALIDATION_FAIL_CODE, False)        

        if appointment_obj.get("is_verified", False): 
            message = BOOKING_ALREADY_VERIFIED
            return generate_response(message, verify_response_obj, VALIDATION_FAIL_CODE, False)

        # is_valid, err_msg = check_image_properties(visitor_data['face_data'])   
        is_valid, err_msg =True, ""

        if not is_valid:   
            return generate_response(err_msg, verify_response_obj, VALIDATION_FAIL_CODE, False)
        
        
        # # upload the face to aws collection
        # AWSFaceMatch_obj= AWSFaceMatch()
        # aws_response= AWSFaceMatch_obj.add_faces_to_collection(booking_id, visitor_data['face_data'], event_id)

        # logger.info("AWS_response: %s", aws_response)

        if appointment_obj.get('payment_status')=="Completed" and appointment_obj.get('is_verified', False):
            verify_response_obj["send_consent"]=True
            message="booking verified"

        verify_response_obj['encrypted_face_data'] = encrypt_base64_string(visitor_data['face_data'])
        # generate QR of booking ID
        qr_text=  appointment_id
        response = generate_qr(qr_text)
        filepath = response['data'] if response['status'] else ""
        print(filepath)

        verify_response_obj['qr_link']=filepath

        # update booking
        # db.visitors.update_one({"_id":visitor_obj['_id']}, {"$set":{'is_verified':True, 'verified_on':current_timestamp()}})
        db.appointment_bookings.update_one({"appointment_id": appointment_id}, {"$set":{'qr_link': filepath, 'is_verified':True, 'verified_on':current_timestamp()}})


        return {"data": verify_response_obj , "status": True, "code": UPDATED_CODE, "errorMessage": "", "message": message}
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}



def get_face_match_percentage(data):
    try:
        logger.info("FACE from machine is_base64: %s, face from data is_base64: %s", 
                    is_base64(data['captured_face_image']), 
                    is_base64(data['doc_face_image']))
        api_status, match_percentage, api_response = compare_faces_aws(data['captured_face_image'], 
            data['doc_face_image'])
        
        return {
            "message": "",
            "data": {'match_percentage':match_percentage},
            "status": api_status,
            "is_exception": False,
            "code":READ_CODE,
            "errorMessage": ""
        }
    except Exception as e:
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: {inspect.stack()[0][3]}")
        logger.info(20 * "....")
        return {"code": EXCEPTION_CODE, "data": {}, "message": EXCEPTION_MESSAGE, "errorMessage": e.__str__(),
                "status": False}


# he
