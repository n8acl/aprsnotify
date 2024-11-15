FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

ADD src /app/src
add an_util/templates /app/templates

COPY an_util/an_util.py .

RUN chmod +x an_util.py

CMD ./an_util.py