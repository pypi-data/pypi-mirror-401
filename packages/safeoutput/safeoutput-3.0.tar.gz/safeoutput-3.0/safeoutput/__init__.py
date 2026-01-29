from __future__ import annotations

import argparse
import logging
import sys
from os import rename
from os.path import abspath, dirname
from tempfile import NamedTemporaryFile
from typing import IO, Any, Callable, Literal, TypeVar, overload

LOG = logging.getLogger(__name__)

def _sameDir(dst: str) -> str:
    return dirname(abspath(dst))

@overload
def open(
    dst: str | None = None,
    mode: Literal["w"] = "w",
    useDir: Callable[[str], str] = _sameDir,
) -> SafeTextOutput: ...


@overload
def open(
    dst: str | None,
    mode: Literal["wb"],
    useDir: Callable[[str], str] = _sameDir,
) -> SafeBinaryOutput: ...


def open(
    dst: str | None = None,
    mode: Literal["w", "wb"] = "w",
    useDir: Callable[[str], str] = _sameDir,
) -> SafeTextOutput | SafeBinaryOutput:
    if dst:
        fd: IO[Any] = NamedTemporaryFile(dir=useDir(dst), mode=mode)
    else:
        if mode == "w":
            fd = sys.stdout
        else:
            fd = sys.stdout.buffer
    if mode == "wb":
        return SafeBinaryOutput(fd, dst)
    return SafeTextOutput(fd, dst)


T = TypeVar("T", str, bytes)


class _SafeOutputWrapper[T]:
    fd: IO[Any]
    dst: str | None

    def __init__(self, fd: IO[Any], dst: str | None) -> None:
        self.fd = fd
        self.dst = dst

    def __enter__(self) -> _SafeOutputWrapper[T]:
        if self.dst:
            self.fd.__enter__()
        return self

    def __getattr__(self, name: str) -> Any:
        # Attribute lookups are delegated to the underlying file
        fd = self.__dict__['fd']
        a = getattr(fd, name)
        return a

    def write(self, data: T) -> int:
        return self.fd.write(data)

    def flush(self) -> None:
        self.fd.flush()

    @property
    def name(self) -> str:
        return self.fd.name

    def close(self, commit: bool = True) -> None:
        if self.dst:
            if commit:
                LOG.debug("renaming %s to %s", self.fd.name, self.dst)
                self.fd.flush()
                rename(self.fd.name, self.dst)
            try:
                LOG.debug("closed %s", self.fd.name)
                self.fd.close()
            except OSError:
                pass

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> bool | None:
        self.close(exc_value is None)
        if self.dst:
            return self.fd.__exit__(exc_type, exc_value, traceback)
        else:
            return exc_type is None

    def __del__(self) -> None:
        # If we get to __del__ and have not already committed,
        # we don't know that the output is safe. Allow
        # tempfile to delete the file.
        self.close(False)


SafeTextOutput = _SafeOutputWrapper[str]
SafeBinaryOutput = _SafeOutputWrapper[bytes]


def main(argv: list[str] | None = None) -> None:
    """Buffer stdin and flush, and avoid incomplete files."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--binary',
                        dest='mode',
                        action='store_const',
                        const="wb",
                        default="w",
                        help='write in binary mode')
    parser.add_argument('output',
                        metavar='FILE',
                        type=str,
                        help='Output file')

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stderr,
        format='[%(levelname)s elapsed=%(relativeCreated)dms] %(message)s')

    args = parser.parse_args(argv or sys.argv[1:])

    with open(args.output, args.mode) as fd:
        for line in sys.stdin:
            fd.write(line)
