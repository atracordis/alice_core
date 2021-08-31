FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests pandas==1.2.4
ARG USERNAME
ARG PASSWORD
ENV USERNAME=${USERNAME} 
ENV PASSWORD=${PASSWORD}
ADD test_sentiment.py test_sentiment.py
ADD test_data.csv test_data.csv
EXPOSE 8000
CMD python3 test_sentiment.py ${USERNAME} ${PASSWORD}
