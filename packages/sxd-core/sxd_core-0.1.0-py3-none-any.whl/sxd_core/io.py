"""
Context-Aware I/O Module

Drop-in replacements for standard library I/O operations that automatically
route through the simulation runtime when in simulation mode.

Usage:
    # Instead of:
    import os
    import time
    import subprocess

    # Use:
    from sxd_core import io

    # Then replace:
    #   os.path.getsize(path)  ->  io.getsize(path)
    #   time.time()            ->  io.time()
    #   subprocess.run(...)    ->  io.run(...)
    #   open(path, 'rb')       ->  io.open_file(path, 'rb')

In production (no simulation context), these call the real implementations.
In simulation (within simulation_context), they route through the Runtime.
"""

from __future__ import annotations

import os as _os
import subprocess as _subprocess
import time as _time
import shutil as _shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any, Iterator, cast
from io import BytesIO as _BytesIO
from uuid import uuid4 as _uuid4

from sxd_core.simulation.context import get_runtime

link = _os.link
disk_usage = _shutil.disk_usage


def BytesIO(*args, **kwargs) -> _BytesIO:
    """Simulation-aware BytesIO (currently just a wrapper)."""
    return _BytesIO(*args, **kwargs)


# =============================================================================
# Time Operations
# =============================================================================


def time() -> float:
    """
    Return current time in seconds since epoch.

    Equivalent to time.time() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _time.time()
    return rt.clock.now_ns() / 1e9


def time_ns() -> int:
    """
    Return current time in nanoseconds since epoch.

    Equivalent to time.time_ns() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _time.time_ns()
    return rt.clock.now_ns()


def monotonic() -> float:
    """
    Return monotonic clock time in seconds.

    Equivalent to time.monotonic() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _time.monotonic()
    return rt.clock.monotonic()


def sleep(seconds: float) -> None:
    """
    Sleep for specified seconds.

    In simulation mode, this advances the clock instead of blocking.
    """
    rt = get_runtime()
    if rt is None:
        _time.sleep(seconds)
    else:
        # In simulation, advance clock by sleep duration
        rt.clock.advance(int(seconds * 1e9))


def now(tz: timezone | None = None) -> datetime:
    """
    Return current datetime.

    Equivalent to datetime.now() but simulation-aware.
    Defaults to UTC timezone.
    """
    rt = get_runtime()
    if rt is None:
        return datetime.now(tz or timezone.utc)
    return rt.clock.now_datetime()


def now_iso() -> str:
    """
    Return current time as ISO 8601 string.

    Simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return datetime.now(timezone.utc).isoformat()
    return rt.clock.now_iso()


# =============================================================================
# Random/UUID Operations
# =============================================================================


def uuid4() -> str:
    """
    Generate a UUID4 string.

    In simulation mode, uses deterministic RNG for reproducibility.
    """
    rt = get_runtime()
    if rt is None:
        return str(_uuid4())
    return rt.rng.uuid4()


def random() -> float:
    """
    Return random float in [0, 1).

    In simulation mode, uses deterministic RNG for reproducibility.
    """
    rt = get_runtime()
    if rt is None:
        import random as _random

        return _random.random()
    return rt.rng.random()


def randint(a: int, b: int) -> int:
    """
    Return random integer in [a, b] inclusive.

    In simulation mode, uses deterministic RNG for reproducibility.
    """
    rt = get_runtime()
    if rt is None:
        import random as _random

        return _random.randint(a, b)
    return rt.rng.randint(a, b)


# =============================================================================
# Environment Operations
# =============================================================================


def getenv(key: str, default: str | None = None) -> str | None:
    """
    Get an environment variable.

    Simulation-aware replacement for os.getenv().
    """
    rt = get_runtime()
    if rt is None:
        return _os.getenv(key, default)
    return rt.env.get(key, default)


def get_env() -> dict[str, str]:
    """
    Get all environment variables.

    Simulation-aware replacement for os.environ.
    """
    rt = get_runtime()
    if rt is None:
        return dict(_os.environ)
    return rt.env.copy()


