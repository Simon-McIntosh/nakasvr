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
Connect to `nakasvr23.naka.qst.go.jp` and load a recent Python (>=3.10) module.
```sh
ssh <username>@nakasvr23.naka.qst.go.jp
module use /home/d230021/public/imas/etc/modules/all
ml Python
```
Create and activate the server-side virtual environment. `Nakasvr` assumes the following default location and name of the server-side virtual environment.
```sh
python -m venv ~/.venv/nakasvr
. ~/.venv/nakasvr/bin/activate
```
Install the spyder kernel into the `nakasvr` venv.
```sh
pip install --user git+https://github.com/Simon-McIntosh/nakasvr.git@main
```
### Client-side install
Create and activate the client-side virtual environment. This environment may take any name or location. Here, for simplicity, we select the same name and location of the virtual environment as the one used for the server side install.
```sh
python -m venv ~/.venv/nakasvr
. ~/.venv/nakasvr/bin/activate
```
Install the client environment. This install includes the Spyder IDE that is ensured to be compatable with the remote spyder-kernel.
```sh
pip install "nakasvr[client] @ git+https://github.com/Simon-McIntosh/nakasvr.git@main"
```
## Use
The following `lanuch_kernel`, `copy_kernel`, and `kill_kernel` commands are issued from the client-side.  These commands are used to manage the spyder kernel running on the Naka server. Commands are 'windowed' using `tmux`. This allows the remote spyder kernel to persist independent of the connection status of the user.

Connection of a local Spyder IDE to a remote client requires an instance of the Spyder kernel to be launched on server. The connection file for this kernel must then be copied from the server to the client. Both of these steps are handled by the `Nakasvr` module using the `lanuch_kernel` and `copy_kernel` commands run from the client. 
```sh
launch_kernel <username>
copy_kernel <username>
```
The kernel running on the Naka server may be terminated at any time with the following command.
```sh
kill_kernel <username>
```
The launch / copy step described below is only required following reboots of the `nakasvr23` analysis server or following a `kill_kernel` command.

Once the remote spyder kernel has been lanuched and the ID has been copied back to the client a local Spyder (>=6.0.0) IDE may now be connected to the remote kernel. This IDE does not need to be run in an OS of choice (Windows, Linux, Mac). 
Select `consoles/connect to an existing kernel` from within the Spyder IDE and fill in the required details, including the path to the `kernel.json` connection file downloaded by the `copy_kernel` command.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg2MDI2Njc5MywxMDM5NzgxMDM4LC03OD
A3NDQ4NTgsMTQ4MTkyNDI2NiwxODM3MDc1NTcwLC0xODE0Nzky
MTI3LDExMzg0NzI2ODEsMTEzNzcxMDgxMCw2Njg5NjM4MDhdfQ
==
-->
