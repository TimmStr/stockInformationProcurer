# start by pulling the python image
FROM python:3.8-alpine

WORKDIR /app

# copy every content from the local file to the image
COPY . /app

# install the dependencies and packages in the requirements file
RUN pip install -r analysisrequirements.txt
EXPOSE 9030
CMD python ./app.py