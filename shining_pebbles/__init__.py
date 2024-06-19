import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Shining Pebbles package initialized")

from .ShiningPebbles import *

import sys
import inspect
from . import ShiningPebbles

for name, obj in inspect.getmembers(ShiningPebbles):
    if inspect.isfunction(obj) or inspect.isclass(obj):
        globals()[name] = obj

__all__ = [name for name, obj in inspect.getmembers(ShiningPebbles) if inspect.isfunction(obj) or inspect.isclass(obj)]