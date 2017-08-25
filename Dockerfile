FROM python:3.4-slim

RUN mkdir /csud-reservation
WORKDIR /csud-reservation
ADD requirements.txt /csud-reservation
RUN pip install -r requirements.txt

ADD app /csud-reservation/app
ADD config.py /csud-reservation
ADD manage.py /csud-reservation
ADD data /csud-reservation/data
ADD load_csv.py /csud-reservation

CMD python manage.py runserver

# CMD gunicorn -w 4 -b 0.0.0.0:5000 app:app
