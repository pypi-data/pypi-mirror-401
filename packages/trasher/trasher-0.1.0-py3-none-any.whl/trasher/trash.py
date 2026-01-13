from __future__ import annotations

import errno
import os
import pwd
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import typer
from rich.console import Console
from rich.prompt import Confirm


out_console = Console()
err_console = Console(stderr=True)


@dataclass(frozen=True)
class TrashContext:
    uid: int
    home: Path
    home_dev: int


def _invoking_uid() -> int:
    sudo_uid = os.environ.get("SUDO_UID")
    if sudo_uid:
        try:
            return int(sudo_uid)
        except ValueError:
            pass
    return os.getuid()


def _home_for_uid(uid: int) -> Path:
    return Path(pwd.getpwuid(uid).pw_dir)


def _path_lstat(path: Path) -> os.stat_result:
    return os.lstat(path)


def _is_dir_no_follow(path: Path, st: os.stat_result | None = None) -> bool:
    st = st or _path_lstat(path)
    return stat.S_ISDIR(st.st_mode)


def _find_mount_point(path: Path) -> Path:
    absolute_path = path.absolute()
    try:
        st = _path_lstat(absolute_path)
    except FileNotFoundError:
        raise

    if _is_dir_no_follow(absolute_path, st=st):
        current = absolute_path
        dev = st.st_dev
    else:
        current = absolute_path.parent
        dev = _path_lstat(current).st_dev

    while True:
        parent = current.parent
        if parent == current:
            return current
        if _path_lstat(parent).st_dev != dev:
            return current
        current = parent


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _unique_destination(trash_dir: Path, name: str) -> Path:
    candidate = trash_dir / name
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    for i in range(1, 10_000):
        numbered = trash_dir / f"{stem} ({i}){suffix}"
        if not numbered.exists():
            return numbered

    raise RuntimeError(f"Unable to find unique destination for {name!r} in {trash_dir}")


def _trash_dir_for_path(path: Path, ctx: TrashContext) -> Path:
    is_macos = os.uname().sysname == "Darwin"
    if not is_macos:
        return ctx.home / ".trash"

    try:
        source_dev = _path_lstat(path).st_dev
    except FileNotFoundError:
        source_dev = None

    if source_dev is not None and source_dev == ctx.home_dev:
        return ctx.home / ".Trash"

    mount_point = _find_mount_point(path)
    return mount_point / ".Trashes" / str(ctx.uid)


def _move_into_trash(src: Path, ctx: TrashContext) -> Path:
    trash_dir = _trash_dir_for_path(src, ctx)
    try:
        _ensure_dir(trash_dir)
    except PermissionError:
        fallback = ctx.home / ".Trash"
        try:
            _ensure_dir(fallback)
            trash_dir = fallback
        except PermissionError:
            trash_dir = ctx.home / ".trash"
            _ensure_dir(trash_dir)

    destination = _unique_destination(trash_dir, src.name)

    try:
        os.rename(src, destination)
        return destination
    except OSError as e:
        if e.errno not in (errno.EXDEV, errno.EACCES, errno.EPERM):
            raise

    shutil.move(str(src), str(destination))
    return destination


def trash_paths(
    paths: Iterable[str],
    *,
    recursive: bool,
    force: bool,
    interactive: bool,
    dry_run: bool,
    verbose: bool,
) -> None:
    uid = _invoking_uid()
    home = _home_for_uid(uid)
    ctx = TrashContext(
        uid=uid,
        home=home,
        home_dev=_path_lstat(home).st_dev,
    )

    if force:
        interactive = False

    had_error = False
    for raw in paths:
        path = Path(os.path.expandvars(os.path.expanduser(raw)))

        raw_clean = raw.strip()
        if raw_clean == "" or Path(raw_clean) in {Path("."), Path("..")}:
            err_console.print(f"[red]trash:[/red] refusing to trash {raw!r}")
            had_error = True
            continue

        if os.path.normpath(str(path.absolute())) == "/":
            err_console.print("[red]trash:[/red] refusing to trash '/'")
            had_error = True
            continue

        try:
            st = _path_lstat(path)
        except FileNotFoundError:
            if force:
                continue
            err_console.print(f"[red]trash:[/red] {raw}: No such file or directory")
            had_error = True
            continue
        except PermissionError:
            err_console.print(f"[red]trash:[/red] {raw}: Permission denied")
            had_error = True
            continue

        if _is_dir_no_follow(path, st=st) and not recursive:
            err_console.print(
                f"[red]trash:[/red] {raw}: is a directory (use [bold]-r[/bold])"
            )
            had_error = True
            continue

        if interactive and not Confirm.ask(
            f"Trash {raw!r}?", default=False, console=err_console
        ):
            continue

        trash_dir = _trash_dir_for_path(path, ctx)
        destination = _unique_destination(trash_dir, path.name)

        if dry_run:
            if verbose:
                out_console.print(f"{path} -> {destination}")
            continue

        try:
            destination = _move_into_trash(path, ctx)
        except FileNotFoundError:
            if force:
                continue
            err_console.print(f"[red]trash:[/red] {raw}: No such file or directory")
            had_error = True
            continue
        except Exception as e:  # noqa: BLE001
            err_console.print(f"[red]trash:[/red] {raw}: {e}")
            had_error = True
            continue

        if verbose:
            out_console.print(f"{path} -> {destination}")

    if had_error:
        raise typer.Exit(code=1)
