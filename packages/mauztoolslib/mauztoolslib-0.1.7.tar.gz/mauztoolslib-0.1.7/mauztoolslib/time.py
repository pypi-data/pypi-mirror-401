import time
import threading
from typing import Callable, Optional, List


class Timer:
    """Ein einfacher Timer für Start, Stop, Reset, Zwischenzeiten und Wartefunktion."""

    def __init__(self, auto_start: bool = False):
        self._start_time: float | None = None
        self._elapsed: float = 0.0
        self._running: bool = False
        self._laps: list[float] = []

        if auto_start:
            self.start()

    # -------------------------------
    # Start / Stop / Pause / Reset
    # -------------------------------
    def start(self) -> None:
        if not self._running:
            self._start_time = time.perf_counter()
            self._running = True

    def pause(self) -> None:
        if self._running:
            self._elapsed += time.perf_counter() - self._start_time
            self._start_time = None
            self._running = False

    def stop(self) -> None:
        self.pause()

    def reset(self) -> None:
        self._start_time = time.perf_counter() if self._running else None
        self._elapsed = 0.0
        self._laps.clear()

    # -------------------------------
    # Zeitabfrage
    # -------------------------------
    def elapsed(self) -> float:
        if self._running:
            return self._elapsed + (time.perf_counter() - self._start_time)
        return self._elapsed

    def lap(self) -> float:
        current = self.elapsed()
        self._laps.append(current)
        return current

    def laps(self) -> List[float]:
        return self._laps.copy()

    # -------------------------------
    # Formatierte Zeit
    # -------------------------------
    def formatted(self) -> str:
        total = self.elapsed()
        hours, rem = divmod(total, 3600)
        minutes, rem = divmod(rem, 60)
        seconds, ms = divmod(rem, 1)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(ms*1000):03d}"

    # -------------------------------
    # Statische Wait
    # -------------------------------
    @staticmethod
    def wait(sec: float) -> None:
        time.sleep(sec)

    # -------------------------------
    # Str / Repr
    # -------------------------------
    def __str__(self) -> str:
        return f"Timer(elapsed={self.elapsed():.4f}s, running={self._running})"

    def __repr__(self) -> str:
        return f"<Timer elapsed={self.elapsed():.4f}s running={self._running}>"


# -------------------------------
# TimerThread – Komplexe Version
# -------------------------------
class TimerThread:
    """
    Läuft in einem separaten Thread, verwaltet Laps, Callbacks, Auto-Lap, Pause/Resume
    """

    def __init__(
        self,
        timer: Timer,
        tick_interval: float = 0.1,
        max_time: Optional[float] = None,
    ):
        self.timer = timer
        self.tick_interval = tick_interval
        self.max_time = max_time
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._running = False
        self._callbacks_tick: List[Callable[[Timer], None]] = []
        self._callbacks_lap: List[Callable[[Timer], None]] = []
        self._callbacks_stop: List[Callable[[Timer], None]] = []
        self._auto_lap_interval: Optional[float] = None
        self._last_lap_time: float = 0.0
        self._lock = threading.Lock()

    # -------------------------------
    # Callback-Management
    # -------------------------------
    def on_tick(self, callback: Callable[[Timer], None]):
        self._callbacks_tick.append(callback)

    def on_lap(self, callback: Callable[[Timer], None]):
        self._callbacks_lap.append(callback)

    def on_stop(self, callback: Callable[[Timer], None]):
        self._callbacks_stop.append(callback)

    def set_auto_lap(self, interval: float):
        """Alle x Sekunden automatisch eine Lap speichern"""
        self._auto_lap_interval = interval
        self._last_lap_time = self.timer.elapsed()

    # -------------------------------
    # Thread-Loop
    # -------------------------------
    def _run(self):
        self.timer.start()
        while self._running:
            with self._lock:
                current_elapsed = self.timer.elapsed()

                # Auto-Lap
                if self._auto_lap_interval:
                    if current_elapsed - self._last_lap_time >= self._auto_lap_interval:
                        self._last_lap_time = current_elapsed
                        lap_time = self.timer.lap()
                        for cb in self._callbacks_lap:
                            cb(self.timer)

                # Tick callbacks
                for cb in self._callbacks_tick:
                    cb(self.timer)

            # Max Time prüfen **außerhalb des Locks**
            if self.max_time is not None and current_elapsed >= self.max_time:
                self._running = False
                for cb in self._callbacks_stop:
                    cb(self.timer)
                break

            time.sleep(self.tick_interval)

    # -------------------------------
    # Steuerung
    # -------------------------------
    def start(self):
        if not self._running:
            self._running = True
            if not self._thread.is_alive():
                self._thread = threading.Thread(target=self._run, daemon=True)
                self._thread.start()

    def pause(self):
        with self._lock:
            self.timer.pause()

    def resume(self):
        with self._lock:
            self.timer.start()

    def stop(self):
        self._running = False
        with self._lock:
            self.timer.stop()
        for cb in self._callbacks_stop:
            cb(self.timer)

    def reset(self):
        with self._lock:
            self.timer.reset()
            self._last_lap_time = 0.0


# -------------------------------
# Einfacher Test-Block
# -------------------------------
if __name__ == "__main__":
    print("Starte komplexen TimerThread...")

    def print_tick(timer: Timer):
        print("Tick:", timer.formatted())

    def print_lap(timer: Timer):
        print("Lap:", timer.formatted())

    def print_stop(timer: Timer):
        print("Stop:", timer.formatted())

    t = Timer()
    tt = TimerThread(timer=t, tick_interval=0.5, max_time=5)
    tt.on_tick(print_tick)
    tt.on_lap(print_lap)
    tt.on_stop(print_stop)
    tt.set_auto_lap(1.0)  # jede Sekunde Lap
    tt.start()

    # Hauptthread wartet, TimerThread läuft parallel
    Timer.wait(6)
    tt.stop()
    print("Test fertig")