def set_env(key: str, value: str) -> None:
    """
    Set an environment variable.

    Simulation-aware replacement for os.environ[key] = value.
    Note: In simulation, this only affects the current node's runtime.
    """
    rt = get_runtime()
    if rt is None:
        _os.environ[key] = value
    else:
        rt.env[key] = value


# =============================================================================
# File Operations
# =============================================================================


def getsize(path: str | Path) -> int:
    """
    Return size of file in bytes.

    Equivalent to os.path.getsize() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _os.path.getsize(str(path))
    size = rt.disk.size(str(path))
    if size is None:
        raise FileNotFoundError(f"No such file: {path}")
    return size


def exists(path: str | Path) -> bool:
    """
    Check if path exists.

    Equivalent to os.path.exists() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _os.path.exists(str(path))
    return rt.disk.exists(str(path))


def isfile(path: str | Path) -> bool:
    """
    Check if path is a file.

    Equivalent to os.path.isfile() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _os.path.isfile(str(path))
    return rt.disk.is_file(str(path))


def isdir(path: str | Path) -> bool:
    """
    Check if path is a directory.

    Equivalent to os.path.isdir() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _os.path.isdir(str(path))
    return rt.disk.is_dir(str(path))


def listdir(path: str | Path) -> list[str]:
    """
    List directory contents.

    Equivalent to os.listdir() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _os.listdir(str(path))
    return rt.disk.list_dir(str(path))


def makedirs(path: str | Path, exist_ok: bool = False) -> None:
    """
    Create directory and parents.

    Equivalent to os.makedirs() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _os.makedirs(str(path), exist_ok=exist_ok)
    else:
        rt.disk.mkdir(str(path), parents=True)
        # DiskResult.OK is fine, ignore for exist_ok semantics


def remove(path: str | Path) -> None:
    """
    Remove a file.

    Equivalent to os.remove() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _os.remove(str(path))
    else:
        from sxd_core.simulation.runtime import DiskResult

        result = rt.disk.delete(str(path))
        if result == DiskResult.NOT_FOUND:
            raise FileNotFoundError(f"No such file: {path}")


def rename(src: str | Path, dst: str | Path) -> None:
    """
    Rename/move a file.

    Equivalent to os.rename() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _os.rename(str(src), str(dst))
    else:
        from sxd_core.simulation.runtime import DiskResult

        result = rt.disk.rename(str(src), str(dst))
        if result == DiskResult.NOT_FOUND:
            raise FileNotFoundError(f"No such file: {src}")


def link(src: str | Path, dst: str | Path) -> None:
    """
    Create a hard link.

    Equivalent to os.link() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _os.link(str(src), str(dst))
    else:
        from sxd_core.simulation.runtime import DiskResult

        result = rt.disk.link(str(src), str(dst))
        if result == DiskResult.NOT_FOUND:
            raise FileNotFoundError(f"No such file: {src}")
        if result != DiskResult.OK:
            raise IOError(f"Failed to link {src} to {dst}: {result}")


def disk_usage(path: str | Path) -> Any:
    """
    Get disk usage statistics.

    Equivalent to shutil.disk_usage() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _shutil.disk_usage(str(path))
    return rt.disk.disk_usage(str(path))


def glob(pattern: str, root: str | Path = ".") -> list[str]:
    """
    Find files matching glob pattern.

    Simulation-aware glob.
    """
    rt = get_runtime()
    if rt is None:
        from pathlib import Path as P

        return [str(p) for p in P(root).glob(pattern)]

    # Simulation mode: combine root and pattern
    root_str = str(root)
    full_pattern = _os.path.join(root_str, pattern)
    return rt.disk.glob(full_pattern)


def rglob(path: str | Path, pattern: str = "*") -> list[str]:
    """
    Recursive glob - find all files matching pattern under path.

    Simulation-aware version of Path.rglob().

    In simulation mode, recursively walks the simulated filesystem.
    """
    rt = get_runtime()
    if rt is None:
        from pathlib import Path as P

        return [str(p) for p in P(path).rglob(pattern)]

    # Simulation mode: recursive walk
    import fnmatch

    results = []
    path_str = str(path)

    def _walk(dir_path: str):
        if not rt.disk.is_dir(dir_path):
            return
        for entry in rt.disk.list_dir(dir_path):
            full_path = f"{dir_path}/{entry}" if dir_path != "/" else f"/{entry}"
            if rt.disk.is_dir(full_path):
                _walk(full_path)
            elif fnmatch.fnmatch(entry, pattern):
                results.append(full_path)

    _walk(path_str)
    return results


