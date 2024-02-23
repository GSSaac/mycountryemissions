#) create requirements using
pip list --format=freeze > requirements.txt   



# 1) run the application in localhost and verify that it works, with the following code in the command line
uvicorn main:app

# 4) login in google cloud with command, and check that yu are in the right project
gcloud init

#) check that the configuration are correct, for example if you see the following
  region: europe-west1
  zone: europe-west1-d
# 2) go to google cloud console in the web
# create a project: pythonwebapp
# 3) go to artifact registry in the goocle cloud search bar and get the Artifact Registry API for this project
#)create a repository in this artifact registry called mycountryemissions, set the region and the tools docker

#) open the docker desktop application, using following command line code:
open -a Docker

#) run the following code
docker build -t europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image .
#) run the following code
docker push europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image

#) run the following code to deply the app in the cloud
gcloud run deploy --image europe-west4-docker.pkg.dev/pythonwebapp-415018/mycountryemissions/image --platform managed

it will ask a service name you can leave it empty
it will asl to install run.googleapis.com in your project and say yes
it will ask a region 20/21

Allow unauthenticated invocations to [image] (y/N)?  y


https://www.youtube.com/watch?v=gdUh6ZdiN4Y

https://forums.docker.com/t/accessing-a-db-inside-a-docker-container/116106/7
https://www.docker.com/blog/how-to-dockerize-your-python-applications/

https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-copy-files-from-a-Docker-container-to-a-host-machine

I was able to get it to work by building the dockerfile with the whole sqlite database into the image, then run it, and when it's finished, use $ docker cp to copy the updated database into a local folder.

https://cloud.google.com/container-registry/pricing
https://cloud.google.com/artifact-registry/pricing
https://cloud.google.com/python/docs/reference
https://cloud.google.com/python


