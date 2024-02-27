# mycountryemissions

Steps to follow:

# 1) clone the repository:
https://github.com/GSSaac/mycountryemissions.git

# 2) and set it as your working directory

# 3) create a virtual evnironment in python with python 3.9 and the libraries in the requirements.txt file, 
conda update conda
#conda env remove --name webappenv
conda create -n webappenv python=3.9 --yes

conda activate webappenv
which -a pip
which -a python
python -m pip install -r requirements.txt

# command for creating requirements.txt: pip list --format=freeze > requirements.txt 

# 4) run the application in local server

uvicorn main:app


# 5)1 build and run and test the dockerimage locally:

uncomment this line in the dockerfile:
CMD ["uvicorn","main:app", "--host","0.0.0.0","--port","8000"]

comment this line in the docker file
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app
# 5)2 build and run and test the dockerimage locally: write in the terminal the following two commands
open -a Docker
docker build -t code .
docker run -p 8000:8000 code

# 5)3 you will receive a link to test that the image is working locally: check this link on your browser

http://0.0.0.0:8000 


# 6)1 build and run and test the dockerimage in the cloud:

comment this line in the dockerfile:
CMD ["uvicorn","main:app", "--host","0.0.0.0","--port","8000"]

uncomment this line in the docker file
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app


# 7)1 connect to your google cloud account and create a project:
pythonwebapp

https://console.cloud.google.com/welcome?_ga=2.241349186.-1939604590.1705934040&_gl=1*12d1qps*_up*MQ..&gclid=Cj0KCQiAoeGuBhCBARIsAGfKY7zCGS3UJf6SRfO8eBPQ5y5QJ2IgesyfmhwHzoxaIRYftdmGaB83CucaAlFUEALw_wcB&gclsrc=aw.ds&hl=en&project=pythonwebapp-415018


# 8)2 go to artifact registry and create a repository called mycountryemissions
here the docker image will be sent

gcloud artifacts repositories list

# 9)3 start, choose region close to you west4  is Netherlands 
gcloud init


# 10) open your docker desktop application
open -a Docker

# 11) build the docker image
docker build -t europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image .

# 12) push the docker image
docker push europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image
# gcloud auth configure-docker \ europe-west4-docker.pkg.dev (run this if the next command does not work)

# 13) run and deploy the app in the cloud: This command deploys the specified container image to Cloud Run with the given service name.
gcloud run deploy --image europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image --platform managed

# it will ask a service name you can leave it empty
# it will ask to install run.googleapis.com in your project and say yes
# it will ask a region 21 corresponding to europe west 4
# Aset llow unauthenticated invocations to [image] (y/N)?  y


# 14) test locally the docker image that has been pushed in the Artifact Registry using this command:

PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image

# then connect to 
http://localhost:9090/
# to verify that the application is running






##################

# USEFUL COMMANDS:
# get docker version
docker -v

# get list of containers:
docker ps -a

# stop docker:
docker stop containerID

# remove docker:
docker rm containerID

# check processes on port 8000
sudo lsof -i :8000

# kill process on port 8000
sudo kill -9 `sudo lsof -t -i:8000` 