def walk(path: str | Path) -> list[tuple[str, list[str], list[str]]]:
    """
    Walk directory tree.

    Simulation-aware version of os.walk().

    Returns list of (dirpath, dirnames, filenames) tuples.
    """
    import os as _os

    rt = get_runtime()
    if rt is None:
        return list(_os.walk(str(path)))

    # Simulation mode: recursive walk
    results = []
    path_str = str(path)

    def _walk(dir_path: str):
        if not rt.disk.is_dir(dir_path):
            return
        dirs = []
        files = []
        for entry in rt.disk.list_dir(dir_path):
            full_path = f"{dir_path}/{entry}" if dir_path != "/" else f"/{entry}"
            if rt.disk.is_dir(full_path):
                dirs.append(entry)
            else:
                files.append(entry)
        results.append((dir_path, dirs, files))
        for d in dirs:
            child_path = f"{dir_path}/{d}" if dir_path != "/" else f"/{d}"
            _walk(child_path)

    _walk(path_str)
    return results


def read_bytes(path: str | Path) -> bytes:
    """
    Read entire file as bytes.

    Equivalent to Path(path).read_bytes() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return Path(path).read_bytes()
    from sxd_core.simulation.runtime import DiskResult

    data, result = rt.disk.read(str(path))
    if result != DiskResult.OK:
        if result == DiskResult.NOT_FOUND:
            raise FileNotFoundError(f"No such file: {path}")
        raise IOError(f"Failed to read {path}: {result}")
    return data or b""


def write_bytes(path: str | Path, data: bytes, fsync: bool = False) -> None:
    """
    Write bytes to file.

    Equivalent to Path(path).write_bytes() but simulation-aware.

    Args:
        path: File path
        data: Bytes to write
        fsync: If True, fsync after write (important for durability in simulation)
    """
    rt = get_runtime()
    if rt is None:
        Path(path).write_bytes(data)
        if fsync:
            # Real fsync
            import os

            fd = os.open(str(path), os.O_RDWR)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
    else:
        from sxd_core.simulation.runtime import DiskResult

        result = rt.disk.write(str(path), data)
        if result != DiskResult.OK:
            raise IOError(f"Failed to write {path}: {result}")
        if fsync:
            rt.disk.fsync(str(path))


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """
    Read entire file as text.

    Equivalent to Path(path).read_text() but simulation-aware.
    """
    return read_bytes(path).decode(encoding)


def write_text(
    path: str | Path, text: str, encoding: str = "utf-8", fsync: bool = False
) -> None:
    """
    Write text to file.

    Equivalent to Path(path).write_text() but simulation-aware.
    """
    write_bytes(path, text.encode(encoding), fsync=fsync)


def fsync(path: str | Path) -> None:
    """
    Sync file to disk.

    In simulation, marks the file as durable (survives crashes).
    """
    rt = get_runtime()
    if rt is None:
        fd = _os.open(str(path), _os.O_RDWR)
        try:
            _os.fsync(fd)
        finally:
            _os.close(fd)
    else:
        rt.disk.fsync(str(path))


class SimulationFile:
    """
    File-like object for simulation mode.

    Provides a subset of file operations needed for common patterns.
    """

    def __init__(self, path: str, mode: str, runtime):
        self.path = path
        self.mode = mode
        self.runtime = runtime
        self._pos = 0
        self._buffer = b""
        self._closed = False

        if "r" in mode:
            from sxd_core.simulation.runtime import DiskResult

            data, result = runtime.disk.read(path)
            if result == DiskResult.NOT_FOUND:
                raise FileNotFoundError(f"No such file: {path}")
            if result != DiskResult.OK:
                raise IOError(f"Failed to read {path}: {result}")
            self._buffer = data or b""
        elif "w" in mode:
            self._buffer = b""
        elif "a" in mode:
            from sxd_core.simulation.runtime import DiskResult

            data, result = runtime.disk.read(path)
            if result == DiskResult.OK:
                self._buffer = data or b""
            else:
                self._buffer = b""
            self._pos = len(self._buffer)

    def read(self, size: int = -1) -> bytes:
        if self._closed:
            raise ValueError("I/O operation on closed file")
        if size < 0:
            data = self._buffer[self._pos :]
            self._pos = len(self._buffer)
        else:
            data = self._buffer[self._pos : self._pos + size]
            self._pos += len(data)
        return data

    def write(self, data: bytes) -> int:
        if self._closed:
            raise ValueError("I/O operation on closed file")
        if "a" in self.mode:
            self._buffer += data
            self._pos = len(self._buffer)
        else:
            # Insert/overwrite at current position
            before = self._buffer[: self._pos]
            after = self._buffer[self._pos + len(data) :]
            self._buffer = before + data + after
            self._pos += len(data)
        return len(data)

    def seek(self, pos: int, whence: int = 0) -> int:
        if whence == 0:  # SEEK_SET
            self._pos = pos
        elif whence == 1:  # SEEK_CUR
            self._pos += pos
        elif whence == 2:  # SEEK_END
            self._pos = len(self._buffer) + pos
        return self._pos

    def tell(self) -> int:
        return self._pos

    def flush(self) -> None:
        if "w" in self.mode or "a" in self.mode:
            self.runtime.disk.write(self.path, self._buffer)

    def close(self) -> None:
        if not self._closed:
            self.flush()
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __iter__(self) -> Iterator[bytes]:
        return self

    def __next__(self) -> bytes:
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    # Expose exception
    CalledProcessError = _subprocess.CalledProcessError

    @property
    def closed(self) -> bool:
        return self._closed

    def readable(self) -> bool:
        return "r" in self.mode or "+" in self.mode

    def writable(self) -> bool:
        return "w" in self.mode or "a" in self.mode or "+" in self.mode

    def seekable(self) -> bool:
        return True

    def readline(self, size: int = -1) -> bytes:
        if self._closed:
            raise ValueError("I/O operation on closed file")
        start = self._pos
        end = self._buffer.find(b"\n", start)
        if end == -1:
            end = len(self._buffer)
        else:
            end += 1  # Include newline
        if size >= 0:
            end = min(end, start + size)
        self._pos = end
        return self._buffer[start:end]


def open_file(
    path: str | Path,
    mode: str = "r",
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> IO:
    """
    Open a file.

    Equivalent to open() but simulation-aware.
    Returns a file-like object.

    Note: In simulation mode, only binary modes are fully supported.
    Text mode wraps binary mode with encoding/decoding.
    """
    rt = get_runtime()
    if rt is None:
        return open(str(path), mode, buffering, encoding, errors, newline)

    # Simulation mode
    binary = "b" in mode
    if not binary:
        # Wrap in text mode
        import io

        binary_mode = mode.replace("t", "") + "b"
        if "b" not in binary_mode:
            binary_mode += "b"
        binary_file = SimulationFile(str(path), binary_mode, rt)
        wrapper = io.TextIOWrapper(cast(Any, binary_file), encoding=encoding or "utf-8")
        return cast(Any, wrapper)

    return cast(Any, SimulationFile(str(path), mode, rt))


# Expose exception
CalledProcessError = _subprocess.CalledProcessError
TimeoutExpired = _subprocess.TimeoutExpired
PIPE = _subprocess.PIPE
STDOUT = _subprocess.STDOUT
DEVNULL = _subprocess.DEVNULL

# =============================================================================
# Subprocess Operations
# =============================================================================


class ProcessResult:
    """Result of a completed process, compatible with subprocess.CompletedProcess."""

    def __init__(self, returncode: int, stdout: Any, stderr: Any, args: list[str]):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.args = args

    def check_returncode(self) -> None:
        if self.returncode != 0:
            raise _subprocess.CalledProcessError(
                self.returncode, self.args, self.stdout, self.stderr
            )


def run(
    args: list[str],
    *,
    capture_output: bool = False,
    timeout: float | None = None,
    check: bool = False,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    input: bytes | None = None,
    text: bool = False,
    **kwargs,
) -> ProcessResult | _subprocess.CompletedProcess:
    """
    Run a subprocess.

    Equivalent to subprocess.run() but simulation-aware.

    In simulation mode, uses the mocked process implementation from Runtime.
    """
    rt = get_runtime()
    if rt is None:
        return _subprocess.run(
            args,
            capture_output=capture_output,
            timeout=timeout,
            check=check,
            cwd=cwd,
            env=env,
            input=input,
            text=text,
            **kwargs,
        )

    # Simulation mode
    result = rt.process.run(
        args,
        capture_output=True,  # Always capture in sim so we can write to file if needed
        timeout=timeout,
        cwd=cwd,
        env=env,
    )

    stdout = result.stdout
    stderr = result.stderr

    # Handle stdout redirection
    stdout_arg = kwargs.get("stdout")
    if stdout_arg and hasattr(stdout_arg, "write") and stdout:
        stdout_arg.write(stdout)

    if text:
        # Decode if text requested
        encoding = kwargs.get("encoding", "utf-8")
        errors = kwargs.get("errors", "strict")
        if stdout is not None:
            stdout = cast(Any, stdout).decode(encoding, errors)
        if stderr is not None:
            stderr = cast(Any, stderr).decode(encoding, errors)

    proc_result = ProcessResult(
        returncode=result.returncode,
        stdout=stdout,
        stderr=stderr,
        args=args,
    )

    if check:
        proc_result.check_returncode()

    return cast(Any, proc_result)


class SimulatedPopen:
    """
    Simulated Popen object for simulation mode.

    Mimics subprocess.Popen but executes via simulation runtime.
    Since simulation is synchronous, the process is already "done" upon creation.
    """

    def __init__(
        self,
        args: list[str],
        stdout=None,
        stderr=None,
        text=False,
        encoding="utf-8",
        errors="strict",
        **kwargs,
    ):
        self.args = args
        self.text = text
        self.encoding = encoding or "utf-8"
        self.errors = errors or "strict"
        self.returncode = None
        self._stdout_data: Any = None
        self._stderr_data: Any = None

        rt = get_runtime()
        assert rt is not None
        # Execute immediately in simulation
        result = rt.process.run(args, capture_output=True, **kwargs)

        self.returncode = result.returncode
        self._stdout_data = result.stdout or b""
        self._stderr_data = result.stderr or b""

        # Prepare output streams
        if text:
            if isinstance(self._stdout_data, bytes):
                self._stdout_data = self._stdout_data.decode(self.encoding, self.errors)
            if isinstance(self._stderr_data, bytes):
                self._stderr_data = self._stderr_data.decode(self.encoding, self.errors)

            from io import StringIO

            self.stdout = cast(
                Any, StringIO(self._stdout_data) if stdout == PIPE else None
            )
            self.stderr = cast(
                Any, StringIO(self._stderr_data) if stderr == PIPE else None
            )
        else:
            from io import BytesIO

            self.stdout = cast(
                Any, BytesIO(self._stdout_data) if stdout == PIPE else None
            )
            self.stderr = cast(
                Any, BytesIO(self._stderr_data) if stderr == PIPE else None
            )

        # For simulation of long-running processes, we could add delay support here
        # But for now, we assume instant completion (poll returns returncode immediately)

    def poll(self) -> int | None:
        return self.returncode

    def wait(self, timeout: float | None = None) -> int | None:
        return self.returncode

    def communicate(self, input: bytes | None = None, timeout: float | None = None):
        return (
            self.stdout.read() if self.stdout else None,
            self.stderr.read() if self.stderr else None,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def which(cmd: str, mode: int = _os.F_OK, path: str | None = None) -> str | None:
    """
    Find executable in path.

    Equivalent to shutil.which() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _shutil.which(cmd, mode, path)
    else:
        # In simulation, we check if any mock handles this command
        if rt.process._match_command([cmd]):
            return cmd
        return None


