"""
AIVibe AWS Knowledge Module

Complete AWS CLI patterns, Lambda, DynamoDB, S3, API Gateway,
Cognito, and serverless architecture best practices.
"""


class AWSKnowledge:
    """Comprehensive AWS development knowledge."""

    CLI_VERSION = "2.15"
    SDK_VERSION = "boto3 1.34"

    CLI_COMMANDS = {
        "configuration": {
            "configure": "aws configure --profile myprofile",
            "list_profiles": "aws configure list-profiles",
            "get_caller": "aws sts get-caller-identity",
            "assume_role": """
aws sts assume-role \\
    --role-arn arn:aws:iam::123456789012:role/MyRole \\
    --role-session-name MySession""",
        },
        "s3": {
            "list_buckets": "aws s3 ls",
            "list_objects": "aws s3 ls s3://bucket-name/prefix/",
            "copy": "aws s3 cp local-file s3://bucket/key",
            "sync": "aws s3 sync ./local-dir s3://bucket/prefix --delete",
            "presigned_url": "aws s3 presign s3://bucket/key --expires-in 3600",
            "recursive_delete": "aws s3 rm s3://bucket/prefix --recursive",
        },
        "dynamodb": {
            "list_tables": "aws dynamodb list-tables",
            "describe_table": "aws dynamodb describe-table --table-name MyTable",
            "get_item": """
aws dynamodb get-item \\
    --table-name MyTable \\
    --key '{"pk": {"S": "USER#123"}, "sk": {"S": "PROFILE"}}'""",
            "query": """
aws dynamodb query \\
    --table-name MyTable \\
    --key-condition-expression "pk = :pk" \\
    --expression-attribute-values '{":pk": {"S": "USER#123"}}'""",
            "put_item": """
aws dynamodb put-item \\
    --table-name MyTable \\
    --item '{"pk": {"S": "USER#123"}, "sk": {"S": "PROFILE"}, "name": {"S": "John"}}'""",
        },
        "lambda": {
            "list_functions": "aws lambda list-functions",
            "invoke": """
aws lambda invoke \\
    --function-name MyFunction \\
    --payload '{"key": "value"}' \\
    --cli-binary-format raw-in-base64-out \\
    response.json""",
            "update_code": """
aws lambda update-function-code \\
    --function-name MyFunction \\
    --zip-file fileb://function.zip""",
            "get_logs": """
aws logs filter-log-events \\
    --log-group-name /aws/lambda/MyFunction \\
    --start-time $(date -d '1 hour ago' +%s000)""",
        },
        "secrets_manager": {
            "list_secrets": "aws secretsmanager list-secrets",
            "get_secret": """
aws secretsmanager get-secret-value \\
    --secret-id my-secret-name \\
    --query SecretString \\
    --output text""",
            "create_secret": """
aws secretsmanager create-secret \\
    --name my-secret \\
    --secret-string '{"key": "value"}'""",
        },
        "cognito": {
            "list_user_pools": "aws cognito-idp list-user-pools --max-results 10",
            "list_users": """
aws cognito-idp list-users \\
    --user-pool-id us-east-1_xxxxx""",
            "admin_get_user": """
aws cognito-idp admin-get-user \\
    --user-pool-id us-east-1_xxxxx \\
    --username user@example.com""",
        },
    }

    LAMBDA = {
        "handler_patterns": {
            "api_gateway": """
import json
from typing import Any

def handler(event: dict, context: Any) -> dict:
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = event['requestContext']['authorizer']['claims']['sub']

        result = process_request(body, user_id)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
    except ValidationError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }""",
            "sqs_trigger": """
def handler(event: dict, context: Any) -> dict:
    failed_ids = []

    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            process_message(body)
        except Exception as e:
            print(f"Failed to process {record['messageId']}: {e}")
            failed_ids.append({'itemIdentifier': record['messageId']})

    return {'batchItemFailures': failed_ids}""",
            "dynamodb_stream": """
def handler(event: dict, context: Any) -> None:
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            handle_insert(deserialize(new_image))
        elif record['eventName'] == 'MODIFY':
            old_image = record['dynamodb']['OldImage']
            new_image = record['dynamodb']['NewImage']
            handle_update(deserialize(old_image), deserialize(new_image))
        elif record['eventName'] == 'REMOVE':
            old_image = record['dynamodb']['OldImage']
            handle_delete(deserialize(old_image))""",
            "scheduled": """
def handler(event: dict, context: Any) -> None:
    # Triggered by EventBridge schedule
    print(f"Running scheduled task at {event['time']}")
    run_scheduled_job()""",
        },
        "best_practices": {
            "cold_start": [
                "Keep deployment packages small",
                "Initialize SDK clients outside handler",
                "Use provisioned concurrency for critical functions",
                "Prefer ARM64 architecture (Graviton2)",
            ],
            "connections": [
                "Reuse database connections",
                "Use RDS Proxy for relational databases",
                "Configure proper timeout values",
            ],
            "logging": """
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(json.dumps({
        'event': 'request_received',
        'request_id': context.aws_request_id,
        'path': event.get('path'),
        'method': event.get('httpMethod')
    }))""",
        },
    }

    DYNAMODB = {
        "single_table_design": {
            "patterns": {
                "pk_sk": "Use composite primary key (PK, SK) for all access patterns",
                "gsi_overloading": "GSI1PK, GSI1SK for additional access patterns",
                "type_prefix": "USER#123, PROJECT#456 for type identification",
            },
            "example": """
# Single-table design example
ITEMS = [
    # User profile
    {'PK': 'USER#123', 'SK': 'PROFILE', 'name': 'John', 'email': '...'},

    # User's projects (1:N)
    {'PK': 'USER#123', 'SK': 'PROJECT#p1', 'GSI1PK': 'PROJECT#p1', 'GSI1SK': 'MEMBER#123'},
    {'PK': 'USER#123', 'SK': 'PROJECT#p2', 'GSI1PK': 'PROJECT#p2', 'GSI1SK': 'MEMBER#123'},

    # Project details
    {'PK': 'PROJECT#p1', 'SK': 'METADATA', 'name': 'Project 1', 'owner': 'USER#123'},

    # Project tasks
    {'PK': 'PROJECT#p1', 'SK': 'TASK#t1', 'title': 'Task 1', 'status': 'pending'},
    {'PK': 'PROJECT#p1', 'SK': 'TASK#t2', 'title': 'Task 2', 'status': 'done'},
]

# Access patterns:
# 1. Get user profile: query(PK='USER#123', SK='PROFILE')
# 2. Get user's projects: query(PK='USER#123', SK begins_with 'PROJECT#')
# 3. Get project details: query(PK='PROJECT#p1', SK='METADATA')
# 4. Get project tasks: query(PK='PROJECT#p1', SK begins_with 'TASK#')
# 5. Get project members: query(GSI1PK='PROJECT#p1', GSI1SK begins_with 'MEMBER#')""",
        },
        "boto3_operations": {
            "get_item": """
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def get_user(user_id: str) -> dict | None:
    response = table.get_item(
        Key={'PK': f'USER#{user_id}', 'SK': 'PROFILE'}
    )
    return response.get('Item')""",
            "query": """
def get_user_projects(user_id: str) -> list[dict]:
    response = table.query(
        KeyConditionExpression=Key('PK').eq(f'USER#{user_id}') & Key('SK').begins_with('PROJECT#')
    )
    return response['Items']""",
            "put_item": """
def create_user(user_id: str, data: dict) -> None:
    table.put_item(
        Item={
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE',
            **data,
            'created_at': datetime.utcnow().isoformat()
        },
        ConditionExpression='attribute_not_exists(PK)'  # Prevent overwrite
    )""",
            "update_item": """
def update_user(user_id: str, updates: dict) -> dict:
    update_expr = 'SET ' + ', '.join(f'#{k} = :{k}' for k in updates)
    expr_names = {f'#{k}': k for k in updates}
    expr_values = {f':{k}': v for k, v in updates.items()}
    expr_values[':updated_at'] = datetime.utcnow().isoformat()
    update_expr += ', #updated_at = :updated_at'
    expr_names['#updated_at'] = 'updated_at'

    response = table.update_item(
        Key={'PK': f'USER#{user_id}', 'SK': 'PROFILE'},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values,
        ReturnValues='ALL_NEW'
    )
    return response['Attributes']""",
            "batch_write": """
def batch_create_items(items: list[dict]) -> None:
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)""",
            "transact_write": """
def transfer_credits(from_user: str, to_user: str, amount: int) -> None:
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_client.transact_write_items(
        TransactItems=[
            {
                'Update': {
                    'TableName': 'MyTable',
                    'Key': {'PK': {'S': f'USER#{from_user}'}, 'SK': {'S': 'PROFILE'}},
                    'UpdateExpression': 'SET credits = credits - :amount',
                    'ConditionExpression': 'credits >= :amount',
                    'ExpressionAttributeValues': {':amount': {'N': str(amount)}}
                }
            },
            {
                'Update': {
                    'TableName': 'MyTable',
                    'Key': {'PK': {'S': f'USER#{to_user}'}, 'SK': {'S': 'PROFILE'}},
                    'UpdateExpression': 'SET credits = credits + :amount',
                    'ExpressionAttributeValues': {':amount': {'N': str(amount)}}
                }
            }
        ]
    )""",
        },
    }

    S3 = {
        "operations": {
            "upload": """
import boto3

s3 = boto3.client('s3')

def upload_file(file_path: str, bucket: str, key: str) -> str:
    s3.upload_file(file_path, bucket, key)
    return f's3://{bucket}/{key}'

def upload_bytes(data: bytes, bucket: str, key: str, content_type: str) -> str:
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        ContentType=content_type
    )
    return f's3://{bucket}/{key}'""",
            "download": """
def download_file(bucket: str, key: str, local_path: str) -> None:
    s3.download_file(bucket, key, local_path)

def get_object_content(bucket: str, key: str) -> bytes:
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()""",
            "presigned_url": """
def generate_presigned_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expires_in
    )

def generate_presigned_post(bucket: str, key: str) -> dict:
    return s3.generate_presigned_post(
        Bucket=bucket,
        Key=key,
        Fields={'Content-Type': 'application/octet-stream'},
        Conditions=[
            {'Content-Type': 'application/octet-stream'},
            ['content-length-range', 0, 10485760]  # 10MB max
        ],
        ExpiresIn=3600
    )""",
        },
    }

    COGNITO = {
        "user_management": """
import boto3

cognito = boto3.client('cognito-idp')
USER_POOL_ID = 'us-east-1_xxxxxx'

def get_user(username: str) -> dict | None:
    try:
        response = cognito.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=username
        )
        return {
            attr['Name']: attr['Value']
            for attr in response['UserAttributes']
        }
    except cognito.exceptions.UserNotFoundException:
        return None

def create_user(email: str, temp_password: str) -> str:
    response = cognito.admin_create_user(
        UserPoolId=USER_POOL_ID,
        Username=email,
        UserAttributes=[
            {'Name': 'email', 'Value': email},
            {'Name': 'email_verified', 'Value': 'true'}
        ],
        TemporaryPassword=temp_password,
        MessageAction='SUPPRESS'  # Don't send welcome email
    )
    return response['User']['Username']

def set_user_attribute(username: str, name: str, value: str) -> None:
    cognito.admin_update_user_attributes(
        UserPoolId=USER_POOL_ID,
        Username=username,
        UserAttributes=[{'Name': name, 'Value': value}]
    )""",
        "token_verification": """
import jwt
from jwt import PyJWKClient

COGNITO_REGION = 'us-east-1'
USER_POOL_ID = 'us-east-1_xxxxxx'
APP_CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'

jwks_url = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'
jwks_client = PyJWKClient(jwks_url)

def verify_token(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=['RS256'],
        audience=APP_CLIENT_ID,
        issuer=f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}'
    )""",
    }

    API_GATEWAY = {
        "lambda_integration": """
# API Gateway event structure
{
    "resource": "/users/{userId}",
    "path": "/users/123",
    "httpMethod": "GET",
    "headers": {"Authorization": "Bearer xxx"},
    "pathParameters": {"userId": "123"},
    "queryStringParameters": {"include": "profile"},
    "body": null,
    "requestContext": {
        "authorizer": {
            "claims": {
                "sub": "user-uuid",
                "email": "user@example.com"
            }
        }
    }
}""",
        "response_format": """
# Proper API Gateway response
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
    },
    "body": "{\"data\": \"value\"}"  # Must be string
}""",
    }

    BEST_PRACTICES = {
        "security": [
            "Use IAM roles, never hardcode credentials",
            "Enable CloudTrail for all accounts",
            "Use Secrets Manager for sensitive config",
            "Enable encryption at rest (S3, DynamoDB, RDS)",
            "Use VPC endpoints for private access",
            "Apply least-privilege IAM policies",
        ],
        "cost_optimization": [
            "Use reserved capacity for predictable workloads",
            "Enable S3 Intelligent-Tiering",
            "Use DynamoDB on-demand for variable traffic",
            "Set up billing alerts",
            "Use Spot instances for fault-tolerant workloads",
        ],
        "reliability": [
            "Design for multi-AZ availability",
            "Implement exponential backoff for retries",
            "Use DLQ for failed messages",
            "Enable point-in-time recovery for DynamoDB",
            "Use CloudWatch alarms for monitoring",
        ],
    }

    def get_all(self) -> dict:
        """Get complete AWS knowledge."""
        return {
            "cli_version": self.CLI_VERSION,
            "cli_commands": self.CLI_COMMANDS,
            "lambda": self.LAMBDA,
            "dynamodb": self.DYNAMODB,
            "s3": self.S3,
            "cognito": self.COGNITO,
            "api_gateway": self.API_GATEWAY,
            "best_practices": self.BEST_PRACTICES,
        }

    def get_cli_commands(self) -> dict:
        """Get AWS CLI command reference."""
        return self.CLI_COMMANDS

    def get_lambda_patterns(self) -> dict:
        """Get Lambda handler patterns."""
        return self.LAMBDA

    def get_dynamodb_patterns(self) -> dict:
        """Get DynamoDB patterns."""
        return self.DYNAMODB
