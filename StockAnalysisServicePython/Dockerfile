# start by pulling the python image
FROM python:3.6

WORKDIR /app

# copy every content from the local file to the image
COPY . /app

# install the dependencies and packages in the requirements file
#RUN pip install --upgrade pip
#RUN apk add --no-cache --update \
#    python3 python3-dev gcc \
#    gfortran musl-dev

RUN pip install -r analysisrequirements.txt
#RUN #pip3 install --upgrade pip setuptools && \
#
EXPOSE 9040
CMD python ./app.py