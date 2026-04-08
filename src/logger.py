import logging


def setup_logger(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("job_hunter_agent")
    if logger.handlers:
        return logger  # 防止重复添加 handler

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger