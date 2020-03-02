import atexit
import logging
import traceback

from lifecycle_handler import Lifecycle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

lifecycle = Lifecycle("all")
atexit.register(lifecycle.exit)

try:
    lifecycle.start("all")
    lifecycle.wait_for_exit()
except Exception as e:
    logger.error("Encountered error:")
    logger.error(traceback.format_exc())
    logger.info("Stopping remaining services...")
    lifecycle.exit()
