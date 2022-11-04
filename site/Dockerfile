FROM python:3.10-slim

WORKDIR /usr/src/app
COPY . .
#RUN yum -y update -y && yum -y install python3
#RUN yum -y install python3
#RUN mv /usr/bin/python3 /usr/bin/python
RUN pip3 install -U pip
RUN pip install -r requirements.txt
RUN /bin/bash -c ./init.sh
CMD /bin/bash -c ./start.sh
EXPOSE 8000
