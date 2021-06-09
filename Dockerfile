FROM python:3.9.5

USER root
# ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /
RUN wget -q https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py
RUN python get-poetry.py -y
# RUN source /root/.poetry/env
ENV PATH = "${PATH}:/root/.poetry/bin"
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN poetry install
RUN poetry show

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# ADD requirements.txt /home/app
# ADD . .

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

