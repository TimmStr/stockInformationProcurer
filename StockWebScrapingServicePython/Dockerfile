# start by pulling the python image
FROM python:3.9-slim

WORKDIR /app

# copy every content from the local file to the image
COPY . /app
COPY stockinformationprocurer-f97f16464594.json stockinformationprocurer-f97f16464594.json

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Port "9040" auf dem FLASK-APP läuft
EXPOSE 9040

# Starten der FLASK-App, wenn Contaianer ausgeführt wird
CMD python ./app.py