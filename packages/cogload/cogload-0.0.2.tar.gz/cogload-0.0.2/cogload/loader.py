import sys
from typing import TYPE_CHECKING, Callable
from functools import wraps
from pathlib import Path
import logging

if TYPE_CHECKING:
    from discord.ext import commands


_CEND = "\33[0m"
_CBOLD = "\33[1m"
_CGREEN = "\33[32m"
_CYELLOW = "\33[33m"
_CRED = "\33[31m"


def _green(m: str, t: str) -> str:
    return f"{_CBOLD}{_CGREEN}[{m}]{_CEND} {t}"


def _yellow(m: str, t: str) -> str:
    return f"{_CBOLD}{_CYELLOW}[{m}]{_CEND} {t}"


def _red(m: str, t: str) -> str:
    return f"{_CBOLD}{_CRED}[{m}]{_CEND} {t}"


def _make_logger(enabled: bool) -> logging.Logger:
    logger = logging.getLogger("cogloader")

    if not enabled:
        logger.disabled = True
        return logger

    logger.disabled = False
    logger.setLevel(logging.INFO)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
        logger.addHandler(handler)

    return logger


def _dotted_extension(root: str, file: Path) -> str:
    relative = file.with_suffix("").relative_to(root)
    return ".".join((root, *relative.parts))


async def preload_cogs(
    bot: commands.Bot,
    *,
    path: str,
    logger: logging.Logger,
):
    root = Path(path)

    if not root.exists():
        raise FileNotFoundError(f"Cog directory '{root.resolve()}' does not exist")

    found_files = 0
    loaded_cogs = 0

    for file in root.rglob("*.py"):
        found_files += 1
        if file.name.startswith("_"):
            continue

        ext = _dotted_extension(path, file)

        try:
            await bot.load_extension(ext)
        except commands.ExtensionAlreadyLoaded:
            logger.info(_yellow("SKIPPED", ext))
        except commands.NoEntryPointError:
            logger.warning(_yellow("SKIPPED", f"{ext} is missing setup()"))
        except commands.ExtensionFailed:
            logger.warning(_red("FAILED", ext))
            raise
        else:
            logger.info(_green("LOADED", ext))
            loaded_cogs += 1

    if found_files == 0:
        logger.warning(f"Cog directory {_CBOLD}'{path}'{_CEND} has no .py files")

    elif loaded_cogs == 0:
        logger.warning(f"Cog directory {_CBOLD}'{path}'{_CEND} has no cogs")

    else:
        logger.info(
            f"{_CBOLD}Successfully loaded {loaded_cogs} cog{'s' if loaded_cogs != 1 else ''}{_CEND}"
        )


def load(*, path: str = "cogs", use_logger: bool = True, color: bool = True):
    """
    Decorator that attaches to `on_ready` event (or similar) of a `commands.Bot` subclass. Preloads all cogs before continuing.

    ### Example
    ```
        class Bot(commands.Bot):
            def __init__(self):
                super().__init__(...)

            @load(path="cogs", use_logger=True)
            async def on_ready(self):
                pass
    ```

    Parameters
    ----------
    path
        The relative path of the directory where cog files reside.
    use_logger
        Whether to use the built-in logger (stdout).
    color
        Whether the built-in logger should use ANSI colors.
    """

    if color is False:
        global _CEND, _CBOLD, _CGREEN, _CYELLOW, _CRED
        _CEND = _CBOLD = _CGREEN = _CYELLOW = _CRED = ""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self: commands.Bot, *args, **kwargs):
            if not getattr(self, "_cogs_preloaded", False):
                logger = _make_logger(use_logger)
                await preload_cogs(self, path=path, logger=logger)
                setattr(self, "_cogs_preloaded", True)

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator
