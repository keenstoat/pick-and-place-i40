SHELL=bash
FAAAST_DOCKER_IMAGE_NAME=faaast-server-arm
REST_API_DOCKER_IMAGE_NAME=rest-api

PROJECT_ROOT=/home/charles/repos/project-ss

cleanfast:
	cd aas && make clean

buildfast:
	cd aas && make build

upfast:
	cd aas && make up

#=======================================================================================================================
cleanrest:
	docker rmi -f ${REST_API_DOCKER_IMAGE_NAME} || true

buildrest:
	cd ${PROJECT_ROOT}/integration && docker build --platform linux/arm/v8 -t ${REST_API_DOCKER_IMAGE_NAME} .

uprest:
	docker compose -f ${PROJECT_ROOT}/integration/docker-compose.yaml up

saverest:
	rm -rf /tmp/${REST_API_DOCKER_IMAGE_NAME}-file || true
	docker save -o /tmp/${REST_API_DOCKER_IMAGE_NAME}-file ${REST_API_DOCKER_IMAGE_NAME}

sendrest:
	rsync -a --delete /tmp/${REST_API_DOCKER_IMAGE_NAME}-file pi:/tmp

loadrest:
	docker load -i /tmp/${REST_API_DOCKER_IMAGE_NAME}-file



#=======================================================================================================================

syncfast:
	rsync -a --delete ${PROJECT_ROOT}/faaast pi:${PROJECT_ROOT}

syncint:
	rsync -a --delete ${PROJECT_ROOT}/integration pi:${PROJECT_ROOT}

syncmake:
	rsync -a --delete ${PROJECT_ROOT}/Makefile pi:${PROJECT_ROOT}
