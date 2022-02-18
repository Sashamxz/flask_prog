FROM python:3.8-slim-buster

ENV FLASK_APP manage.py
ENV FLASK_CONFIG dewelop

RUN adduser  flask


WORKDIR /home/flask

COPY requirements.txt requirements.txt
RUN python -m venv env
RUN env/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY manage.py config.py start.sh ./
RUN chmod +x start.sh
ENV FLASK_APP manage.py

RUN chown -R flask:flask ./

USER flask

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./start.sh"]