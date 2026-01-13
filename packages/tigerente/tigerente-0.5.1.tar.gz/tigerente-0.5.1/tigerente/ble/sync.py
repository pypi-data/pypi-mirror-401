import asyncio
import base64
import hashlib
import logging
import math
import zlib
from pathlib import Path

from ..com.comm import Task, Tasks
from .bleio import BLEIOConnector


class UnexpectedResponseError(BaseException): ...


async def send_file(bleio: BLEIOConnector, file, task: Task | None = None):
    data = file.read()
    data = zlib.compress(data)
    data = base64.b64encode(data)
    if task is not None:
        await task.set_max(len(data))
    while True:
        await asyncio.sleep(0.001)
        chunk = data[:110]
        data = data[110:]
        if not chunk:
            break
        await bleio.send_packet(b"C", chunk)
        await bleio.expect_OK()
        if task is not None:
            await task.update(len(chunk))
    await bleio.send_packet(b"E")


async def sync_path(
    bleio: BLEIOConnector,
    file: Path,
    root_dir: Path,
    tasks: Tasks,
):
    path = file.relative_to(root_dir).as_posix()
    if path == ".":
        return

    if not file.exists():
        await bleio.send_packet(b"R", ("/" + path).encode())
    elif file.is_dir():
        await bleio.send_packet(b"D", ("/" + path).encode())
        await bleio.expect_OK()
    else:
        hashv = hashlib.sha256(file.read_bytes()).hexdigest()
        await bleio.send_packet(b"F", ("/" + path + " " + hashv).encode())
        while True:
            nxt, _ = await bleio.get_packet_wait()
            if nxt == b"K":
                break
            if nxt != b"U":
                logging.warning(
                    f"Expecting OK or Update Request, Invalid response {nxt}, resetting connection",
                )
                await bleio.send_packet(b"$")
                raise UnexpectedResponseError

            max_ = math.ceil(file.stat().st_size * (4 / 3))
            async with tasks.task(f"Sync file {path}...", max_, "B") as task:
                with file.open("rb") as f:
                    await send_file(bleio, f, task)


async def sync_dir(
    bleio: BLEIOConnector,
    dir: Path,
    tasks: Tasks,
    mode: str,
    paths: list[Path],
):
    if not paths:
        await bleio.send_packet(b"Y" + mode.encode("ascii"))
        await bleio.expect_OK()

    files = paths or tuple(dir.glob("**"))
    max_prog = len(files)
    async with tasks.task("Sync directory...", max_prog, "files") as task:
        for file in files:
            await sync_path(bleio, file, dir, tasks)
            await task.update(1)

    if not paths:
        await bleio.send_packet(b"N")
        await bleio.expect_OK()
