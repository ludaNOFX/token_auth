import logging
import pytest

from src.application.logger_settings import CustomLogRecord, ExtraCtxFilter


@pytest.fixture(scope="function")
def log_record() -> CustomLogRecord:
    """Фикстура для создания LogRecord"""
    return CustomLogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test",
        args=(),
        exc_info=None,
    )


@pytest.fixture(scope="function")
def ctx_filter() -> ExtraCtxFilter:
    """Фикстура для фильтра."""
    return ExtraCtxFilter()
