# py-rtsp-recorder
A simple rtsp recorder

## Installation

### Install ffmpeg

On debian/ubuntu :
```shell
$ sudo apt install -y ffmpeg
```

### Install python

On debian/ubuntu :
```shell
$ sudo apt install -y python3 python3-pip
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

### Install dependencies
```shell
$ pip3 install -r requirements.txt
```

### Configure the project
copy .env.exemple to .env

Edit values with yours

## Usage
```shell
$ python3 recorder.py
```


## Use with docker

### Docker

```shell
$ docker run -d \
  --name rtsp_recorder \
  --env-file .env \
  -v $(pwd)/recordings:/app/recordings \
  ghcr.io/d4rts/py-rtsp-recorder:latest
```

### Docker compose
```yml
services:
  recorder:
    image: ghcr.io/d4rts/py-rtsp-recorder:latest
    container_name: rtsp_recorder
    env_file:
      - .env
    volumes:
      - ./recordings:/app/recordings
    restart: unless-stopped
```