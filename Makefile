SHELL=bash

PROJECT_ROOT=/home/charles/repos/project-ss
AAS_DIR=aas
INTEGRATION_API_DIR=integration_api

cleanaas:
	cd ${AAS_DIR} && make clean

buildaas:
	cd ${AAS_DIR} && make build

upaas:
	cd ${AAS_DIR} && make up

#=======================================================================================================================

cleanapi:
	cd ${INTEGRATION_API_DIR} && make clean

buildapi:
	cd ${INTEGRATION_API_DIR} && make build

upapi: loadapi
	cd ${INTEGRATION_API_DIR} && make up

saveapi:
	cd ${INTEGRATION_API_DIR} && make save

sendapi:
	cd ${INTEGRATION_API_DIR} && make send

loadapi:
	cd ${INTEGRATION_API_DIR} && make load

api: cleanapi buildapi saveapi sendapi


#=======================================================================================================================

cleanall:
	docker rmi -f $$(docker images -aq)

sync:
	cp /mnt/c/Users/charles/Desktop/pick-and-place.aasx aas/faaast/.
	rsync -a --delete ${PROJECT_ROOT}/ pi:${PROJECT_ROOT}/

