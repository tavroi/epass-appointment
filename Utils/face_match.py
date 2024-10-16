import boto3, requests, os, inspect, traceback, base64
import time
from dotenv import load_dotenv

import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv(".env")

CREATED_CODE = 201
EXCEPTION_CODE = 500
USER_ERROR_MESSAGE = "An error occurred. Please try again"
NOT_FOUND_CODE = 404
READ_CODE = 200

FaceMatchThreshold = 85

def compare_faces_aws(face_from_machine, face_from_id):
    try:
        rec_client = boto3.client('rekognition', 
                                        region_name=os.getenv('REGION_NAME'), 
                                        aws_access_key_id=os.getenv("S3_KEY"),
                                        aws_secret_access_key=os.getenv("S3_SECRET"))
        
        response = rec_client.compare_faces(SimilarityThreshold=FaceMatchThreshold,
                                        SourceImage={'Bytes': base64.b64decode(face_from_machine)},
                                        TargetImage={'Bytes': base64.b64decode(face_from_id)})
        
        logger.info(f"response from aws: {response}")
        if len(response.get('FaceMatches',[])):
            return True, response['FaceMatches'][0]['Similarity'], response 
        return False, 0.00, response
    except Exception as e:
        logger.info(f"Error from aws: {e.__str__()}")
        logger.error(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                     f"Method-Name: compare_faces_aws")
        return False, 0.00, {}
    

# compare_faces_aws(base64.b64decode("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"),
#                   base64.b64decode("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"))






