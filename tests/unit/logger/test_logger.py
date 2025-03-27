import logging
from src.application.shared.logutils import CtxVarEnum, set_logging_var
from src.application.logger_settings import CustomLogRecord, ExtraCtxFilter


def test_set_logging_var_sets_and_resets():
    """Проверка, что переменная устанавливается и сбрасывается."""
    var = CtxVarEnum.RequestId.value
    assert var.get() == ""

    with set_logging_var(enum=CtxVarEnum.RequestId, value="123"):
        assert var.get() == "123"

    assert var.get() == ""


def test_extra_ctx_filter_no_context(
    log_record: CustomLogRecord,
    ctx_filter: ExtraCtxFilter,
):
    """Без контекста extra_message должен быть пустым."""
    filtered_record = ctx_filter.filter(log_record)

    assert filtered_record.extra_message == ""


def test_extra_ctx_filter_with_request_id(
    log_record: CustomLogRecord, ctx_filter: ExtraCtxFilter
):
    """Должен добавить RequestId в extra_message."""
    with set_logging_var(enum=CtxVarEnum.RequestId, value="123"):
        filtered_record = ctx_filter.filter(log_record)
        assert "RequestId: 123" in filtered_record.extra_message


def test_extra_ctx_filter_with_request_and_user(
    log_record: CustomLogRecord, ctx_filter: ExtraCtxFilter
):
    """Должен добавить RequestId и CurrentUser в extra_message."""
    with (
        set_logging_var(enum=CtxVarEnum.RequestId, value="123"),
        set_logging_var(enum=CtxVarEnum.CurrentUser, value="admin"),
    ):
        filtered_record = ctx_filter.filter(log_record)
        assert "RequestId: 123" in filtered_record.extra_message
        assert "CurrentUser: admin" in filtered_record.extra_message


def test_set_lvl_loggers_changes_level():
    """Проверка, что уровень логирования меняется."""
    logger = logging.getLogger(__name__)
    logger.info(f"logger: {logger.name}")

    logger.setLevel(logging.WARNING)

    from src.application.logger_settings import _set_lvl_loggers

    _set_lvl_loggers(
        logging.INFO,
        *[
            str(logger.name),
        ],
    )

    assert logger.level == logging.INFO
