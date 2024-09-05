SHELL=bash
DOCKER_IMAGE_NAME=integration-app
DOCKER_IMAGE_TAG=1.0

clean:
	docker rmi -f $$(docker images ${DOCKER_IMAGE_NAME} -q) || true

build:
	docker build --platform linux/arm/v8 -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .
