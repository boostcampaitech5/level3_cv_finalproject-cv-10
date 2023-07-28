__version__ = "10.0.16"

from .tracker_zoo import create_tracker, get_tracker_config
from .trackers.botsort.bot_sort import BoTSORT
from .trackers.bytetrack.byte_tracker import BYTETracker
from .trackers.deepocsort.deep_ocsort import DeepOCSort as DeepOCSORT
from .trackers.ocsort.ocsort import OCSort as OCSORT
from .trackers.strongsort.strong_sort import StrongSORT

__all__ = ("__version__",
           "StrongSORT", "OCSORT", "BYTETracker", "BoTSORT", "DeepOCSORT",
           "create_tracker", "get_tracker_config")