def Popen(
    args: list[str],
    stdout=None,
    stderr=None,
    shell: bool = False,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    text: bool = False,
    encoding: str | None = None,
    errors: str | None = None,
    **kwargs,
) -> SimulatedPopen | _subprocess.Popen:
    """
    Open a subprocess.

    Equivalent to subprocess.Popen() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _subprocess.Popen(
            args,
            stdout=stdout,
            stderr=stderr,
            shell=shell,
            cwd=cwd,
            env=env,
            text=text,
            encoding=encoding,
            errors=errors,
            **kwargs,
        )

    return SimulatedPopen(
        args,
        stdout=stdout,
        stderr=stderr,
        text=text,
        encoding=encoding or "utf-8",
        errors=errors or "strict",
        cwd=cwd,
        env=env,
        **kwargs,
    )
def rmtree(path: str | Path, ignore_errors: bool = False) -> None:
    """
    Remove a directory tree.

    Equivalent to shutil.rmtree() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _shutil.rmtree(str(path), ignore_errors=ignore_errors)
    else:
        # Simple recursive delete for simulation
        path_str = str(path)
        if not rt.disk.is_dir(path_str):
            if not ignore_errors:
                raise FileNotFoundError(f"No such directory: {path_str}")
            return

        # List all files and subdirs under this path
        def _delete_recursive(p: str):
            for entry in rt.disk.list_dir(p):
                full = f"{p}/{entry}" if p != "/" else f"/{entry}"
                if rt.disk.is_dir(full):
                    _delete_recursive(full)
                    rt.disk.rmdir(full)
                else:
                    rt.disk.delete(full)

        _delete_recursive(path_str)
        rt.disk.rmdir(path_str)


