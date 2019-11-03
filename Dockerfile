FROM python:3.7-stretch

COPY . /usr/src/app/
RUN /usr/src/app/scripts/install-coap-client.sh && pip3 install pytradfri flask

WORKDIR /usr/src/app

CMD ["python3", "app.py"]