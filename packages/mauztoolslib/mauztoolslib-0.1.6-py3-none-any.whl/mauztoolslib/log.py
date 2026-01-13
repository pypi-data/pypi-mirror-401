from datetime import datetime
from typing import Optional, Any
import traceback as _traceback
import copy as _copy
import enum


class FrozenLoggingError(Exception):
    pass


class Levels(enum.IntEnum):
    # Log-Level
    NOLEVEL = 0      # nichts loggen
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logging:
    def __init__(
        self,
        filename: Optional[str] = None,
        level: Levels = Levels.DEBUG,
        show_time: bool = True,
    ):
        self.filename = filename
        self.level = level
        self.show_time = show_time
        self._frozen = False

    # -------------------------------
    # Laufzeit-Konfiguration ändern
    # -------------------------------
    def changeConfig(
        self,
        *,
        filename: Optional[str] = None,
        level: Optional[Levels] = None,
        show_time: Optional[bool] = None,
    ) -> None:
        """Ändert die Logger-Konfiguration zur Laufzeit."""
        if self._frozen:
            raise FrozenLoggingError("Logger ist eingefroren")

        if filename is not None:
            self.filename = filename

        if level is not None:
            self.level = level

        if show_time is not None:
            self.show_time = show_time

    # -------------------------------
    # Intern
    # -------------------------------
    def _format(
        self,
        level_name: str,
        message: object,
        tb: Optional[str],
    ) -> str:
        parts: list[str] = []

        if self.show_time:
            parts.append(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

        parts.append(level_name)
        parts.append(str(message))

        if tb:
            parts.append(tb)

        return " - ".join(parts)

    def _write(self, text: str) -> None:
        if self.filename:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        else:
            print(text)

    def _log(
        self,
        level: Levels,
        level_name: str,
        message: object,
        tb: Optional[str] = None,
    ) -> None:
        # NOLEVEL = nichts loggen
        if self.level == Levels.NOLEVEL:
            return

        if level < self.level:
            return

        self._write(self._format(level_name, message, tb))

    # -------------------------------
    # Logging-Methoden
    # -------------------------------
    def debug(self, message: object) -> None:
        self._log(Levels.DEBUG, "DEBUG", message)

    def info(self, message: object) -> None:
        self._log(Levels.INFO, "INFO", message)

    def warning(self, message: object) -> None:
        self._log(Levels.WARNING, "WARNING", message)

    def error(
        self,
        message: object,
        *,
        exc: Exception | bool | None = None,
    ) -> None:
        tb = None
        if exc is True:
            tb = _traceback.format_exc()
        elif isinstance(exc, Exception):
            tb = "".join(
                _traceback.format_exception(
                    type(exc), exc, exc.__traceback__
                )
            )

        self._log(Levels.ERROR, "ERROR", message, tb)

    def critical(
        self,
        message: object,
        *,
        exc: Exception | bool | None = None,
    ) -> None:
        tb = None
        if exc is True:
            tb = _traceback.format_exc()
        elif isinstance(exc, Exception):
            tb = "".join(
                _traceback.format_exception(
                    type(exc), exc, exc.__traceback__
                )
            )

        self._log(Levels.CRITICAL, "CRITICAL", message, tb)

    # -------------------------------
    # Repr / Str
    # -------------------------------
    def __str__(self) -> str:
        return (
            f"Logging("
            f"level={self.level.name}, "
            f"filename={self.filename!r}, "
            f"show_time={self.show_time}"
            f")"
        )

    def __repr__(self) -> str:
        return (
            f"<Logging "
            f"level={self.level.name} "
            f"filename={self.filename!r} "
            f"show_time={self.show_time}>"
        )

    # -------------------------------
    # Utilities
    # -------------------------------
    def copy(self) -> "Logging":
        """Gibt eine Kopie der Logger-Konfiguration zurück."""
        return _copy.deepcopy(self)

    def switch_freeze(self) -> None:
        """Schaltet das Einfrieren der Konfiguration um."""
        self._frozen = not self._frozen

    def is_frozen(self) -> bool:
        return self._frozen

    def as_dict(self) -> dict[str, Any]:
        """Exportiert die aktuelle Logger-Konfiguration."""
        return {
            "filename": self.filename,
            "level": self.level,
            "show_time": self.show_time,
            "frozen": self._frozen,
        }
