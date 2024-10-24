"""Lanuch spyder kernel on remote server."""

from dataclasses import dataclass, field
from functools import cached_property
import invoke
from pathlib import Path
import subprocess

import appdirs
import click
import fabric
import fsspec
import logging
import numpy as np


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class Connect:
    """Manage connection to remote server."""

    username: str
    hostname: str = "nakasvr23.naka.qst.go.jp"
    session: str = "nakasvr"

    def has_session(self, ssh):
        """Return True if has-session else create new session."""
        try:
            result = ssh.run(f"tmux has-session -t {self.session}", hide=True)
            assert result.return_code == 0
            return True
        except (invoke.UnexpectedExit, AssertionError):
            ssh.run(f"tmux new -d -s {self.session} /usr/bin/bash", hide=True)

    @cached_property
    def filesystem(self):
        """Return fsspec instance."""
        return fsspec.filesystem("ssh", host=self.hostname, username=self.username)

    def connect(self):
        """Mannage connection to host."""
        return fabric.Connection(f"{self.username}@{self.hostname}")

    def kill(self):
        """Kill remote tmux session."""
        with self.connect() as ssh:
            ssh.run(f"tmux kill-session -t {self.session}")


@dataclass
class SpyderKernel(Connect):
    """Manage remote spyder-kernel."""

    kerneldir: str = field(default_factory=appdirs.user_cache_dir)

    @cached_property
    def venv_dir(self):
        """Return venv directory."""
        try:
            venv_dir = f"/home/{self.username}/.venv/{self.session}/bin"
            assert self.filesystem.isdir(venv_dir)
        except AssertionError as error:
            raise AssertionError(
                "SpyderKernel requires a venv on the "
                "remote host with a compatatable version of "
                "spyder-kernel installed."
            ) from error
        return venv_dir

    def _ssh_run(self, ssh, command):
        """Run tmux command."""
        command = command.replace(" ", r"\ ")
        return ssh.run(rf"tmux send -t {self.session}.0 {command} ENTER", hide=True)

    def launch(self):
        """Launch spyder kernel in tmux session running in a venv on the remote host."""
        module_use = "ml use /home/d230021/public/imas/etc/modules/all"
        module_load = "ml Python"
        venv_activate = f". {self.venv_dir}/activate"
        spyder_kernel = "python -m spyder_kernels.console"

        with self.connect() as ssh:
            if self.has_session(ssh):
                return
            for command in [module_use, module_load, venv_activate, spyder_kernel]:
                self._ssh_run(ssh, command)

    @cached_property
    def runtime(self):
        """Return runtime directory."""
        runtime = f"/home/{self.username}/.local/share/jupyter/runtime"
        try:
            assert self.filesystem.isdir(runtime)
        except AssertionError as error:
            raise FileNotFoundError(
                f"runtime directory {runtime} not found."
            ) from error
        return runtime

    def locate(self):
        """Return file detal of last created kernel."""
        files = self.filesystem.ls(self.runtime, detail=True)
        filedetail = files[np.argmax([file["mtime"].timestamp() for file in files])]
        logging.info(f'Found {Path(filedetail["name"]).name}.')
        logging.info(f'Kernel last modified at {filedetail["time"]}.')
        return filedetail

    def copy(self):
        """Copy remote kernel connection file to local host."""
        filedetail = self.locate()
        filepath = filedetail["name"]
        filename = Path(filepath).name
        try:
            assert self.filesystem.isfile(filepath)
        except AssertionError as error:
            raise FileNotFoundError(f"kernel file {filename} not found.") from error

        kerneldir = Path(self.kerneldir) / "kernel.json"
        subprocess.run(
            ["scp", f"{self.username}@{self.hostname}:{filepath}", f"{kerneldir}"]
        )
        assert kerneldir.is_file()
        logging.info(f"Copied {filename} from {self.hostname} to {kerneldir}.")


@click.command()
@click.argument("username")
@click.option(
    "--hostname",
    default="nakasvr23.naka.qst.go.jp",
    help="default: nakasvr23.naka.qst.go.jp.",
)
def remote_kernel(username, hostname):
    """Launch remote spyder-kernel and copy to local host."""
    kernel = SpyderKernel(username, hostname)
    kernel.launch()
    kernel.copy()


if __name__ == "__main__":

    kernel = SpyderKernel("d240044", "nakasvr23.naka.qst.go.jp")
    kernel.launch()
    kernel.copy()
