# our base image
FROM python:3.7-stretch

RUN mkdir /cnn
WORKDIR /cnn

# specify the port number the container should expose
EXPOSE 5000

COPY requirements.txt /cnn

RUN pip install -r requirements.txt

# Download spacy model (problem if it's in the requirements file. It would be because of the version)
RUN spacy download en_core_web_sm

COPY . /cnn/


# run the application
CMD ["python", "./run.py"]