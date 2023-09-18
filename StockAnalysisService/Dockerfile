# start by pulling the python image
FROM python:3.9-slim

WORKDIR /app

# copy every content from the local file to the image
COPY . /app

RUN pip install -r analysisrequirements.txt

EXPOSE 9030

CMD python ./app.py