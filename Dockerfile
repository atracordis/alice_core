FROM ubuntu:20.04

ADD ./ ./

RUN apt update && apt install python3-pip libmysqlclient-dev -y && pip install -r requirements.txt

RUN python3 -m nltk.downloader stopwords

EXPOSE 8000

CMD uvicorn src.app:app --host 0.0.0.0
