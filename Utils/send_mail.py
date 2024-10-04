import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from email.mime.base import MIMEBase
from email import encoders
import requests
from Utils.config import *

class EmailUtility:
    EmailId = "digipass@verismart.ai"
    EmailPassword = "ojqi znvw lbyd dfzx"
    MailServer = "smtp.gmail.com,587"
    EnableEmail = True
#
    # EmailId = 'amit.sharma@verismart.ai'  
    # EmailPassword = 'bigx jwrt vsja elrv'  
    # MailServer = 'smtp.gmail.com,587'  

    @staticmethod
    def SendEmailToDistrictUser(e, EmailIds,event_id,type_id,name,campaing_type,campaing_id:Optional[str]=" "):
        email_attributes = {}  # Should be a dictionary
    # Pass the correct type to GetEmailAttributes
        EmailUtility.GetEmailAttributes(email_attributes)
        r = {"status": False, "message": []}
        if EmailUtility.EnableEmail:
            ee = EmailUtility.GetEmailAttributes(email_attributes)
            print(ee)
            if ee:
                try:
                    smtp_host = ee["MailServer"]
                    smpt_mailid_from = ee["SenderEmail_Id"]
                    smpt_username = ee["SenderEmail_Id"]
                    smpt_password = ee["SenderPassword"]
                    smpt_port = int(ee["MailServerPort"])
                    image_path=e.get('image_link')

                    msg = MIMEMultipart()
                    msg['From'] = smpt_mailid_from
                    msg['To'] = ", ".join(EmailIds)
                    msg['Subject'] = e["subject"]
                    msg.attach(MIMEText(e["message"], 'plain'))
                    print(f"msg: {msg}")
                    if image_path:
                        
                        # Download the image file
                        response = requests.get(image_path)
                        if response.status_code == 200:
                            image_data = response.content
                            image_name = image_path.split("/")[-1]

                            # Create a MIMEBase object for the image
                            mime_base = MIMEBase('application', 'octet-stream')
                            mime_base.set_payload(image_data)
                            encoders.encode_base64(mime_base)
                            mime_base.add_header('Content-Disposition', f'attachment; filename={image_name}')
                            msg.attach(mime_base)
                        else:
                            print(f"Failed to download image. HTTP status code: {response.status_code}")
                            # return
                    smtp = smtplib.SMTP(smtp_host, smpt_port)
                    smtp.starttls()
                    print("try login")
                    smtp.login(smpt_username, smpt_password)
                    print("logged in sending email")
                    smtp.sendmail(smpt_mailid_from, EmailIds, msg.as_string())
                    print("email sent")
                    smtp.quit()
                    
                    r["status"] = True
                    r["message"] = "Email sent successfully!"
                except Exception as ex:
                    print(ex.__str__())
                    import traceback
                    print(traceback.print_exc())
                    r["message"] = "Something went wrong, Please contact Administration!"
            else:
                r["message"] = "Email Service configuration not found."
        else:
            r["message"] = "Email Service is currently disabled, Please enable it from Configuration Setting."
        email_invites_id =unique_id()

        # Emails=EmailIds.split(',')
        for item in EmailIds:
            db.broadcast_list.insert_one(
                            {"_id": email_invites_id,
                            "name":name,
                            "email": item,
                            "mobile": "",
                            "created_at": current_timestamp(),
                            "message_status": r['status'],
                            "response":r ,
                            "message_payload":e,
                            "message_type": type_id,
                            "campaing_type": campaing_type,
                            "channel":"email",
                            "campaing_id":campaing_id,
                            "event_id":event_id
                            }
                        )
        return r

    @staticmethod
    def GetEmailAttributes(e):
        if not isinstance(e, dict):
            raise ValueError("Expected a dictionary for email attributes")
        e["MailServer"] = EmailUtility.MailServer.split(',')[0]
        e["MailServerPort"] = EmailUtility.MailServer.split(',')[1]
        e["SenderEmail_Id"] = EmailUtility.EmailId
        e["SenderPassword"] = EmailUtility.EmailPassword
        return e if e else None


# def send_notification_on_email(data):
#     result = EmailUtility.SendEmailToDistrictUser(data, [data["recipient"]])
#     update_record(id=data["id"], status=result["status"], job_status="finished" if result["status"] else "failed", message=result.get("message", ""))
#     return result

# print(send_notification_on_email({
#         "recipient": "shanu@verismart.ai",
#         "subject": "Test Email",
#         "message": "Hello, this is a test email!"
#     }))


