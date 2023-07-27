from flask import Flask, has_request_context, request
import logging

from config import LogConfig


def setup_logger(app):
    logger = logging.getLogger("")

    # Определите фабрику записей, как в вашем изначальном примере
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.remote_addr = '-'
        record.user = '-'
        if has_request_context():
            record.remote_addr = request.remote_addr
            if hasattr(request, 'user_id'):
                record.user = request.user_id
        return record
    logging.setLogRecordFactory(record_factory)

    # Настройте обработчики и уровень логирования
    if hasattr(LogConfig, 'FILE') and isinstance(LogConfig.FILE, str):
        log_handler = logging.FileHandler(LogConfig.FILE, 'a')
    else:
        log_handler = logging.StreamHandler()
    log_handler.setFormatter(
        logging.Formatter(
            fmt=getattr(LogConfig, 'FORMAT', "[%(asctime)s] [%(levelname)s] [%(remote_addr)s] [%(user)s]: %(message)s"),
            datefmt=getattr(LogConfig, 'DATE_FORMAT', "%Y-%m-%d %H:%M:%S"),
        )
    )
    logger.addHandler(log_handler)
    logger.setLevel(getattr(LogConfig, 'LEVEL', logging.INFO))
    return logger
