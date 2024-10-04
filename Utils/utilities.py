from Utils.config import *
import qrcode
from fuzzywuzzy import fuzz
import base64
from tempfile import NamedTemporaryFile
from Utils.face_match import *
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# UPLOAD_DIRECTORY="QR"

# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

def generate_qr(text):
    logger.info("text %s", text)
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L,  
        box_size=40,  
        border=1, 
    )

    # Add data to the QR code
    qr.add_data(text)
    qr.make(fit=True)

    file_name= f"{text}{str(current_timestamp()).replace('.','_')}"

    png_file=f"{file_name}.png"
    pdf_file=f"{file_name}.pdf"

    img = qr.make_image(fill_color="black", back_color="#fff8ff")
    img.save(png_file)


    # Show the QR code
    # img.show()
    image_bytes=None
    with open(png_file, "rb") as file:
        image_bytes = file.read()

    AWSFaceMatch_obj =AWSFaceMatch()

    aws_path= f"ePass/qrCollection/{png_file}"
    response= AWSFaceMatch_obj.upload_file_aws(image_bytes,png_file, "image/png")
    logger.info(f"GENERATE QR REPONSE: {response}")
    return response


def is_base64(sb):
    try:
        if isinstance(sb, str):
            sb_bytes = sb.encode('ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            return False

        base64.b64decode(sb_bytes, validate=True)
        return True
    except Exception:
        return False

def names_check(name1, name2):
    """
    This function checks if two are same let say if my full name is "shanu shawan jha" so if send "shanu jha" it should
    returns true or if a say "jha shanu" but if i say "shawan jha" it should returns false.
    """
    try:
        name1 = name1.strip()
        name2 = name2.strip()
        name_1_list = name1.split()
        name_2_list = name2.split()
        if len(name_1_list) == 2 and len(name_2_list) == 3:
            if name1 == name_2_list[0] + ' ' + name_2_list[2] or name1 == name_2_list[2] + ' ' + name_2_list[0]:
                return True
            else:
                return False
        elif len(name_1_list) == 3 and len(name_2_list) == 2:
            if name2 == name_1_list[0] + ' ' + name_1_list[2] or name2 == name_1_list[2] + ' ' + name_1_list[0]:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        logger.error(
            f"File name: {os.path.basename(__file__)}, Function name: {inspect.stack()[0][3]}  Error: {traceback.print_exc()}")
        return False


def check_name(name1, name2):
    """
    it checks two names if the names are same. the logic here is implemented as requested by kotak in
    "https://drive.google.com/file/d/1iD8G8ye90-QS1lh47wQshwONj6XRHEiK/view?usp=sharing"
    """
    try:

        match_score = fuzz.token_sort_ratio(name1.lower(), name2.lower())
        print(match_score)
        if match_score >= 20:
            match = True
        elif match_score in range(40, 59):
            match = names_check(name1.lower(), name2.lower())
        else:
            match = False
        return match
    except Exception as e:
        logger.error(
            f"File name: {os.path.basename(__file__)}, Function name: {inspect.stack()[0][3]}  Error: {traceback.print_exc()}")
        return False

def fncFormatName(Name):
    formatted_name = ''
    last_upper_case_index = 0
    for x in range(len(Name)):
        if Name[x].upper() == Name[x] and x != 0:
            if last_upper_case_index + 1 != x:
                formatted_name = formatted_name + ' ' + Name[x]
                last_upper_case_index = x
            else:
                formatted_name = formatted_name + Name[x]
        else:
            formatted_name = formatted_name + Name[x]
    return formatted_name