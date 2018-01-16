FROM circleci/python:3.6.1

RUN sudo apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential

COPY . /cn-back
WORKDIR /cn-back

RUN sudo pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app/app.py"]

EXPOSE 8080