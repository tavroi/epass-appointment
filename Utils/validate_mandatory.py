import re
import requests

from Utils.utilities import fncFormatName
from Utils.sanitation import validate_date


def fncGetRegex(FieldDetails):
    regex_for_data_type = {
        "Varchar": "^[A-Za-z 0-9]*$",
        "Char": "^[^\s][A-Za-z ]*$",
        "Integer": "^[0-9][0-9]*$",
        "CountryCode": "^[0-9][0-9]{1,3}$",
        "MobileNumber": "^[0-9][0-9]{5,15}$",
        "EmailID": "^[A-Za-z0-9-.]+[\._]?[A-Za-z0-9-.]+[@]\w+[.]\w{2,3}$",
        "All": "",
        "URL":"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

    }
    regex = regex_for_data_type.get(FieldDetails["DataType"], '')
    if FieldDetails["DataType"] in ["Varchar", "Integer", "Char"]:
        if FieldDetails.get('Length', None) is not None:
            regex = regex.replace('*', "{" + str(FieldDetails["Length"] - 1) + "}")
        if FieldDetails.get('IngeterRange', None) is not None:
            regex = regex.replace('0-9', FieldDetails["IngeterRange"])
        if FieldDetails.get('Prefix', None) is not None:
            regex = FieldDetails["Prefix"] + regex[1:]
        if FieldDetails.get('Suffix', None) is not None:
            regex = regex.replace('$', FieldDetails["Suffix"] + "$")
        if FieldDetails.get('WithSpace', None) == 0:
            regex = regex.replace(' ', '').replace('[^\s]', '')
        if FieldDetails.get('SymbolsAllowed', None) is not None:
            if FieldDetails["DataType"] in ["Varchar", "Char"]:
                regex = regex.replace('A-Z', 'A-Z' + FieldDetails["SymbolsAllowed"])
            else:
                regex = regex.replace('0-9', '0-9' + FieldDetails["SymbolsAllowed"])
        if FieldDetails.get('MinLength', None) is not None and FieldDetails.get('MaxLength', None) is not None:
            regex = regex.replace('*', "{" + str(FieldDetails["MinLength"] - 1) + "," + str(
                FieldDetails["MaxLength"] - 1) + "}")
        else:
            if FieldDetails.get('MinLength', None) is not None:
                regex = regex.replace('*', "{" + str(FieldDetails["MinLength"] - 1) + ",}")
            if FieldDetails.get('MaxLength', None) is not None:
                regex = regex.replace('*', "{," + str(FieldDetails["MaxLength"] - 1) + "}")
    return regex


# Length, MaxLength, MinLegth, WithSpace, Prefix, Suffix


def fncGetErrorMessagesAndRegex(FieldName, FieldsDetail):
    error_message_and_regex = FieldsDetail.get(
        FieldName,
        {"errorMessage": "Please Specify a Valid " + fncFormatName(FieldName), "DataType": "All"}
    )
    return error_message_and_regex


def fncFormatErrorMessage(ValidationMessages, RequestData, RowNo):
    error_messages = {}
    for field_name, error_message in ValidationMessages.items():
        error_message = error_message[:-1] + ' for Passenger 0' + str(RowNo + 1)
        if field_name == 'TicketNo':
            error_message = error_message + " with Booking Code " + RequestData.get("BookingCode", '-') + "."
        else:
            error_message = error_message + " with Ticket number " + RequestData.get("TicketNo", '-') + "."
        error_messages[field_name] = error_message
    return error_messages


def fncValidateField(FieldName, FieldValue, FieldsDetail):
    error_message_and_regex = fncGetErrorMessagesAndRegex(FieldName, FieldsDetail)
    # print(f" data \n {str(FieldName)}, {str(FieldsDetail)} {str(error_message_and_regex)} ")
    if error_message_and_regex["DataType"] == "Dropdown":
        return {"Result": 1}
    elif error_message_and_regex['DataType'] == "Url":
        validate_url = fncValidateURLField(FieldName, FieldValue, FieldsDetail)
        return validate_url
    elif error_message_and_regex['DataType'] in ["Date", "DateTime"]:
        validate_obj = validate_date(FieldValue, error_message_and_regex['Format'])
        if not validate_obj['status']:
            return {"Result": 0, "errorMessage": error_message_and_regex["errorMessage"]}
        return {"Result": 1}
    else:
        if re.match(fncGetRegex(error_message_and_regex), str(FieldValue)):
            return {"Result": 1}
        else:
            return {"Result": 0, "errorMessage": error_message_and_regex["errorMessage"]}


