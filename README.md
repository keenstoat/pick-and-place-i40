# Industrie 4.0-compliant Digitalization of a Pick and Place Module with Real-time Asset Integration within a Digital Factory

This report presents a project to create a functional prototype of an AAS-compliant digital twin for a pick and place module of the Digital Factory if the University of Applied Sciences in Emden, using the RAMI4.0 model as a theoretical background and the FA³ST service tool as the implementation technology. The project focuses on the real-time syncrhonization of the asset's data to and from the digital twin. ???????????

## Project structure

The project has two main areas:
1. The implementation source code 
2. The report source code

### Implementation Source

The source code is divided into:
- [FA³ST service docker image](./aas/README.md)
- [Integration app docker image](./integration/README.md)

The diagram below shows how these two components make up the final implementation.

<img src="./report/img/pick-and-place-station-implementation.svg" width="50%">

### Report Source

The report for this project was created using the [Quarto](https://quarto.org/docs/output-formats/pdf-basics.html) technical authoring and publication system. 

The report source code is included in this project so that it can be versioned along side the source code.

The report PDF file is found [here](./report/report.pdf).

The report sources are found [here](./report).

## Installation

The installation consists on building the docker images and adding the systemd service so the OPC UA service starts upon system startup.

First copy this project into the Raspberry Pi. Then run the following command with a sudoer user:
```bash
make install
```
> I believe that the best documentation for source code should be the source code itself, so don't be afraid to take a look underneath the hood!
>
> Never the less, the is a README file here and there for general guidance and rationale.

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
