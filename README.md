# mycountryemissions

Steps to follow:

# 1) clone the repository:
https://github.com/GSSaac/mycountryemissions.git

# 2) and set it as your working directory
# 3) create a virtual evnironment in python with python 3.9 and the libraries in the requirements.txt file, 
conda update conda
conda env remove --name webappenv
conda create -n webappenv python=3.9 --yes

conda activate webappenv
which -a pip
which -a python
python -m pip install -r requirements.txt

# 4)1 connect to your google cloud account and create a project:
pythonwebapp

https://console.cloud.google.com/welcome?_ga=2.241349186.-1939604590.1705934040&_gl=1*12d1qps*_up*MQ..&gclid=Cj0KCQiAoeGuBhCBARIsAGfKY7zCGS3UJf6SRfO8eBPQ5y5QJ2IgesyfmhwHzoxaIRYftdmGaB83CucaAlFUEALw_wcB&gclsrc=aw.ds&hl=en&project=pythonwebapp-415018

# 4)2 go to artifact registry and create a repository called mycountryemissions
here the docker image will be sent

# 4)3 start
gcloud init

# 5) open your docker desktop application
open -a Docker

# 6) build the docker image
docker build -t europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image .

# 7) push the docker image
docker push europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image

# 8) run and deploy the app in the cloud
gcloud run deploy --image europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image --platform managed


