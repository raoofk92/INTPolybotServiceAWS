FROM python:3.10-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV TELEGRAM_APP_URL="Raoof-LoadBalancer-1780755932.us-west-1.elb.amazonaws.com"
ENV S3_BUCKET_NAME="awsraoofbucket"
CMD ["python3", "app.py"]