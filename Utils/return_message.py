EXCEPTION_MESSAGE = "Something Went Wrong!"
CREATED = "{name} created successfully."
UPDATED = "{name} updated successfully."
DELETED = "{name} deleted successfully."
ALREADY_EXISTS ="{name} already exists."
FILE_ERROR = "Invalid Data in {name} File."
WRONG_ID = "Please enter correct {name}."
NOT_ACTIVE = "{name} is not active."
NOT_FOUND_OR_ACTIVE = "{name} is not found or not active."
NOT_FOUND = "{name} not found."
VERIFIED = "{name} verified successfully."
NOT_VALID = "Requested Data is not valid"
UNIQUE = "Please enter unique {name}"
USER_ERROR_MESSAGE = "There is some technical Issue. Please try after some time."
READ_SUCCESS_MESSAGE = "{name} listing."
READ_SUCCESS_DETAIL_MESSAGE = "{name} detail."
GOV_SERVER_DOWN = "Government Server is Down. Please check after some time."
SEND_SUCCESSFUL = "{name} send successfully."
INVALID_CREDENTIALS = "Invalid Credentials"
REQUIRED = "{name} is required field"
ABSENT = "User Not Found"
DISABLED = "User disabled"
LOGGED_IN = "Successfully Logged In"
LOGGED_OUT = "Successfully Logged Out"
EXPIRED = "Token is already expired"
NOT_SUPPORTED = "{name} not Supported"

BOOKING_ALREADY_VERIFIED= "Booking has already been verified and is confirmed"
NO_BOOKING_FOUND="No booking found. please verify details and try again"
NO_EVENT_FOUND="No event found. please verify details and try again"
INVALID = "Please specify valid {name}"
NOTIFICATION_DAY = "Please specify valid notification day."
INVALID_TEMPLATE = "Please specify valid template id."
INVALID_WA_ACCESS_TOKEN = "Please specify valid Wa access token."
# EMAIL_NOTIFICATION_LINK= "Dear {name},\n\nThank you for registering for the event! Your registration has been completed.\nPlease proceed with the verification process by clicking on the following link:\n{link}\n\nIf you have any questions or need further assistance, please do not hesitate to contact us.\n\nBest regards,\nJITO"

EMAIL_VERIFICATION_DONE= "Dear {name},\n\nWe are pleased to inform you that your verification is complete.\nPlease use the following QR code for entry into the event. \n\nWe look forward to seeing you at the event! If you have any questions or need further assistance, please do not hesitate to contact us at {contact_us_at}.\n\nBest regards,\n{signature}"

CONSENT_CONFIRMATION="Dear User,\n\nYour consent has been recored successfully. \n\nBest regards\n{signature}"
EMAIL_NOTIFICATION_LINK="Dear {name},\n\nThank you for registering for the event! Your registration has been successfully completed. Please proceed with the verification process by clicking on the following link:\n{link}\n\nIf you have any questions or need further assistance, please do not hesitate to contact Bhagyashila at +91 7447864520. (The helpline number will start working only after 12 PM on June 27th, 2024.)\n\nPlease note that this verification process is compulsory for seamless entry into the event venue, as it involves a facial recognition entry system.\n\nBest regards,\nTeam Pagariya JBN Mahakumbh"


TEMPLATE_EVENT_CANCELLED = "Dear {visitor_name}, we regret to inform you that event  {event_name} is canceled."
TEMPLATE_APPOINTMENT_CONFIRM = "Dear {visitor_name}, Your appointment is confirmed with {officer_name}.\nYou can download you ePass by clicking on this link:\n{epass_url}"
EMAIL_TEMPLATE_APPOINTMENT_CONFIRM = "Dear {visitor_name}, Your appointment is confirmed with {officer_name}.\nYou can download you ePass by clicking on this link:\n{epass_url}"

TEMPLATE_APPOINTMENT_CANCELLED = "Dear {visitor_name}, we regret to inform you that your appointment request is declined with officer {officer_name} with rejection reason: {remarks}."


EMAIL_TEMPLATE_EVENT_CONFIRM = "Dear {visitor_name},\n\nYour booking is confirmed for event: {event_name} on {event_date} at {event_start_time}. You can download you ePass by clicking on this link:\n{epass_url}"
TEMPLATE_EVENT_CONFIRM = "Dear {visitor_name}, Your booking is confirmed for event: {event_name} on {event_date} at {event_start_time}. Here is your ePass."
TEMPLATE_EVENT_CONFIRM_WA = "455620377149563"

TEMPLATE_EVENT_REJECT = "Dear {visitor_name},\n\nYour booking request for the event: {event_name} has been rejected due to {remarks}."
TEMPLATE_EVENT_REJECT_WA = "684330770452894"


