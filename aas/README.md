# AAS with FAST

## AAS Information Model

The AAS information model is created using the AASX Package Explorer. 

The FA3ST server can take an aasx or a json file as model. We provide the aasx file.

## AssetConnection configuration

The FAST server uses a JSON file for the asset connection configuration.

It is more convenient to use a YAML file as YAML allows comments and text strings are easier to handle. 

For this reason the YAML configuration file is converted to a JSON file using the `yaml2json.py` script.

## FA³ST Server Docker Image for Raspberry PI

The Docker image `fraunhoferiosb/faaast-service` does not have compatibility for linux/arm/v8 platform. For this reason a custom docker image must be used to run the FA³ST server with docker in a raspberry Pi.

The image must be built in the Raspberry PI because the difference in architecture prevents the image form being built in an architecture other than ARM (which is the Raspberry Pi's architecture)

> Building in Ubuntu with the `--platform linux/arm/v8` option set throws an error when installing the `openjdk-17-jre`.