FROM python:3.10-slim-buster

WORKDIR /home/universe_backend
COPY . .

RUN apt update -y
RUN apt install build-essential -y
RUN apt install default-libmysqlclient-dev -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "server.py" ]