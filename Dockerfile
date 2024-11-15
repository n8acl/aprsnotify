FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

ADD src /app/src

COPY aprsnotify.py .

RUN chmod +x aprsnotify.py

CMD ./aprsnotify.py
