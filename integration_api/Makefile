SHELL=bash
DOCKER_IMAGE_NAME=integration-api
DOCKER_IMAGE_TAG=1.0

clean:
	docker rmi -f $$(docker images ${DOCKER_IMAGE_NAME} -q) || true

build:
	docker build --platform linux/arm/v8 -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .

up:
	docker compose up

save:
	rm -rf /tmp/${DOCKER_IMAGE_NAME}-file || true
	docker save -o /tmp/${DOCKER_IMAGE_NAME}-file ${DOCKER_IMAGE_NAME}

send:
	rsync -a --delete /tmp/${DOCKER_IMAGE_NAME}-file pi:/tmp

load:
	docker load -i /tmp/${DOCKER_IMAGE_NAME}-file
