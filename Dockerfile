FROM python:3.8-slim-buster

ENV FLASK_APP flask_proj.py
ENV FLASK_CONFIG docker

RUN useradd -ms /bin/bash flask




WORKDIR /home/flask


COPY requirements.txt requirements.txt
RUN python -m venv env
RUN env/bin/pip install -r requirements.txt
RUN env/bin/pip install gunicorn

COPY app app
COPY migrations migrations

COPY flask_proj.py config.py start.sh ./

ENV FLASK_APP flask_proj.py


RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8



RUN chown -R flask:flask ./
RUN chmod +x start.sh
USER flask

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./start.sh"]