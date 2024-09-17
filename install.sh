#!/usr/bin/env bash

END='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'

PICK_AND_PLACE_WORKING_DIR=/etc/pick-and-place
PICK_AND_PLACE_SYSTEMD_DIR=/etc/systemd/system/
PICK_AND_PLACE_SERVICE_FILENAME=pick-and-place.service

echo_info() {
    echo -e "${CYAN}INFO: ${END} ${1}\n"
}
echo_ok() {
    echo -e "${GREEN}OK: ${END} ${1}\n"
}
echo_fail() {
    echo -e "${RED}FAIL: ${END} ${1}\n"
}


system_checks() {
    cat /etc/os-release | grep -i raspbian > /dev/null 2>&1
    if [[ $? == 1 ]]; then
        echo_fail "Must run this script inside the Raspberry Pi!. Nothing to do."
        exit 1
    fi

    which docker > /dev/null 2>&1
    if [[ $? == 1 ]]; then
        echo_info "Docker is not installed in the Raspberry Pi. Installing now!!"
        sudo apt update
        sudo apt upgrade
        curl -sSL https://get.docker.com | sh
        sudo usermod -aG docker $USER
    fi

    which docker > /dev/null 2>&1
    if [[ $? == 1 ]]; then
        echo_fail "Docker could not be installed. Please troubleshoot manually and try again."
        exit 1
    fi

    echo_ok "All dependencies are met. Continuing..."
}

build_docker_images() {
    echo_info "Building AAS docker image"
    cd aas/
    make all

    echo_info "Building Integration app docker image"
    cd ../integration/
    make all

    cd ..
}

setup_docker_compse_files() {

    echo_info "Creating ${PICK_AND_PLACE_WORKING_DIR} directory..."
    sudo mkdir -p ${PICK_AND_PLACE_WORKING_DIR} || true > /dev/null 2>&1

    echo_info "Copying faaast directory to ${PICK_AND_PLACE_WORKING_DIR}"
    sudo cp -r aas/faaast ${PICK_AND_PLACE_WORKING_DIR}/.

    echo_info "Copying docker-compose.yaml to ${PICK_AND_PLACE_WORKING_DIR}"
    sudo cp docker-compose.yaml ${PICK_AND_PLACE_WORKING_DIR}/.
}

setup_systemd_service() {

    echo_info "Stopping ${PICK_AND_PLACE_SERVICE_FILENAME} service..."
    sudo systemctl stop ${PICK_AND_PLACE_SERVICE_FILENAME} || true > /dev/null 2>&1

    echo_info "Creating pick-and-place.service service file"
    cat <<-_EOF > ${PICK_AND_PLACE_SERVICE_FILENAME}
	[Unit]
	Description=Pick and place Docker Compose Service
	Requires=docker.service
	After=docker.service

	[Service]
	Type=oneshot
	RemainAfterExit=yes
	WorkingDirectory=${PICK_AND_PLACE_WORKING_DIR}
	ExecStart=/usr/bin/docker compose up -d
	ExecStop=/usr/bin/docker compose down
	TimeoutStartSec=0

	[Install]
	WantedBy=multi-user.target
	_EOF

    echo_info "Setting up pick-and-place.service service"
    sudo mv ${PICK_AND_PLACE_SERVICE_FILENAME} ${PICK_AND_PLACE_SYSTEMD_DIR}/${PICK_AND_PLACE_SERVICE_FILENAME}
    sudo chmod 644 ${PICK_AND_PLACE_SYSTEMD_DIR}/${PICK_AND_PLACE_SERVICE_FILENAME}
    sudo systemctl daemon-reload
    sudo systemctl enable ${PICK_AND_PLACE_SERVICE_FILENAME}
}

start_service() {

    echo_info "Starting the ${PICK_AND_PLACE_SERVICE_FILENAME} service..."
    sudo systemctl start ${PICK_AND_PLACE_SERVICE_FILENAME}
    for (( i=1; i<=10; i++ ))
    do
        nc -zv localhost 4840 > /dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            break
        fi
        sleep 3
    done
    nc -zv localhost 4840 > /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo_fail "Seems the pick-and-place OPC UA server is not responding. Please troubleshoot manually!"
        exit 1
    else
        echo_ok "The pick-and-place OPC UA server is listening on port 4840!"
    fi
}


system_checks
build_docker_images
setup_docker_compse_files
setup_systemd_service

start_service