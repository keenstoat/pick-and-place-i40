# Docker image fraunhoferiosb/faaast-service does not have compatibility for linux/arm/v8 platform
# This image based on https://github.com/FraunhoferIOSB/FAAAST-Service/blob/v1.1.0/starter/Dockerfile
# but uses Raspbian as base image so it can be run in a Raspberry Pi

FROM balenalib/raspberry-pi-debian:20240527

ARG MAVEN_REPO_URL=https://repo1.maven.org/maven2/de/fraunhofer/iosb/ilt/faaast/service/starter
ARG FA3ST_VERSION=1.1.0
ARG USERNAME=faaast

ADD $MAVEN_REPO_URL/$FA3ST_VERSION/starter-$FA3ST_VERSION.jar /app/starter.jar

RUN apt update && apt upgrade && apt install openjdk-17-jre

RUN addgroup --system --gid 1000 $USERNAME \
    && adduser --system --uid 1000 --gid 1000 --no-create-home $USERNAME \
    # restrict permissions on working directory /app
    && chgrp -R 0 /app \
    && chmod -R g=u /app \
    && chown -R $USERNAME:$USERNAME /app \
    # Create directories to which FA³ST needs permissions
    && mkdir /app/resources /app/logs /app/PKI /app/USERS_PKI \
    # Grant read and write permissions on created directories
    && chmod -R ugo+rw /app/resources /app/PKI /app/USERS_PKI /app/logs

USER $USERNAME
WORKDIR /app
ENTRYPOINT ["java", "-jar", "starter.jar"]
