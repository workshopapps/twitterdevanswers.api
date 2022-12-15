FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
#CMD [k"uvicorn", "app.main:app", "host" "000.0",= "--reoad
