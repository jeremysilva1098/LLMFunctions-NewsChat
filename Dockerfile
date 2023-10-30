FROM python:3.10-slim-buster

RUN mkdir /usr/src/app

# install node js
RUN apt-get update && \
    apt-get install -y nodejs && \
    apt-get install -y npm 

RUN apt-get install -y libmagic1

# configure typescript
RUN npm install -g typescript

COPY . /usr/src/app
COPY ./templates/* /usr/src/app/templates/
COPY ./static/* /usr/src/app/static/

WORKDIR /usr/src/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3", "app.py"]