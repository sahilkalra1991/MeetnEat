FROM python:3.10

WORKDIR /build

COPY requirements.txt ./

RUN apt-get update
RUN apt-get install -y libmariadb-dev gcc python3-dev
RUN pip install -r requirements.txt
RUN pip freeze


CMD python manage.py runserver 0.0.0.0:8000