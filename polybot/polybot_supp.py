import boto3
import logging
import os
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, s3_client, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def count_objects_in_list(my_list):
    obj_count = {}
    for i in my_list:
        obj_name = i.get('M').get('class').get('S')

        if obj_count.get(obj_name) is None:
            obj_count[obj_name] = 1
        else:
            obj_count[obj_name] = obj_count[obj_name] + 1

    return obj_count


def parse_info_to_text(obj_count_dict):
    text = ""
    for key, value in obj_count_dict.items():
        if value > 1:
            text = text + f"there are {value} {key}s,\n"
        else:
            text = text + f"there is 1 {key},\n"

    return text


def get_secret(secret_name):

    region_name = "us-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret