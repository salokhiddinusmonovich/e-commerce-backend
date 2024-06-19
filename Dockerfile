FROM python:3.10.12-alpine

WORKDIR /app


COPY r.txt r.txt

#RUN pip install --upgrate pip
RUN pip install -r r.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]