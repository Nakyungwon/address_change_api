FROM python:3.9.5

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# ADD requirements.txt /home/app
# ADD . .

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

