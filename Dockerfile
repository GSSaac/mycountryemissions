# Dockerfile, Image, Container
FROM python:3.9



WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

# CMD ["uvicorn","main:app", "--host","0.0.0.0","--port","8000"]
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app

# docker build -t europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions .
# docker push europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions

# docker build -t fastapi-tutorial .

# docker run -p 8000:8000 fastapi-tutorial
# docker run -p --name myfastapicotainer -p 8000:8000 fastapi-tutorial


# docker -v

# build docker image (gives a name python-imdb in current directory)

# rebuild every time make change to the code
## docker build -t python-imdb .

# run the image
## docker run python-imdb

# if application requires inut from outside
# then write -i of interactive
## docker run -i -t python-imdb

#sudo kill -9 `sudo lsof -t -i:80` 

# get list of containers:
# docker ps -a

# stop docker:
# docker stop containerID


# stop docker:
# docker stop containerID

# remove docker:
# docker rm containerID

# check processes on port 80
# sudo lsof -i :80