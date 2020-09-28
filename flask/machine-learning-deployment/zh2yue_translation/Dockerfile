FROM python:3.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-pip

RUN pip3 install pip --upgrade

RUN pip3 install -r requirements.txt

COPY . /app

CMD python /app/app.py