FROM python:3.9.5

USER root
# ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /

# CHROME
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# CHROME_DRIVER
RUN apt-get install -yqq unzip
RUN apt-get install -y curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

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

EXPOSE 8000 8001
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

# ADD requirements.txt /home/app
# ADD . .

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

