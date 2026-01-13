from pathlib import Path
import sys
import pprint

# Projekt-Root in sys.path aufnehmen
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mauztoolslib.log import Levels, Logging, FrozenLoggingError

logger = Logging(level=Levels.DEBUG)

logger.debug("Test")
logger.info(logger)
logger.info("Info")
logger.warning("Hilfe")
logger.changeConfig(
    filename="test.log",
)
logger.info(str(logger))
logger2 = logger.copy()
logger2.switch_freeze()
if logger2.is_frozen():
    logger2.critical("Gleich wird das Programm anstürzen!")
try:
    logger2.changeConfig(filename="test2.log")
except FrozenLoggingError as e:
    logger2.critical("Doch Abgefangen!", exc=e)
print(pprint.pformat(logger2.as_dict()))
logger.error("ERROR! ERROR!")
try:
    [0, 1, 2][5]
except Exception:
    logger.critical("IndexError!", exc=True)
logger.info("HoHoHo, nur eine info")