FROM python:3.8

RUN apt update

RUN mkdir /srv/project
WORKDIR /srv/project

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENV TZ Europe/Kiev

CMD ["bash"]