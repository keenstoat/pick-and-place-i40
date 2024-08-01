# FA³ST Server Docker Image for Raspberry PI


## Build Image

```bash
docker build --platform linux/arm/v8 -t faaast-server-arm .
```

## save image as file
```bash
docker save -o faaast-server-arm-file faaast-server-arm
```

## transfer image to remote
```bash
rsync -a faaast-server-arm-file pi:project-ss
```

## load image from image
```bash
docker load -i faaast-server-arm-file
```

## Run with docker compose

```bash
docker compose up -d
```

## Install Java 17 in Rpi
```bash
sudo apt install openjdk-17-jre
```