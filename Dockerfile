FROM python:3.10-slim-bullseye

RUN apt-get -y update \
&& apt-get -y upgrade

RUN apt install -y build-essential default-libmysqlclient-dev
RUN pip install --upgrade pip

ENV SERVER /home/universe_backend

RUN mkdir -p $SERVER
WORKDIR $SERVER

EXPOSE 3333

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]