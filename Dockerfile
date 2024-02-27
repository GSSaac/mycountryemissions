# Dockerfile, Image, Container
FROM python:3.9

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

#CMD ["uvicorn","main:app", "--host","0.0.0.0","--port","8000"]

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app