class AWSFaceMatch:

    def __init__(self) -> None:
        self.client = boto3.client('rekognition', region_name=os.getenv('REGION_NAME'), 
                                   aws_access_key_id=os.getenv("S3_KEY"), aws_secret_access_key=os.getenv("S3_SECRET"))
        self.S3_BUCKET = os.getenv("S3_BUCKET")
        self.S3_KEY = os.getenv("S3_KEY")
        self.S3_SECRET = os.getenv("S3_SECRET")
        self.S3_LOCATION = os.getenv("S3_LOCATION")
        self.REGION_NAME = os.getenv('REGION_NAME')

    def upload_file_aws(self, byte_data, file_name, mime_type=None, bucket_address=None):
        try:
            client = boto3.client('s3', region_name=self.REGION_NAME, aws_access_key_id=self.S3_KEY, aws_secret_access_key=self.S3_SECRET)
            print(f"UPLOAD_SERVICE:: AWS S3")
            print(f"S3 Secret: {self.S3_SECRET}, S3 Key: {self.S3_KEY}, S3Bucket: {self.S3_BUCKET}, S3 Location: {self.S3_LOCATION}")
            
            fields = {'acl': 'public-read'}
            conditions = [{"acl": "public-read"}]
            if mime_type:
                fields['Content-Type'] = mime_type
                conditions.append({"Content-Type": mime_type})
                
            buc_address = file_name if not bucket_address else bucket_address + file_name
            boto3_response = client.generate_presigned_post(Bucket=self.S3_BUCKET, Key=buc_address, Fields=fields,
                                                            ExpiresIn=60, Conditions=conditions)
            
            print(f"Boto3 response for Broadcast: {boto3_response}, File-Name: {os.path.basename(__file__)}, "
                  f"Method-Name: {inspect.stack()[0][3]}")
            print(20 * "####")
            
            files = {'file': (file_name, byte_data)}
            data = boto3_response['fields']
            r = requests.post(boto3_response['url'], data=data, files=files)
            
            # print(r.status_code)
            # print(r.text)
            
            file_url = self.S3_LOCATION + buc_address
            return {"data": file_url, "message": "File Uploaded Successfully.", "status": True}
        except Exception as e:
            print(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                  f"Method-Name: {inspect.stack()[0][3]}")
            print(20 * "####")
            return {"message": "Something Went Wrong!", "errorMessage": str(e), "status": False}

    def create_collection(self, collection_id):
        print('Creating collection:' + collection_id)
        response = self.client.create_collection(CollectionId=collection_id)
        if response.get("StatusCode") == 200:
            return {"status": True, 'data': {"arn": response['CollectionArn']}, "code": CREATED_CODE, 
                    "message": "Face Collection Created", "errorMessage": ""}
        
        return {"status": False, 'data': {}, "code": EXCEPTION_CODE, "message": USER_ERROR_MESSAGE, "errorMessage": "Failed to create face collection"}

    def add_faces_to_collection(self, visitor_id, image_base64, collection_id="ePassFacesCollection"):
        image_bytes = base64.b64decode(image_base64)
        file_name = f"ePass/faceCollection/{visitor_id}"
        upload_response = self.upload_file_aws(byte_data=image_bytes, file_name=file_name)
        if not upload_response["status"]:
            return {"status": False, 'data': {}, "code": EXCEPTION_CODE, "message": USER_ERROR_MESSAGE, "errorMessage": "Failed to upload file to S3"}
        
        response = self.client.index_faces(CollectionId=collection_id, Image={'S3Object': {'Bucket': self.S3_BUCKET, 'Name': file_name}},
                                           ExternalImageId=visitor_id, MaxFaces=1, QualityFilter="AUTO", DetectionAttributes=['ALL'])
        # print("ADD RESPONSE: ", res)
        return {"status": True, 'data': {"face_collection_size": len(response['FaceRecords'])}, "code": CREATED_CODE, "message": "Face Uploaded to the Collections", "errorMessage": ""}
    
    def match_face_from_collection(self, image_base64, collection_id="ePassFacesCollection", max_faces=1):
        try:
            image_bytes = base64.b64decode(image_base64)
            file_name = f"ePass/faceMatches/{int(time.time())}"
            upload_response = self.upload_file_aws(byte_data=image_bytes, file_name=file_name)
            print("UPLOAD REPONSE %s", upload_response,collection_id)
            if not upload_response["status"]:
                return {"status": False, 'data': {}, "code": EXCEPTION_CODE, "message": USER_ERROR_MESSAGE, "errorMessage": "Failed to upload file to S3"}

            response = self.client.search_faces_by_image(CollectionId=collection_id, Image={'S3Object': {'Bucket': self.S3_BUCKET, 'Name': file_name}},
                                                        FaceMatchThreshold=FaceMatchThreshold, MaxFaces=max_faces)
            
            matching_face = response['FaceMatches'][0] if len(response.get("FaceMatches", [])) > 0 else {}
            print("FACEMATCH REPONSE %s", response)

            if matching_face:
                return {"status": True, 'data': {"visitor_id": matching_face['Face']['ExternalImageId']}, 
                        "code": READ_CODE, "message": "Face Match Found", "errorMessage": ""}
            
            return {"status": False, 'data': {}, "code": NOT_FOUND_CODE, "message": "No Face Match Found", "errorMessage": "Face Match not Found"}
        except Exception as e:
            return {"status": False, 'data': {}, "code": NOT_FOUND_CODE, "message": "No Face Match Found", "errorMessage": "Face Match not Found"}
        

    def clear_collection(self, collection_id='ePassFacesCollection'):
        try:
            response = self.client.list_faces(CollectionId=collection_id)
            face_ids = [face['FaceId'] for face in response.get('Faces', [])]

            while 'NextToken' in response:
                response = self.client.list_faces(CollectionId=collection_id, NextToken=response['NextToken'])
                face_ids.extend([face['FaceId'] for face in response.get('Faces', [])])

            if not face_ids:
                return {"status": True, "message": "No faces to delete", "errorMessage": ""}

            delete_response = self.client.delete_faces(CollectionId=collection_id, FaceIds=face_ids)

            return {
                "status": True,
                "data": {"deleted_faces": delete_response['DeletedFaces']},
                "message": "Faces deleted successfully from the collection",
                "errorMessage": ""
            }
        except Exception as e:
            print(f"Exception Message: {traceback.print_exc()}, File-Name: {os.path.basename(__file__)}, "
                  f"Method-Name: {inspect.stack()[0][3]}")
            print(20 * "####")
            return {"status": False, "message": "Failed to clear the collection", "errorMessage": str(e)}