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
compatible versions of the Spyder IDE and Spyder kernel are used. SSH key sharing should be set up between the client and the server.

### Server-side install
Connect to `nakasvr23.naka.qst.go.jp` and the Load Python module 
```sh
ssh <username>@nakasvr23.naka.qst.go.jp
module use /home/d230021/public/imas/etc/modules/all
ml Python
```
Create and activate the server-side virtual environment. `Nakasvr` assumes the following default location and name of the server side virtual environment.
```sh
python -m venv ~/.venv/nakasvr
. ~/.venv/nakasvr/bin/activate
```
Install spyder kernel 
```sh
pip install --user git+https://github.com/Simon-McIntosh/nakasvr.git@main
```
### Client-side install
Create and activate the client-side virtual environment. This environment may take any name or location. Here, for simplicity, we select the same name and location of the virtual environment as the one used for the server side install.
```sh
python -m venv ~/.venv/nakasvr
. ~/.venv/nakasvr/bin/activate
```
Install the client environment. This install includes the Spyder IDE.
```sh
pip install "nakasvr[client] @ git+https://github.com/Simon-McIntosh/nakasvr.git@main"
```
Connection of a local Spyder IDE to a remote client requires an instance of the Spyder kernel to be launched on server. The connection ID of this kernel must then be copied from the server to the client. Both of these steps are handled by the `Nakasvr` module using the `lanuch_kernel` and `copy_kernel` commands run from the client. 
```sh
launch_kernel

```
## Use


This command instigates the spyder kernel within a `tmux` window on the server.  The use of a `tmux` window allows the remote spyder kernel to persist independent of the connection status of the user.
###

The launch / copy step described below is only required following reboots of the `nakasvr23` analysis server.





## Development
This packaging and development is managed using Poetry>=2.

```sh
pipx install git+https://github.com/python-poetry/poetry.git
pipx inject poetry "poetry-dynamic-versioning[plugin]"

poetry install
pre-commit install
```
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjg5ODA5NTgzLDEwMzk3ODEwMzgsLTc4MD
c0NDg1OCwxNDgxOTI0MjY2LDE4MzcwNzU1NzAsLTE4MTQ3OTIx
MjcsMTEzODQ3MjY4MSwxMTM3NzEwODEwLDY2ODk2MzgwOF19
-->