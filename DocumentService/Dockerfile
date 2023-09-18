# start by pulling the python image
FROM python:3.9-slim

WORKDIR /app

# copy every content from the local file to the image
COPY . /app

# install the dependencies and packages in the requirements file
RUN pip install -r document_requirements.txt

# Port "9010" auf dem FLASK-APP läuft
EXPOSE 9010

# Starten der FLASK-App, wenn Contaianer ausgeführt wird
CMD python ./app.py