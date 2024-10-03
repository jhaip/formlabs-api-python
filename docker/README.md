# Docker Setup

Example of using the Formlabs SDK in Docker.

The Dockerfile exects that the PreFormServer .zip has been downloaded first. Then you can build the dockerfile with a command like:

```
docker build --build-arg ZIP_PATH=PreForm_Server_linux_3.39.0_testing_2320_64310.zip -t preform-server-test .
```

Running the docker image:

```
docker run -it --name preform_server_app -p 44388:44388 --rm docker.io/library/preform-server-test
docker exec -it preform_server_app /workspace/preform/latest/PreForm_Server/PreFormServer
```
