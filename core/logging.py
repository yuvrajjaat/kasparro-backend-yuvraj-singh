import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format=json.dumps({
        "time": "%(asctime)s",
        "level": "%(levelname)s",
        "msg": "%(message)s"
    })
)

logger = logging.getLogger(__name__)
