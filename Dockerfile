FROM python:3

#Move to working dir in container
WORKDIR /usr/src/app

#Copy files in this directory to work dir
COPY . .
#Install dependencies
RUN pip install -r requirements.txt

#Run the server
WORKDIR src
EXPOSE 50000
ENTRYPOINT ["python", "apiserver.py"]