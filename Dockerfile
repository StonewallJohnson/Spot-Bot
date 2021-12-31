FROM python:3

#Move to working dir in container
WORKDIR /usr/src/app

#Copy files in this directory to work dir
COPY . .

#Install dependencies
RUN pip install -r requirements.txt

#Run the server
WORKDIR /usr/src/app/src
EXPOSE 50000
CMD ["python", "apiserver.py", "$BOT_ID"]