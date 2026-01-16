import datetime as DT
import os

MODE = os.getenv("MODE", "dev")
STARTED = DT.datetime.now()
BUILD = os.getenv("BUILD", "unknown")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


SPEC = dict(
    image=os.getenv("IMAGE_NAME", "unknown"),
    container_image=os.getenv("CONTAINER_IMAGE_NAME", "unknown"),
    app_name=os.getenv("METADATA_NAME", "unknown"),
    namespace=os.getenv("METADATA_NAMESPACE", "unknown"),
    version=os.getenv("VERSION", "unknown"),
    revision=os.getenv("REVISION", "unknown"),
    authored=os.getenv("COMMITTED", "unknown"),
    created=os.getenv("CREATED", "unknown"),
    started=str(STARTED),
    build=BUILD,
)
