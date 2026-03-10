import structlog
from structlog.stdlib import add_log_level
from structlog.processors import JSONRenderer, TimeStamper


structlog.configure(
    processors=[
        TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        add_log_level,
        JSONRenderer(),
    ]
)
log = structlog.get_logger()
