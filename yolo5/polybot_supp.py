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


def count_objects_in_dict(mydict):
    obj_count = {}
    for i in mydict:
        obj_name = i.get('class')

        if obj_count.get(obj_name) is not None:
            obj_count[obj_name] = obj_count[obj_name] + 1
        else:
            obj_count[obj_name] = 1

    return obj_count


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


def dict_to_dynamo_format(srs_dict):
    """Convert python dictionary to dynammoDB item.
    this function does not cover all the features and variants of a python dictionary
    and doesn't suitable for usage out-side of the scope of this project.
    """

    dynamo_dict = {}
    for key, value in srs_dict.items():

        if isinstance(value, list) and isinstance(value[0], dict):
            list_item = {'L': []}
            for item in value:
                list_item.get('L').append({'M': dict_to_dynamo_format(item)})
            dynamo_dict[key] = list_item
        else:
            if type(value) is int or type(value) is float:
                type_spec = 'N'
            else:
                type_spec = 'S'
            dynamo_dict[key] = {type_spec: str(value)}
    return dynamo_dict