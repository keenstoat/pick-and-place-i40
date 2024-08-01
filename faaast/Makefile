SHELL=bash
FAAAST_DOCKER_IMAGE_NAME=faaast-server-arm

syncfast:
	rsync -a --delete /home/charles/repos/project-ss/faaast charles@pi:project-ss

syncint:
	rsync -a --delete /home/charles/repos/project-ss/integration charles@pi:project-ss

clean:
	docker rmi -f ${FAAAST_DOCKER_IMAGE_NAME} || true

build:
	docker build --platform linux/arm/v8 -t ${FAAAST_DOCKER_IMAGE_NAME} .

save:
	rm -rf /tmp/${FAAAST_DOCKER_IMAGE_NAME}-file || true
	docker save -o /tmp/${FAAAST_DOCKER_IMAGE_NAME}-file ${FAAAST_DOCKER_IMAGE_NAME}

send:
	rsync -a --delete /tmp/${FAAAST_DOCKER_IMAGE_NAME}-file pi:/tmp

load:
	docker load -i /tmp/${FAAAST_DOCKER_IMAGE_NAME}-file

up:
	docker compose up

jar:
	cd fa3st && java -jar starter.jar --model /home/charles/project-ss/faaast/fa3st/test-model.aasx --config /home/charles/project-ss/faaast/fa3st/config-opcua-http.json --loglevel-faaast DEBUG