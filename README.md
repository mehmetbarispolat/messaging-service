# Messaging Service

## Setup

### Required:

- Docker

### Step by Step

- Create network in docker

```
docker network create messagingservicenet
```

- Add Dev Container extension into Visual Studio Code

```
Name: Dev Containers
Id: ms-vscode-remote.remote-containers
Description: Open any folder or repository inside a Docker container and take advantage of Visual Studio Code's full feature set.
Version: 0.330.0
Publisher: Microsoft
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
```

- Open command palette by using CTRL + P or F1. Write `Dev Containers: Open Folder in Container`.

- Create virtual environment after finishing installing container.

```
python -m venv .venv
```

- Activate environment

```
source .venv/bin/activate
```

- Install packages

```
pip install --editable .
```

- Run

```
messaging-service
```