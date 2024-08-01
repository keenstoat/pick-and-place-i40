SHELL=bash
DOCKER_IMAGE_NAME=rest-api

clean:
	docker rmi -f ${DOCKER_IMAGE_NAME} || true

build:
	docker build --platform linux/arm/v8 -t ${DOCKER_IMAGE_NAME} .

save:
	rm -rf /tmp/${DOCKER_IMAGE_NAME}-file || true
	docker save -o /tmp/${DOCKER_IMAGE_NAME}-file ${DOCKER_IMAGE_NAME}

send:
	rsync -a --delete /tmp/${DOCKER_IMAGE_NAME}-file pi:/tmp

load:
	docker load -i /tmp/${DOCKER_IMAGE_NAME}-file

up:
	docker compose up