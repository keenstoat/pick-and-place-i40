# Industrie 4.0-compliant Digitalization of a Pick and Place Module with Real-time Asset Integration

This repository contains the sources for a functional prototype of an AAS-compliant digital twin for a pick-and-place module at the Digital Factory of the University of Applied Sciences in Emden. It uses the RAMI4.0 model as the theoretical framework and the FA³ST service tool as the central implementation technology. The project focuses on the real-time synchronization of the asset's data to and from the digital twin.

The figures below show the pick and place module and a component diagram of the implementation.

<p align="center">
<img src="./report/img/pick-and-place-station-components.svg" width="60%"/>
</p>

<table>
    <tr>
        <th>Pick and Place module</th>
        <th>Implementation Component Diagram</th>
    </tr>
    <tr>
        <td width="60%">
            <img src="./report/img/pick-and-place-station-components.svg" />
        </td>
        <td >
            <img src="./report/img/pick-and-place-station-implementation.svg" />
        </td>
    </tr>
</table>

## Installation

As it can be seen in the component diagram, the implementation is composed of two main applications:
- An AAS served as an OPC UA service
- A python application to interface with the module.

Each component is encapsulated in a Docker container. This keeps the implementation free from software and hardware compatibility issues (at least this is the goal!).

The installation sets up all dependencies required and consists on building the docker images and adding a systemd service so the OPC UA service starts upon system startup.

### Installation steps

First, copy this project into the Raspberry Pi. Make sure to use a user that has sudo permissions.

```bash
rsync -a --delete ${PROJECT_ROOT}/ <user>@<hostname>
```

Then login (SSH or other) to the Raspberry Pi and run the [install script](./install.sh).

```bash
./install.sh
```

You should see a successful output.


### Implementation Source

The source code is divided into:
- [FA³ST service docker image](./aas/README.md)
- [Integration app docker image](./integration/README.md)

The diagram below shows how these two components make up the final implementation.



### Report Source

The report for this project was created using the [Quarto](https://quarto.org/docs/output-formats/pdf-basics.html) technical authoring and publication system. 

The report source code is included in this project so that it can be versioned along side the source code.

The report PDF file is found [here](./report/report.pdf).

The report sources are found [here](./report).


## Connecting to the OPC UA service

With an OPC UA client (UAExpert recommended) connect to the OPCUA service running in the RaspberryPi with this discovery URL:

```
opc.tcp://192.168.158.89:4840
```




# TODO

- remove unused targets in makefiles
- add links to files and web URLs in README files
- proofread and refactor info in README files for pretty documentation
- define a global location for project and update the path for mounted volumes
- get the raspberry pi's version and Rasbian version
- add images of connecting to the OPCUA service and of calling some operations and properties
- put the above in this readme as well!
- create a bash script that installs  docker on the pi if not already. 
- this bash could replace the main makefile as well. review this option
