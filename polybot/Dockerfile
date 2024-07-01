FROM python:3.10-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
ENV TELEGRAM_APP_URL="Raoof-LoadBalancer-1780755932.us-west-1.elb.amazonaws.com"
ENV BUCKET_NAME="awsraoofbucket"
ENV REGION_NAME="us-west-1"
ENV SQS_QUEUE_NAME="Raoof-AWS-SQS"
ENV SQS_QUEUE_URL="https://sqs.us-west-1.amazonaws.com/019273956931/Raoof-AWS-SQS"
CMD ["python3", "app.py"]