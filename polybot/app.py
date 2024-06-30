import flask
from flask import request
import os

import getsecret
import boto3
from bot import ObjectDetectionBot

import polybot_supp


dynamo_client = boto3.client('dynamodb', region_name='us-west-1')

app = flask.Flask(__name__)


TELEGRAM_TOKEN = getsecret.get_secret()
TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']
DYNAMODB_TABLE_NAME = os.environ['DYNAMO_NAME']
S3_IMAGE_BUCKET = os.environ['S3_BUCKET']



@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


@app.route(f'/results', methods=['POST'])
def results():
    prediction_id = request.args.get('predictionId')

    if "NONE:" == prediction_id[:5]:
        bot.send_text(prediction_id[5::], "Nothing to Predict in this picture.")
    else:
        # use the prediction_id to retrieve results from DynamoDB and send to the end-user
        result = dynamo_client.get_item(
            TableName=DYNAMODB_TABLE_NAME,
            Key={
                "prediction_id": {'S': prediction_id}
            }
        )
        print(f"ITEM CONTAIN: {result.get('Item')}")
        chat_id = result.get('Item').get('chat_id').get('N')
        print(f"CHAT_ID IS: {chat_id}")
        text_results = result.get('Item').get('labels').get('L')
        obj_count = polybot_supp.count_objects_in_list(text_results)
        answer = polybot_supp.parse_info_to_text(obj_count)

        bot.send_text(chat_id, answer)
    return 'Ok'


@app.route(f'/loadTest/', methods=['POST'])
def load_test():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL, S3_IMAGE_BUCKET)

    app.run(host='0.0.0.0', port=8443)
