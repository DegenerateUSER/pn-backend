import jwt
from datetime import datetime
from django.conf import settings
import boto3
from decouple import config
from .models import *
from django.core.mail import send_mail
from urllib.parse import urlparse
from botocore.exceptions import ClientError
import os

def generate_jwt_tokens(user):
    access_payload = {
        'user_id': user.id,
        'exp': datetime.now() + settings.JWT_ACCESS_TOKEN_LIFETIME,
    }
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return access_token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        return payload
    except Exception as e:
        print("error", e)
        return None


def get_user_from_token(token):
    payload = decode_jwt_token(token)
    print("payload:", payload)
    if payload:
        try:
            user = User.objects.get(id=payload['user_id'])
            print("user:", User)
            return user
        except User.DoesNotExist:
            return None
    return None


def test_ses_connection():
    """Test SES connection and configuration"""
    
    try:
        # Test 1: Check AWS credentials
        print("🔍 Testing AWS SES connection...")
        
        client = boto3.client(
            'ses',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_REGION', default='eu-north-1')
        )
        
        # Test 2: Check SES service connectivity
        response = client.get_send_statistics()
        print("✅ AWS SES connection successful!")
        
        # Test 3: Check verified identities
        verified_emails = client.list_verified_email_addresses()
        print(f"📧 Verified emails: {verified_emails['VerifiedEmailAddresses']}")
        
        # Test 4: Check sending quota
        quota = client.get_send_quota()
        print(f"📊 Send quota: {quota['Max24HourSend']} emails/day, Rate: {quota['MaxSendRate']}/second")
        
        # Test 5: Try sending a test email
        from_email = config('DEFAULT_FROM_EMAIL', default='mayank9178@gmail.com')
        
        if from_email in verified_emails['VerifiedEmailAddresses']:
            print(f"✅ From email {from_email} is verified")
            
            # Send test email
            test_response = client.send_email(
                Source=from_email,
                Destination={'ToAddresses': [from_email]},  # Send to yourself
                Message={
                    'Subject': {'Data': 'SES Test Email'},
                    'Body': {'Text': {'Data': 'This is a test email from AWS SES via boto3'}}
                }
            )
            print(f"✅ Test email sent! Message ID: {test_response['MessageId']}")
        else:
            print(f"❌ From email {from_email} is NOT verified in SES")
            print("Please verify your email in AWS SES console first")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
        # Common error solutions
        if "InvalidClientTokenId" in str(e):
            print("🔧 Fix: Check your AWS_ACCESS_KEY_ID in .env file")
        elif "SignatureDoesNotMatch" in str(e):
            print("🔧 Fix: Check your AWS_SECRET_ACCESS_KEY in .env file")
        elif "is not authorized to perform: ses:SendEmail" in str(e):
            print("🔧 Fix: Your IAM user needs SES permissions")
        elif "Email address not verified" in str(e):
            print("🔧 Fix: Verify your email address in AWS SES console")
        elif "Connection refused" in str(e):
            print("🔧 Fix: Check internet connection or try different region")
            
            
