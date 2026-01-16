"""Loguru Handler - 将 loguru 日志转发到 RabbitMQ."""

from typing import Any

from loguru import logger

from .log_publisher import LogPublisher


class LoguruMQHandler:
    """Loguru 日志处理器，将日志转发到 RabbitMQ.

    这个处理器可以作为 loguru 的 sink，自动将所有 loguru 日志推送到 MQ。
    适用于用户的工具类使用 loguru 记录日志的场景。

    Example:
        >>> from loguru import logger
        >>> from sdwk.core.logging import setup_loguru_mq_handler
        >>>
        >>> # 在组件中自动配置（推荐）
        >>> class MyComponent(Component):
        ...     def run(self):
        ...         # 工具类中的 loguru 日志会自动推送到 MQ
        ...         from my_utils import some_function
        ...         some_function()  # 内部使用 logger.info() 会自动推送
        >>>
        >>> # 或者手动配置（高级用法）
        >>> handler_id = setup_loguru_mq_handler(log_publisher)
        >>> logger.info("这条日志会推送到 MQ")
        >>> logger.remove(handler_id)  # 清理

    """

    def __init__(self, log_publisher: LogPublisher):
        """初始化处理器.

        Args:
            log_publisher: LogPublisher 实例

        """
        self.log_publisher = log_publisher

    def __call__(self, message: Any) -> None:
        """处理日志记录.

        这个方法会被 loguru 调用，接收日志记录对象。

        Args:
            message: loguru 的日志记录对象

        """
        # 提取日志信息
        record = message.record

        # 过滤掉 LogPublisher 的内部日志，避免循环调用导致死锁
        # LogPublisher 使用 logger.bind(internal=True) 标记内部日志
        if record.get("extra", {}).get("internal"):
            return

        level = record["level"].name
        text = record["message"]

        # 提取额外字段
        extra = {}
        if record.get("extra"):
            # 复制 extra 字段，但排除 internal 标记
            extra.update({k: v for k, v in record["extra"].items() if k != "internal"})

        # 添加文件和行号信息
        if record.get("file"):
            extra["file"] = record["file"].name
        if record.get("line"):
            extra["line"] = record["line"]
        if record.get("function"):
            extra["function"] = record["function"]

        # 发送到 RabbitMQ
        self.log_publisher.publish(level, text, **extra)


def setup_loguru_mq_handler(log_publisher: LogPublisher | None) -> int | None:
    """配置 loguru 将日志转发到 RabbitMQ.

    这个函数会添加一个 handler 到全局的 loguru logger，
    使得所有通过 loguru 记录的日志都会自动推送到 MQ。

    Args:
        log_publisher: LogPublisher 实例，如果为 None 则不配置

    Returns:
        handler ID，可用于后续移除 handler；如果未配置则返回 None

    Example:
        >>> from loguru import logger
        >>> from sdwk.core.logging import LogPublisher, setup_loguru_mq_handler
        >>>
        >>> # 创建 LogPublisher
        >>> publisher = LogPublisher(
        ...     rabbitmq_host="localhost",
        ...     user_id="user123",
        ...     workflow_id="workflow456"
        ... )
        >>>
        >>> # 配置 loguru
        >>> handler_id = setup_loguru_mq_handler(publisher)
        >>>
        >>> # 现在所有 loguru 日志都会推送到 MQ
        >>> logger.info("这条日志会推送到 MQ")
        >>>
        >>> # 清理（可选）
        >>> if handler_id:
        ...     logger.remove(handler_id)

    """
    if not log_publisher:
        return None

    # 创建处理器
    handler = LoguruMQHandler(log_publisher)

    # 添加到 loguru
    # format="{message}" 表示只传递消息内容，不包含格式化的时间戳等
    # 因为 LogPublisher 会自己添加时间戳
    handler_id = logger.add(
        handler,
        format="{message}",
        level="DEBUG",  # 捕获所有级别的日志
        enqueue=False,  # 同步处理，避免消息丢失
    )

    return handler_id


def remove_loguru_mq_handler(handler_id: int | None) -> None:
    """移除 loguru MQ handler.

    Args:
        handler_id: handler ID（由 setup_loguru_mq_handler 返回）

    """
    if handler_id is not None:
        try:
            logger.remove(handler_id)
        except ValueError:
            # Handler 已经被移除
            pass