def fncValidateBooleanField(key, FieldsDetail):
    validation_message = {"Result": 0}
    if not FieldsDetail.get(key):
        validation_message['errorMessage'] = "Please Specify a Valid "+key
    else:
        if FieldsDetail[key]['DataType'] == 'Boolean':
            validation_message['Result'] = 1
        else:
            validation_message['errorMessage'] = FieldsDetail['errorMessage']
    return validation_message


def fncValidateURLField(FieldKey, FieldValue, FieldsDetail):
    # validate url is on internet or not.
    try:
        response = requests.get(FieldValue)
        if response.status_code not in [200, 201]:
            return {"Result": 0, "errorMessage": f"Request url status code is {response.status_code}"}
        if FieldsDetail[FieldKey].get("FileType", None):
            file_type = FieldValue.split(".")[-1].lower()
            if file_type != FieldsDetail[FieldKey]['FileType']:
                return {"Result": 0, "errorMessage": FieldsDetail[FieldKey]['fileTypeErrorMessage']}
        return {"Result": 1}
    except requests.ConnectionError as exception:
        return {"Result": 0, "errorMessage": FieldsDetail[FieldKey]['connectionErrorMessage']}


def fncValidate(Data, MadatoryFields, FieldsDetail):
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
                    message[Key] = fncFormatName(Key) + " cannot be blank."
                    message["Result"] = 0
    return message


def fncCheckDublicateTicketNo(RequestData):
    message = {"Result": 1}
    ticket_nos = []
    for Passenger in RequestData["PassengersDetails"]:
        if Passenger["TicketNo"] in ticket_nos:
            return {"Result": 0, "TicketNo": "Dublicate Ticket no."}
        else:
            ticket_nos.append(Passenger["TicketNo"])
    return message


def fncGetErrorMessagesList(ValidationMessages):
    error_messages = []
    for Key, Value in ValidationMessages.items():
        data_type = type(Value)
        if data_type == list:
            for x in ValidationMessages[Key]:
                error_messages = error_messages + fncGetErrorMessagesList(x)
        elif data_type == dict:
            error_messages = error_messages + fncGetErrorMessagesList(Value)
        else:
            if Key != "Result":
                error_messages.append(Value)
    return error_messages


def fncValidateRequestData(RequestData, MadatoryFields, FieldsDetail):
    ValidationResult = checkMissingFields(RequestData, MadatoryFields)
    if len(ValidationResult) > 0:
        ValidationResult.update({"Result": 0})
        return ValidationResult
    validation_result = fncValidate(RequestData, MadatoryFields , FieldsDetail)
    # dublicate_ticket_no_check_result = fncCheckDublicateTicketNo(RequestData)
    # if validation_result["Result"] == 1 and dublicate_ticket_no_check_result["Result"] == 1:
    #     validation_result["Result"] = 1
    # else:
    #     validation_result.update(dublicate_ticket_no_check_result)
    #     validation_result["Result"] = 0
    #     validation_result["errorMessages"] = fncGetErrorMessagesList(validation_result)
    return validation_result


def filterDictionary(pdicToBeComparedWith):
    FilteredDictionary = {}
    for k, v in pdicToBeComparedWith.items():
        if v == True:
            FilteredDictionary.update({k: v})
        if type(v) == list:
            for x in v:
                Result = filterDictionary(x)
                if len(Result) > 0:
                    FilteredDictionary.update({k: []})
                    FilteredDictionary[k].append(Result)
    return FilteredDictionary


def performComparison(pdicToBeCompared, pdicToBeComparedWith, row=""):
    return [{fields: fields + " is missing" + str(row)} for fields in
            set(list(pdicToBeComparedWith.keys())) - set(list(pdicToBeCompared.keys()))]


def checkMissingFields(pdicToBeCompared, pdicToBeComparedWith):
    pdicToBeComparedWith = filterDictionary(pdicToBeComparedWith)
    Result = []
    Result.append(performComparison(pdicToBeCompared, pdicToBeComparedWith, row=""))
    for Key, Value in pdicToBeCompared.items():
        if type(Value) == dict:
            Result.append(performComparison(pdicToBeCompared, pdicToBeComparedWith))

        elif type(Value) == list:
            for x in range(len(Value)):
                try:
                    Result.append(
                        performComparison(Value[x], pdicToBeComparedWith[Key][0], row=" for row no: " + str(x + 1)))
                except:
                    pass

    FinalResult = []

    for i in Result:
        for x in i:
            for y, z in x.items():
                FinalResult.append({y: z})

    FormattedData = {}
    for i in FinalResult:
        FormattedData.update(i)
    return FormattedData