def test_django_email():
    """Test Django email sending"""
    
    print("🔍 Testing Django email configuration...")
    print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
    print(f"🌍 AWS Region: {getattr(settings, 'AWS_REGION_NAME', 'Not set')}")
    print(f"📤 From email: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        # Send test email
        result = send_mail(
            subject='Django SES Test',
            message='This is a test email from Django using AWS SES',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Send to yourself
            fail_silently=False
        )
        
        if result:
            print("✅ Django email sent successfully!")
        else:
            print("❌ Django email sending failed")
            
    except Exception as e:
        print(f"❌ Django email error: {str(e)}")
        

# def delete_all_objects_from_s3_folder(bucket_url, folder_name):
#     """
#     This function deletes all files in a folder from S3 bucket
#     :return: None
#     """
#     s3_client = boto3.client("s3")

#     parsed_url = urlparse(bucket_url)
#     bucket_name = parsed_url.netloc
    
#     folder_to_delete = f'{parsed_url.path[1:]}{folder_name}' # append base folder of bucket url

#     # First we list all files in folder
#     response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_to_delete)
#     if "Contents" in response.keys():
#         files_in_folder = response["Contents"]

#         files_to_delete = []
#         # We will create Key array to pass to delete_objects function
#         for f in files_in_folder:
#             files_to_delete.append({"Key": f["Key"]})
#             print(f'Delete: {f["Key"]}')
#         # This will delete all files in a folder
#         response = s3_client.delete_objects(Bucket=bucket_name, 
#                                             Delete={"Objects": files_to_delete}
#                                             )
#         print(response)

# def create_presigned_url(s3_client, bucket_url, object_name, expiration=os.getenv('PRESIGNED_URL_EXPIRATION_TIME')):
#     """Generate a presigned URL to share an S3 object

#     :param bucket_name: string
#     :param object_name: string
#     :param expiration: Time in seconds for the presigned URL to remain valid
#     :return: Presigned URL as string. If error, returns None.
#     """

#     parsed_url = urlparse(bucket_url)
#     bucket_name = parsed_url.netloc
    
#     object_name = f'{parsed_url.path[1:]}{object_name}'
#     try:
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': bucket_name,
#                                                             'Key': object_name},
#                                                     ExpiresIn=expiration)
#     except ClientError as e:
#         print(e)
#         return None

#     # The response contains the presigned URL
#     return response

# def get_url_list(s3_client, bucket_url, evidence_id, folder, extension, number):
#     urls = []
#     for i in range(number):
#         object_name = f'{evidence_id}/{folder}/{i}{extension}'
#         urls.append(create_presigned_url(s3_client, bucket_url, object_name))
#     urls = [i for i in urls if i is not None]
#     return urls


class AssessmentS3Handler:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def create_presigned_url(self, object_key, content_type='application/octet-stream', expiration=None):
        """Generate a presigned URL to share an S3 object
        
        :param object_key: S3 object key (e.g., 'assessments/1/test.png')
        :param content_type: MIME type of the file
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        if expiration is None:
            expiration = int(os.getenv('PRESIGNED_URL_EXPIRATION_TIME', 3600))
        
        try:
            response = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,  # Use the bucket name directly
                    'Key': object_key,  # Use the object key directly
                    'ContentType': content_type
                },
                ExpiresIn=expiration
            )
            return response, object_key
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None, None
    
    def check_file_exists_and_size(self, object_key):
        """Check if file exists in S3 and return its size
        
        :param object_key: S3 object key
        :return: File size in bytes if exists, None if doesn't exist
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response['ContentLength']
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None  # File doesn't exist
            else:
                print(f"Error checking file: {e}")
                return None
    
    def generate_assessment_presigned_url(self, assessment_id, filename, content_type=None):
        """Generate presigned URL for assessment file upload"""
        # Create S3 key directly - no need for full URL construction
        s3_key = f"assessments/{assessment_id}/{filename}"
        
        # Detect content type if not provided
        if content_type is None:
            import mimetypes
            content_type, _ = mimetypes.guess_type(filename)
            if not content_type:
                content_type = 'application/octet-stream'
        
        return self.create_presigned_url(s3_key, content_type)


class ProctoringDynamoDBHandler:
    """Handler for AWS DynamoDB operations related to proctoring results"""
    
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name='eu-central-1',  # Specific region for the ProctoringResults table
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
        )
        self.table_name = 'ProctoringResults'
        self.table = self.dynamodb.Table(self.table_name)
    
    def get_all_proctoring_results(self):
        """Retrieve all items from the ProctoringResults table"""
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            
            # Handle pagination if there are more items
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response.get('Items', []))
            
            # Transform items to include the specific fields the user wants
            transformed_items = self._transform_items(items)
            
            return {
                'success': True,
                'data': transformed_items,
                'count': len(transformed_items)
            }
        except ClientError as e:
            return {
                'success': False,
                'error': f"DynamoDB client error: {e.response['Error']['Message']}",
                'error_code': e.response['Error']['Code']
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def get_proctoring_result_by_session_id(self, session_id):
        """Retrieve a specific proctoring result by SessionID"""
        try:
            response = self.table.get_item(
                Key={'SessionID': session_id}  # Using SessionID as the primary key
            )
            
            if 'Item' in response:
                transformed_item = self._transform_item(response['Item'])
                return {
                    'success': True,
                    'data': transformed_item
                }
            else:
                return {
                    'success': False,
                    'error': 'Item not found'
                }
        except ClientError as e:
            return {
                'success': False,
                'error': f"DynamoDB client error: {e.response['Error']['Message']}",
                'error_code': e.response['Error']['Code']
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def query_proctoring_results_by_filter(self, filter_params=None):
        """Query proctoring results with optional filters"""
        try:
            scan_kwargs = {}
            
            if filter_params:
                # Build FilterExpression based on provided parameters
                filter_expressions = []
                expression_attribute_values = {}
                expression_attribute_names = {}
                
                for key, value in filter_params.items():
                    if value is not None:
                        if key == 'session_id':
                            filter_expressions.append("SessionID = :session_id")
                            expression_attribute_values[':session_id'] = value
                        elif key == 'risk_score':
                            # RiskScore can be stored as string or Decimal
                            filter_expressions.append("RiskScore = :risk_score")
                            from decimal import Decimal
                            expression_attribute_values[':risk_score'] = Decimal(str(value))
                        elif key == 'min_risk_score':
                            # For numeric comparison, we need to use attribute names
                            filter_expressions.append("#risk_score >= :min_risk_score")
                            expression_attribute_names['#risk_score'] = 'RiskScore'
                            from decimal import Decimal
                            expression_attribute_values[':min_risk_score'] = Decimal(str(value))
                        elif key == 'max_risk_score':
                            filter_expressions.append("#risk_score <= :max_risk_score")
                            expression_attribute_names['#risk_score'] = 'RiskScore'
                            from decimal import Decimal
                            expression_attribute_values[':max_risk_score'] = Decimal(str(value))
                        elif key == 'start_date':
                            filter_expressions.append("#timestamp >= :start_date")
                            expression_attribute_names['#timestamp'] = 'Timestamp'
                            expression_attribute_values[':start_date'] = value
                        elif key == 'end_date':
                            filter_expressions.append("#timestamp <= :end_date")
                            expression_attribute_names['#timestamp'] = 'Timestamp'
                            expression_attribute_values[':end_date'] = value
                        elif key == 'has_flags':
                            # Check if Flags array is not empty
                            filter_expressions.append("size(Flags) > :zero")
                            expression_attribute_values[':zero'] = 0
                
                if filter_expressions:
                    scan_kwargs['FilterExpression'] = ' AND '.join(filter_expressions)
                    scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values
                    if expression_attribute_names:
                        scan_kwargs['ExpressionAttributeNames'] = expression_attribute_names
            
            response = self.table.scan(**scan_kwargs)
            items = response.get('Items', [])
            
            # Handle pagination if there are more items
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey'],
                    **scan_kwargs
                )
                items.extend(response.get('Items', []))
            
            # Transform items to include the specific fields the user wants
            transformed_items = self._transform_items(items)
            
            return {
                'success': True,
                'data': transformed_items,
                'count': len(transformed_items)
            }
        except ClientError as e:
            return {
                'success': False,
                'error': f"DynamoDB client error: {e.response['Error']['Message']}",
                'error_code': e.response['Error']['Code']
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def _transform_item(self, item):
        """Transform a single DynamoDB item to the required format"""
        transformed = {
            'session_id': item.get('SessionID', ''),
            'flags': self._parse_flags(item.get('Flags', [])),
            'risk_score': self._parse_risk_score(item.get('RiskScore', 0)),
            'timestamp': item.get('Timestamp', ''),
            # Include additional fields that might be useful
            's3_key': item.get('S3Key', ''),
            'rekognition_face_response': self._parse_json_field(item.get('RekognitionFaceResponse', '{}')),
            'rekognition_label_response': self._parse_json_field(item.get('RekognitionLabelResponse', '{}'))
        }
        return transformed
    
    def _transform_items(self, items):
        """Transform multiple DynamoDB items to the required format"""
        return [self._transform_item(item) for item in items]
    
    def _parse_risk_score(self, risk_score_value):
        """Parse risk score from various formats (string, Decimal, int)"""
        try:
            from decimal import Decimal
            if isinstance(risk_score_value, Decimal):
                return int(risk_score_value)
            elif isinstance(risk_score_value, (int, float)):
                return int(risk_score_value)
            elif isinstance(risk_score_value, str):
                if risk_score_value.isdigit():
                    return int(risk_score_value)
                else:
                    return int(float(risk_score_value))  # Handle decimal strings
            else:
                return 0
        except (ValueError, TypeError):
            return 0
    
    def _parse_flags(self, flags_data):
        """Parse the Flags field which is an array of objects with 'S' property"""
        try:
            if isinstance(flags_data, list):
                return [flag.get('S', '') for flag in flags_data if isinstance(flag, dict) and 'S' in flag]
            return []
        except Exception:
            return []
    
    def _parse_json_field(self, json_string):
        """Safely parse JSON string fields"""
        try:
            if isinstance(json_string, str) and json_string.strip():
                import json
                return json.loads(json_string)
            return {}
        except (json.JSONDecodeError, Exception):
            return {}