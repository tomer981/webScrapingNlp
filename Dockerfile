FROM python:3.9-alpine

RUN apk add --update --no-cache chromium chromium-chromedriver bash


# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /data/bbc
COPY ./app .
CMD [ "python3", "main.py" , "./config.yaml"]
#CMD ["tail", "-f", "/dev/null"]
