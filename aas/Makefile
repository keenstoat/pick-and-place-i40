SHELL=bash
DOCKER_IMAGE_NAME=faaast-server-arm
DOCKER_IMAGE_TAG=1.1.0

clean:
	docker rmi -f $$(docker images ${DOCKER_IMAGE_NAME} -q) || true > /dev/null 2>&1

build:
	docker build --platform linux/arm/v8 -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .

config:
	./yaml2json.py config-opcua-http.yaml faaast/config-opcua-http.json
	
all: config clean build