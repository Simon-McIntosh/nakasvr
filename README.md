# Nakasvr: Connect a local Spyder IDE to a remote kernel

[![image](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://git.iter.org/projects/EQ/repos/nova)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)

Nakasvr helps you install, launch, and connect to remote python kernels from
your local Spyder IDE.

## Installation
Installation is required on both the client (local) and server (remote). The use of
virtual environments is encouraged when installing Nakasvr on both the client
and the server. Installation of `Nakasvr` requires a recent Python>=3.10. 
Installation of dependencies using the `Nakasvr` module ensures that the 
compatible versions of the Spyder IDE and Spyder kernel are used.

### Server-side install
Set up ssh key sharing between the client and the server.  Connect to `nakasvr23.naka.qst.go.jp` and the Load Python module 
```sh
module use /home/d230021/public/imas/etc/modules/all
ml Python
```
Create and activate virtual environment. `Nakasvr` assumes the following default location and name of the server side virtual environment.
```sh
python -m venv ~/.venv/nakasvr
. ~/.venv/nakasvr/bin/activate
```
Install spyder kernel 
```sh
pip install .[server]
```
### Client install
Client
```sh
pip install .[client]
```

Server


## Use
Connection of a local Spyder IDE to a remote client requires the launch of a Spyder kernel on the server side.
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
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTM3MzY1MjUzNCwtMTgxNDc5MjEyNywxMT
M4NDcyNjgxLDExMzc3MTA4MTAsNjY4OTYzODA4XX0=
-->