FROM python:3.7

EXPOSE 4040

VOLUME /config
VOLUME /archive

WORKDIR /app

COPY . /app

CMD python app.py