def copy2(src: str | Path, dst: str | Path) -> None:
    """
    Copy a file with metadata.

    Equivalent to shutil.copy2() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _shutil.copy2(str(src), str(dst))
    else:
        data = read_bytes(src)
        write_bytes(dst, data)


def make_archive(
    base_name: str, format: str, root_dir: str | Path, base_dir: str | Path | None = None
) -> str:
    """
    Create an archive file.

    Equivalent to shutil.make_archive() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        return _shutil.make_archive(
            base_name,
            format,
            str(root_dir),
            base_dir=str(base_dir) if base_dir else None,
        )
    else:
        # In simulation, we simulate an archive by copying files to a hidden location
        archive_path = f"{base_name}.{format}"
        archive_store = f"/.sim_archives/{base_name}"
        makedirs(archive_store, exist_ok=True)

        for f in rglob(root_dir):
            rel_path = _os.path.relpath(f, str(root_dir))
            dest = f"{archive_store}/{rel_path}"
            makedirs(_os.path.dirname(dest), exist_ok=True)
            copy2(f, dest)

        # Write a marker file so exists() returns True
        write_text(archive_path, f"SIM_ARCHIVE:{archive_store}")
        return archive_path


def unpack_archive(filename: str | Path, extract_dir: str | Path | None = None) -> None:
    """
    Unpack an archive file.

    Equivalent to shutil.unpack_archive() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _shutil.unpack_archive(
            str(filename), extract_dir=str(extract_dir) if extract_dir else None
        )
    else:
        # Read the marker to find the store
        marker_content = read_text(filename)
        if not marker_content.startswith("SIM_ARCHIVE:"):
            raise IOError(f"Not a simulated archive: {filename}")

        archive_store = marker_content.split(":", 1)[1]
        dest_dir = str(extract_dir) if extract_dir else "."
        makedirs(dest_dir, exist_ok=True)

        for f in rglob(archive_store):
            rel_path = _os.path.relpath(f, archive_store)
            dest = f"{dest_dir}/{rel_path}"
            makedirs(_os.path.dirname(dest), exist_ok=True)
            copy2(f, dest)


def chmod(path: str | Path, mode: int) -> None:
    """
    Change file permissions.

    Equivalent to os.chmod() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _os.chmod(str(path), mode)
    else:
        # In simulation, we don't strictly enforce permissions yet
        pass


def chown(path: str | Path, user: str, group: str) -> None:
    """
    Change file ownership.

    Equivalent to os.chown() but simulation-aware.
    """
    rt = get_runtime()
    if rt is None:
        _os.chown(str(path), user, group)
    else:
        # In simulation, we don't strictly enforce ownership yet
        pass
