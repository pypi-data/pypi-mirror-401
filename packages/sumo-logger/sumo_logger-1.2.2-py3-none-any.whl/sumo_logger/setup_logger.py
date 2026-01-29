import logging
import inspect
from .handler import SumoHttpHandler
from .context import get_request_id


# 🔹 Patch LogRecord globally (ONCE)
_old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = _old_factory(*args, **kwargs)
    record.request_id = get_request_id()
    return record


logging.setLogRecordFactory(record_factory)


def setup_sumo_logger(http_url: str, module_name: str = None, log_level=logging.INFO):

    if not http_url:
        raise ValueError("HTTP URL is required to initialize Sumo logger")

    if module_name is None:
        for frame_info in inspect.stack():
            mod_name = frame_info.frame.f_globals.get("__name__")
            if mod_name and not mod_name.startswith("sumo_logger"):
                module_name = mod_name
                break
        else:
            module_name = "UnknownModule"

    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    if not any(isinstance(h, SumoHttpHandler) for h in logger.handlers):
        handler = SumoHttpHandler(http_url)
        logger.addHandler(handler)

    return logger
