FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ARG USERNAME
ARG PASSWORD
ENV USERNAME=${USERNAME} 
ENV PASSWORD=${PASSWORD}
ADD test_user.py test_user.py
EXPOSE 8000
CMD python3 test_user.py ${USERNAME} ${PASSWORD}
