"""UV package manager wrapper for robust command execution."""

import subprocess
from pathlib import Path


class UvCommandError(Exception):
    """Error executing uv command."""

    def __init__(self, command: str, stderr: str, returncode: int):
        self.command = command
        self.stderr = stderr
        self.returncode = returncode
        super().__init__(f"Command '{command}' failed with code {returncode}: {stderr}")


class UvManager:
    """
    Manager for UV package manager commands.

    Provides a clean interface to uv commands, delegating package management
    to uv instead of handling it ourselves.

    Usage:
        uv = UvManager()
        uv.init_app("my_api", Path("src/apps"))
        uv.add_dependency("fastapi", dev=False)
        uv.sync()
    """

    def __init__(self, cwd: Path | None = None):
        """
        Initialize UV manager.

        Args:
            cwd: Working directory for commands (default: current directory)
        """
        self.cwd = cwd or Path.cwd()

    def _run(
        self,
        args: list[str],
        cwd: Path | None = None,
        check: bool = True,
        capture_output: bool = True,
    ) -> subprocess.CompletedProcess:
        """
        Run a uv command.

        Args:
            args: Command arguments (e.g., ["init", "--app"])
            cwd: Working directory (default: self.cwd)
            check: Raise error on failure
            capture_output: Capture stdout/stderr

        Returns:
            CompletedProcess result

        Raises:
            UvCommandError: If command fails and check=True
        """
        cmd = ["uv"] + args
        work_dir = cwd or self.cwd

        try:
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=capture_output,
                text=True,
                check=False,
            )

            if check and result.returncode != 0:
                raise UvCommandError(
                    command=" ".join(cmd),
                    stderr=result.stderr,
                    returncode=result.returncode,
                )

            return result

        except FileNotFoundError:
            raise UvCommandError(
                command=" ".join(cmd),
                stderr="uv command not found. Is uv installed?",
                returncode=127,
            )

    def init_app(self, name: str, destination: Path) -> Path:
        """
        Initialize a new application using uv init --app.

        Args:
            name: Application name
            destination: Parent directory

        Returns:
            Path to created application

        Raises:
            UvCommandError: If uv init fails
        """
        app_path = destination / name
        self._run(["init", "--app", name], cwd=destination)
        return app_path

    def init_lib(self, name: str, destination: Path) -> Path:
        """
        Initialize a new library using uv init --lib.

        Args:
            name: Library name
            destination: Parent directory

        Returns:
            Path to created library

        Raises:
            UvCommandError: If uv init fails
        """
        lib_path = destination / name
        self._run(["init", "--lib", name], cwd=destination)
        return lib_path

    def add_dependency(
        self,
        package: str,
        dev: bool = False,
        cwd: Path | None = None,
    ) -> None:
        """
        Add a dependency to the project.

        Args:
            package: Package name (can include version: "fastapi>=0.100.0")
            dev: Add to dev dependencies
            cwd: Working directory (default: self.cwd)

        Raises:
            UvCommandError: If uv add fails
        """
        args = ["add", package]
        if dev:
            args.insert(1, "--dev")

        work_dir = cwd or self.cwd
        self._run(args, cwd=work_dir)

    def add_dependencies(
        self,
        packages: list[str],
        dev: bool = False,
        cwd: Path | None = None,
    ) -> None:
        """
        Add multiple dependencies at once.

        Args:
            packages: List of package names
            dev: Add to dev dependencies
            cwd: Working directory (default: self.cwd)

        Raises:
            UvCommandError: If uv add fails
        """
        if not packages:
            return

        args = ["add"] + packages
        if dev:
            args.insert(1, "--dev")

        work_dir = cwd or self.cwd
        self._run(args, cwd=work_dir)

    def sync(self, cwd: Path | None = None) -> None:
        """
        Sync dependencies (install/update).

        Args:
            cwd: Working directory (default: self.cwd)

        Raises:
            UvCommandError: If uv sync fails
        """
        work_dir = cwd or self.cwd
        self._run(["sync"], cwd=work_dir)

    def remove_dependency(
        self,
        package: str,
        dev: bool = False,
        cwd: Path | None = None,
    ) -> None:
        """
        Remove a dependency from the project.

        Args:
            package: Package name
            dev: Remove from dev dependencies
            cwd: Working directory (default: self.cwd)

        Raises:
            UvCommandError: If uv remove fails
        """
        args = ["remove", package]
        if dev:
            args.insert(1, "--dev")

        work_dir = cwd or self.cwd
        self._run(args, cwd=work_dir)

    def run(
        self,
        command: str | list[str],
        cwd: Path | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess:
        """
        Run a command in the uv environment.

        Args:
            command: Command to run (string or list)
            cwd: Working directory (default: self.cwd)
            check: Raise error on failure

        Returns:
            CompletedProcess result

        Raises:
            UvCommandError: If command fails and check=True
        """
        if isinstance(command, str):
            args = ["run"] + command.split()
        else:
            args = ["run"] + command

        work_dir = cwd or self.cwd
        return self._run(args, cwd=work_dir, check=check)

    def get_python_path(self, cwd: Path | None = None) -> str:
        """
        Get the path to the Python interpreter in the uv environment.

        Args:
            cwd: Working directory (default: self.cwd)

        Returns:
            Path to Python interpreter

        Raises:
            UvCommandError: If uv run python fails
        """
        work_dir = cwd or self.cwd
        result = self._run(["run", "which", "python"], cwd=work_dir)
        return result.stdout.strip()
