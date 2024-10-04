import requests
import datetime, time
from Utils.config import *
from Utils.validate_mandatory import *


def compare_details(dict1, dict2, keys):
    differences = {}
    for key in keys:
        if key in dict1 and key in dict2:
            if dict1[key] != dict2[key]:
                differences[key] = {'from': dict1[key], 'to': dict2[key]}
        elif key in dict1:
            differences[key] = {'from': dict1[key], 'to': None}
        elif key in dict2:
            differences[key] = {'from': None, 'to': dict2[key]}

    if differences=={}:
        return True
    else:
        return False
    # return differences

# dict1 = {'a': 1, 'b': 2, 'c': 3}
# dict2 = {'a': 1, 'b': 22, 'd': 3}

# # Specify the keys you want to compare
# keys_to_compare = ['a', 'b', 'c']

# # Get the differences
# diffs = compare_specific_keys(dict1, dict2, keys_to_compare)
# print(diffs)

def fncValidateData(Data, MadatoryFields, FieldsDetail):
    message = {"Result": 1}
    for Key, Value in Data.items():
        if type(Value) == dict:
            message[Key] = fncValidate(Value, MadatoryFields[Key], FieldsDetail)
        elif type(Value) == list:
            for x in range(len(Value)):
                validation_result = fncValidate(Value[x], MadatoryFields[Key][0], FieldsDetail)
                if validation_result["Result"] == 0:
                    message["Result"] = 0
                    del validation_result["Result"]
                    if message.get(Key, None) is None:
                        message[Key] = []
                    message[Key].append(fncFormatErrorMessage(validation_result, Value[x], x))
        elif type(Value) == bool:
            validation_message = fncValidateBooleanField(Key, FieldsDetail)
            if validation_message["Result"] == 0:
                message[Key] = validation_message["errorMessage"]
                message["Result"] = 0
        else:
            if str(Value).strip() != "":
                validation_message = fncValidateField(Key, str(Value).strip(), FieldsDetail)
                if validation_message["Result"] == 0:
                    message[Key] = validation_message["errorMessage"]
                    message["Result"] = 0
            else:
                if MadatoryFields[Key]:
                    message[Key] = (fncFormatName(Key) + " cannot be blank.").replace("_"," ").replace("  "," ")
                    message["Result"] = 0
    return message

def fncValidate(Data, MadatoryFields, FieldsDetail):
    ValidationResult = checkMissingFields(Data, MadatoryFields)
    if len(ValidationResult) > 0:
        ValidationResult.update({"Result": 0})
        return ValidationResult
    validation_result = fncValidateData(Data, MadatoryFields, FieldsDetail)
    return validation_result

