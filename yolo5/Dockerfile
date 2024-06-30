FROM ultralytics/yolov5:latest-cpu
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN curl -L https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt -o yolov5s.pt

ENV S3_BUCKET_NAME="raoofbucket"
ENV SQS_QUEUE_URL="https://sqs.us-west-1.amazonaws.com/019273956931/Raoof-AWS-SQS"
ENV DYNAMODB_TABLE_NAME="raoof-DB"
ENV POLYBOT_RESULTS_URL="https://davidhei-polybot.int-devops.click/results"
ENV AWS_REGION="us-west-1"

EXPOSE 80

COPY . .

CMD ["python", "app.py"]