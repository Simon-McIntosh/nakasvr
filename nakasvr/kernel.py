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

    def has_session(self):
        """Return True if has-session else create new session."""
        try:
            result = self.ssh.run(f"tmux has-session -t {self.session}", hide=True)
            assert result.return_code == 0
        except (invoke.UnexpectedExit, AssertionError):
            self.ssh.run(f"tmux new -d -s {self.session} /usr/bin/bash", hide=True)

    @cached_property
    def filesystem(self):
        """Return fsspec instance."""
        return fsspec.filesystem("ssh", host=self.hostname, username=self.username)

    @cached_property
    def ssh(self):
        """Mannage connection to host."""
        return fabric.Connection(f"{self.username}@{self.hostname}")

    def kill(self):
        """Kill remote tmux session."""
        self.ssh.run(f"tmux kill-session -t {self.session}")


@dataclass
class SpyderKernel(Connect):
    """Manage remote spyder-kernel."""

    kerneldir: str = field(default_factory=appdirs.user_cache_dir)

    @cached_property
    def homedir(self):
        """Return home directory on remote."""
        return Path(self.ssh.run("echo $HOME", hide=True).stdout.strip())

    @cached_property
    def venvdir(self):
        """Return venv directory."""
        try:
            venvdir = self.homedir / f".venv/{self.session}/bin"
            assert self.filesystem.isdir(venvdir.as_posix())
        except AssertionError as error:
            raise AssertionError(
                "SpyderKernel requires the following venv to be present on the "
                f"remote host {venvdir}."
            ) from error
        return venvdir

    def _ssh_run(self, command):
        """Run tmux command."""
        command = command.replace(" ", r"\ ")
        return self.ssh.run(
            rf"tmux send -t {self.session}.0 {command} ENTER", hide=True
        )

    def launch(self):
        """Launch spyder kernel in tmux session running in a venv on the remote host."""
        module_use = "ml use /home/d230021/public/imas/etc/modules/all"
        module_load = "ml IMASPy"
        venv_activate = f". {self.venvdir}/activate"
        spyder_kernel = "python -m spyder_kernels.console"

        if self.has_session():
            return
        for command in [module_use, module_load, venv_activate, spyder_kernel]:
            self._ssh_run(command)

    @cached_property
    def runtime(self):
        """Return runtime directory."""
        runtime = self.homedir / ".local/share/jupyter/runtime"
        try:
            assert self.filesystem.isdir(runtime.as_posix())
        except AssertionError as error:
            raise FileNotFoundError(
                f"runtime directory {runtime} not found."
            ) from error
        return runtime

    def locate(self):
        """Return file detal of last created kernel."""
        files = self.filesystem.ls(self.runtime.as_posix(), detail=True)
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
def launch_kernel(username, hostname):
    """Launch remote spyder-kernel and copy to local host."""
    kernel = SpyderKernel(username, hostname)
    kernel.launch()


@click.command()
@click.argument("username")
@click.option(
    "--hostname",
    default="nakasvr23.naka.qst.go.jp",
    help="default: nakasvr23.naka.qst.go.jp.",
)
def copy_kernel(username, hostname):
    """Launch remote spyder-kernel and copy to local host."""
    kernel = SpyderKernel(username, hostname)
    kernel.copy()


if __name__ == "__main__":

    kernel = SpyderKernel("mcintos", "sdcc-login04.iter.org")
    kernel.launch()
    kernel.copy()
