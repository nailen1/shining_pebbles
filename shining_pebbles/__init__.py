import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("shining_pebbles package initialized")

from .collection_of_utils import *
from .dataset_cleanser import *
