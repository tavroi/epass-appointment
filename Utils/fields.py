from Utils.return_message import *

FIELDS = {
    "mobile_no": {
        "errorMessage": INVALID.replace("{name}", "mobile no"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length": 13,
    },

    "on_whatsapp": {
        "errorMessage": INVALID.replace("{name}", "on_whatsapp"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-1",
        "Length": 2,
    },

    "otp": {
        "errorMessage": INVALID.replace("{name}", "OTP"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length": 5,
    },
     "visitor_id": {
        "errorMessage": INVALID.replace("{name}", "visitor id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "dept_id": {
        "errorMessage": INVALID.replace("{name}", "department id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "officer_id": {
        "errorMessage": INVALID.replace("{name}", "officer id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "purpose": {
        "errorMessage": INVALID.replace("{name}", "booking purpose") + ". Only alphanumerics or these symbols are allowed \n:@.!#$%&'*+-/=?^_`|",
        "DataType": "Varchar",
        "SymbolsAllowed":"\n:@.0987654321!#$%&'*+-/=?^_`|"  
        },
    "slot_id": {
        "errorMessage": INVALID.replace("{name}", "slot id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "office_id": {
        "errorMessage": INVALID.replace("{name}", "office id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "visitor_card": {
        "errorMessage": INVALID.replace("{name}", "visitor card url"),
        "DataType": "URL",
        },

    "state_id": {
        "errorMessage": INVALID.replace("{name}", "state id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },
    "district_id": {
        "errorMessage": INVALID.replace("{name}", "district id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "event_id": {
        "errorMessage": INVALID.replace("{name}", "event id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },
        

    "email_id":{"errorMessage": "Please specify valid email address. It must be of between 7-55 characters that can include @,/\- symbols.", 
        "DataType": "Varchar",
        "MinLength": 8,
        "MaxLength": 56,
        "SymbolsAllowed":"@.0987654321!#$%&'*+-/=?^_`{|"  
        },
    "designation": {
        "errorMessage": INVALID.replace("{name}", "designation"),
        "DataType": "Varchar",
        "SymbolsAllowed":"@.0987654321!#$%&'*+-/=?^_`{|" 
        },
     "organization_name": {
        "errorMessage": INVALID.replace("{name}", "organization name"),
        "DataType": "Varchar",
        "SymbolsAllowed":"@.0987654321!#$%&'*+-/=?^_`{|" 
        },
    "booking_type": {
        "errorMessage": INVALID.replace("{name}", "booking type"),
        "DataType": "Varchar",
        },

    "doc_type": {
        "errorMessage": INVALID.replace("{name}", "document type"),
        "DataType": "Varchar",
        },

    "gender": {
        "errorMessage": INVALID.replace("{name}", "gender"),
        "DataType": "Varchar"
        },

    "first_name": {
        "errorMessage": INVALID.replace("{name}", "first name"),
        "DataType": "All"
        },

    "last_name": {
        "errorMessage": INVALID.replace("{name}", "last name"),
        "DataType": "All"
        },

    "dob": {
        "errorMessage": INVALID.replace("{name}", "dob"),
        "DataType": "Varchar",
        "SymbolsAllowed": "-",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },

    "livliness_video_url": {
        "errorMessage": INVALID.replace("{name}", "livliness video url"),
        "DataType": "URL",
        },

    "doc_face_image": {
        "errorMessage": INVALID.replace("{name}", "document face image"),
        "DataType": "Varchar",
        "SymbolsAllowed":"@.0987654321!#$%&'*+-/=?^_`{|" 
        },

    "doc_image": {
        "errorMessage": INVALID.replace("{name}", "document image"),
        "DataType": "URL",
        },

    "id": {
        "errorMessage": INVALID.replace("{name}", "id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
        },
    "aadhar_captcha_generated": {
        "errorMessage": INVALID.replace("{name}", "aadhar captcha generated status"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length":2
        },
        

    "aadhar_kyc": {
        "errorMessage": INVALID.replace("{name}", "aadhar kyc status"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length":2
        },

    "aadhar_otp_generated": {
        "errorMessage": INVALID.replace("{name}", "aadhar otp generated status"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length":2
        },

    "aadhar_otp_verified": {
        "errorMessage": INVALID.replace("{name}", "aadhar otp verified status"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length":2
        },

    "is_verified": {
        "errorMessage": INVALID.replace("{name}", "is verified status"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9",
        "Length":2
        },

        
    

    
    "day": {
        "errorMessage": NOTIFICATION_DAY,
        "DataType": "Integer"
    },
    "template_id": {
        "errorMessage": INVALID_TEMPLATE,
        "DataType": "Varchar",
        "IngeterRange": "0-9",
        "MinLength": 3,
        "MaxLength": 50
    },
    "access_token": {
        "errorMessage": INVALID_WA_ACCESS_TOKEN,
        "DataType": "All"
    },
    "name": {
        "errorMessage": INVALID.replace("{name}", "name"),
        "DataType": "Varchar",
        "MinLength": 3,
        "MaxLength": 250
    },
    "detail_name": {
        "errorMessage": INVALID.replace("{name}", "detail name"),
        "DataType": "Varchar",
    },
    "insurance_id": {
        "errorMessage": INVALID.replace("{name}", "insurance id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "is_active": {
        "errorMessage": INVALID.replace("{name}", "is active"),
        "DataType": "Boolean"
    },
    "sequence": {
        "errorMessage": INVALID.replace("{name}", "Sequence"),
        "DataType": "Integer"
    },
    "category_id": {
        "errorMessage": INVALID.replace("{name}", "Category id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "insurer_id": {
        "errorMessage": INVALID.replace("{name}", "Insurer id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "v_number": {
        "errorMessage": INVALID.replace("{name}", "Vehicle number"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "customer_id": {
        "errorMessage": INVALID.replace("{name}", "Customer Id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "plan_id": {
        "errorMessage": INVALID.replace("{name}", "Plan Id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "is_ncb": {
        "errorMessage": INVALID.replace("{name}", "Is ncb"),
        "DataType": "Boolean"
    },
    "feature_id": {
        "errorMessage": INVALID.replace("{name}", "Feature Id"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "idv_min": {
        "errorMessage": INVALID.replace("{name}", "IDV min"),
        "DataType": "Integer"
    },
    "idv_expected": {
        "errorMessage": INVALID.replace("{name}", "IDV expected"),
        "DataType": "Integer"
    },
    "ncb_value": {
        "errorMessage": INVALID.replace("{name}", "NCB Value"),
        "DataType": "Integer"
    },
    "vehicle_number": {
        "errorMessage": INVALID.replace("{name}", "Vehicle number"),
        "DataType": "Varchar",
        "WithSpace": 0,
        "IngeterRange": "0-9"
    },
    "permanent_address": {
        "errorMessage": INVALID.replace("{name}", "Permanent Address"),
        "DataType": "Varchar",
        "WithSpace": 1,
        "IngeterRange": "0-9",
        "SymbolsAllowed": ","
    },
    "present_address": {
        "errorMessage": INVALID.replace("{name}", "Present Address"),
        "DataType": "Varchar",
        "WithSpace": 1,
        "IngeterRange": "0-9",
        "SymbolsAllowed": ","
    },
    "phone_number": {
        "errorMessage": INVALID.replace("{name}", "Phone Number"),
        "DataType": "MobileNumber"
    },
    "insurance_comp": {
        "errorMessage": INVALID.replace("{name}", "Insurance Company"),
        "DataType": "Varchar",
        "WithSpace": 1,
        "IngeterRange": "0-9",
        "SymbolsAllowed": "."
    },
    "insurance_upto": {
        "errorMessage": INVALID.replace("{name}", "Insurance Upto"),
        "DataType": "Varchar",
        "WithSpace": 1,
        "IngeterRange": "0-9",
        "SymbolsAllowed": "/"
    },
    "consent": {
        "errorMessage": INVALID.replace("{name}", "Consent"),
        "DataType": "Boolean",
    },
    "first_name":
        {"errorMessage": "Please specify valid first name. it must be between 2 to 30 characters", 
        "DataType": "All",
        "MinLength": 3,
        "MaxLength": 31},
    "last_name":
        {"errorMessage": "Please specify valid last name. it must be between 2 to 30 characters", 
        "DataType": "All",
        "MinLength": 3,
        "MaxLength": 31
        },
    "customer_name":
        {"errorMessage": "Please specify valid customer name. it must be between 2 to 60 characters", 
        "DataType": "Varchar",
        "MinLength": 3,
        "MaxLength": 61},

	"contact_no":{"errorMessage": "Please specify valid Contact no. it must be of 10 digits", 
        "DataType": "ContactNo_str",
        "Length": 11,
        
        },
	"address1":{"errorMessage": "Please specify valid Address 1. It must be of between 2-30 characters that can include @,/\- symbols.", 
        "DataType": "Varchar",
        "MinLength": 11,
        "MaxLength": 31,
		"SymbolsAllowed":"@,/\-0987654321"
        
        },
	"address2":{"errorMessage": "Please specify valid Address 2. It must be of between 2-30 characters that can include @,/\- symbols.", 
        "DataType": "Varchar",
        "MinLength": 11,
        "MaxLength": 31,
		"SymbolsAllowed":"@,/\-0987654321"
        
        },
	"address3":{"errorMessage": "Please specify valid Address 3. It must be of between 2-30 characters that can include @,/\- symbols.", 
        "DataType": "Varchar",
        "MinLength": 11,
        "MaxLength": 31,
		"SymbolsAllowed":"@,/\-0987654321"
        
        },
	"email":{"errorMessage": "Please specify valid email address. It must be of between 7-55 characters that can include @,/\- symbols.", 
	"DataType": "Varchar",
	"MinLength": 8,
	"MaxLength": 56,
	"SymbolsAllowed":"@.0987654321!#$%&'*+-/=?^_`{|"
	
	},

	"pan_no":{"errorMessage": "Please specify valid Pan No.", 
	"DataType": "PanNo"
	
	}



    
}