# Invite for Events
EVENT_INVITE_SUBJECT = "You're Invited! Join Us for {event_name}"
EVENT_INVITE_BODY = 'Dear {guest_name},\n\nWe hope this email finds you well! We are excited to extend a warm invitation to you for our upcoming {event_name} taking place on {event_date} at {event_location}.\n\nHere are the event details:\n\n- Event Name: {event_name}\n- Date: {event_date}\n- Time: {event_time}\n- Address: {full_address}\n- Map Link: {map_link}\n\nTo secure your spot, please go to the following link for verification.\n{verification_link}\n\nWe encourage you to respond at your earliest convenience.\n\nWe hope to see you at the event and looking forward to welcoming you.\n\nBest regards'
EVENT_WA_INVITE_MESSAGE = """Dear {guest_name},\n\nWe're thrilled to extend an invitation to you for our upcoming event. Here are the key details:\n\nEvent Name: {event_name}\nDate: {event_date}\nTime: {event_time}\nLocation: {event_location}\nMap Link: {map_link}\nTo ensure your spot, kindly verify your attendance by visiting the following link: {verification_link}\n\nYour prompt response would be greatly appreciated. We eagerly anticipate your presence.\n\nThank you, and we hope to see you there!\n\nBest regards,"""

# Event Cancelled
EVENT_CANCELLED_SUBJECT = 'Subject: {event_name} - Cancellation Notice'
EVENT_CANCELLED_MAIL = 'Dear {guest_name},\n\nWe regret to inform you that the {event_name} on {event_date} with reference id {ref_id}, is canceled due to {reason}.\n\nWe apologize for any inconvenience this may cause and appreciate your understanding.\n\nThank you for your support.\n\nBest regards,\n{premise_name}'

TEMPLATE_EVENT_CANCELLED = "Dear {visitor_name}, we regret to inform you that event  {event_name} is canceled."
TEMPLATE_APPOINTMENT_CONFIRM = "Dear {visitor_name}, Your appointment is confirmed with {officer_name}.\nYou can download you ePass by clicking on this link:\n{epass_url}"
EMAIL_TEMPLATE_APPOINTMENT_CONFIRM = "Dear {visitor_name}, Your appointment is confirmed with {officer_name}.\nYou can download you ePass by clicking on this link:\n{epass_url}"

TEMPLATE_APPOINTMENT_CANCELLED = "Dear {visitor_name}, we regret to inform you that your appointment request is declined with officer {officer_name} with rejection reason: {remarks}."


EMAIL_TEMPLATE_EVENT_CONFIRM = "Dear {visitor_name},\n\nYour booking is confirmed for event: {event_name} on {event_date} at {event_start_time}. You can download you ePass by clicking on this link:\n{epass_url}"
TEMPLATE_EVENT_CONFIRM = "Dear {visitor_name}, Your booking is confirmed for event: {event_name} on {event_date} at {event_start_time}. Here is your ePass."
TEMPLATE_EVENT_CONFIRM_WA = "455620377149563"

TEMPLATE_EVENT_REJECT = "Dear {visitor_name},\n\nYour booking request for the event: {event_name} has been rejected due to {remarks}."
TEMPLATE_EVENT_REJECT_WA = "684330770452894"


# Invite for Events
EVENT_INVITE_SUBJECT = "You're Invited! Join Us for {event_name}"
EVENT_INVITE_BODY = 'Dear {guest_name},\n\nWe hope this email finds you well! We are excited to extend a warm invitation to you for our upcoming {event_name} taking place on {event_date} at {event_location}.\n\nHere are the event details:\n\n- Event Name: {event_name}\n- Date: {event_date}\n- Time: {event_time}\n- Address: {full_address}\n- Map Link: {map_link}\n\nTo secure your spot, please go to the following link for verification.\n{verification_link}\n\nWe encourage you to respond at your earliest convenience.\n\nWe hope to see you at the event and looking forward to welcoming you.\n\nBest regards'
EVENT_WA_INVITE_MESSAGE = """Dear {guest_name},\n\nWe're thrilled to extend an invitation to you for our upcoming event. Here are the key details:\n\nEvent Name: {event_name}\nDate: {event_date}\nTime: {event_time}\nLocation: {event_location}\nMap Link: {map_link}\nTo ensure your spot, kindly verify your attendance by visiting the following link: {verification_link}\n\nYour prompt response would be greatly appreciated. We eagerly anticipate your presence.\n\nThank you, and we hope to see you there!\n\nBest regards,"""

# Event Cancelled
EVENT_CANCELLED_SUBJECT = 'Subject: {event_name} - Cancellation Notice'
EVENT_CANCELLED_MAIL = 'Dear {guest_name},\n\nWe regret to inform you that the {event_name} on {event_date} with reference id {ref_id}, is canceled due to {reason}.\n\nWe apologize for any inconvenience this may cause and appreciate your understanding.\n\nThank you for your support.\n\nBest regards,\n{premise_name}'
