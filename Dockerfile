FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
###CMD ["uvicorn", "app.main:app", "#-jjhost", "0.0.0.0", "--reoad"]
