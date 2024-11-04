# Nakasvr: Connect a local Spyder IDE to a remote kernel

[![image](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.13-blue)](https://git.iter.org/projects/EQ/repos/nova)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)

Nakasvr helps you install, launch, and connect to remote python kernels from
your local Spyder IDE.

## Installation
Instalation is required on both the client (local) and server (remote). The use of
virtual environments is encoraged when installing Nakasvr on both the client
and the server.

### Client install

Create virtual environments for the client and server. Subsiquent use of python commands assumes
that the virtual environment is active.

Installation on the server requires a recent Python>=3.10 module.
```sh
module use /home/d230021/public/imas/etc/modules/all
ml PythonNakasvr helps you install, lanuch, and connect remote python kernels to your local Spyder IDE
```

```sh
python -m venv ~/.venv/nakasvr
. ~/.venv/nakasvr/bin/activate
```

Client
```sh
pip install .[client]
```

Server
```sh
pip install .[server]
```

## Use
Connection of a local Spyder IDE to a remote client requires the lanuch of a Spyder kernel on the server side.
This is managed using the following script

###
```sh

launch_kernel
```

## Development
This packaging and development is managed using Poetry>=2.

```sh
pipx install git+https://github.com/python-poetry/poetry.git
pipx inject poetry "poetry-dynamic-versioning[plugin]"

poetry install
pre-commit install
```
