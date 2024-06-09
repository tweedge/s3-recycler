FROM alpine:latest

COPY ./recycler.py /opt/recycler.py
RUN apk add --no-cache python3 py3-boto3

RUN adduser -D nonroot
USER nonroot

CMD ["python3", "-u", "/opt/recycler.py"]