SHELL=bash

PROJECT_ROOT=/home/charles/repos/project-ss
AAS_DIR=aas
INTEGRATION_DIR=integration

SYSTEMD_SERVICE_FILENAME=pick-and-place.service
SYSTEMD_SERVICES_PATH=/etc/systemd/system



install:
	cp ${SYSTEMD_SERVICE_FILENAME} ${SYSTEMD_SERVICES_PATH}/${SYSTEMD_SERVICE_FILENAME}
	sudo systemctl daemon-reload
	sudo systemctl enable ${SYSTEMD_SERVICE_FILENAME}

#=======================================================================================================================

clean-aas:
	cd ${AAS_DIR} && make clean

build-aas:
	cd ${AAS_DIR} && make build

#=======================================================================================================================

clean-app:
	cd ${INTEGRATION_DIR} && make clean

build-app:
	cd ${INTEGRATION_DIR} && make build


#=======================================================================================================================

cleanall:
	docker rmi -f $$(docker images -aq)

sync:
	cp /mnt/c/Users/charles/Desktop/pick-and-place.aasx aas/faaast/.
	rsync -a --delete ${PROJECT_ROOT}/ pi:${PROJECT_ROOT}/
