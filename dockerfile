FROM python:3.8-slim-buster

WORKDIR /app

# copy the content of the local src directory to the working directory
COPY botv2.py .
COPY game_lg.py .
COPY hellper.py .
COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "main.py" ]