from abc import ABC, abstractmethod
from typing import Callable
from ...model import MessageItem, SchedulerConfig
from queue_sqlite_core import ShardedQueueOperation
import logging


class BaseScheduler(ABC):
    """调度器抽象类"""

    def __init__(self, config: SchedulerConfig = SchedulerConfig()):
        self._queue_operation = None

    @property
    def queue_operation(self) -> ShardedQueueOperation:
        if self._queue_operation is None:
            raise RuntimeError("请先设置队列操作对象")
        return self._queue_operation

    @queue_operation.setter
    def queue_operation(self, value: ShardedQueueOperation | None):
        """设置队列操作对象

        Args:
            value (ShardedQueueOperation): 队列操作对象
        """
        self._queue_operation = value

    @abstractmethod
    def send_message(self, message: MessageItem, callback: Callable):
        """发送消息到队列

        Args:
            message (MessageItem): 消息对象
            callback (Callable): 发送完成后的回调函数
        """
        pass

    @abstractmethod
    def start(self):
        """启动调度器"""
        pass

    @abstractmethod
    def stop(self):
        """停止调度器"""
        pass

    @abstractmethod
    def update_listen_data(self, key, value):
        """更新监听数据"""
        pass

    @abstractmethod
    def get_listen_datas(self) -> list:
        """获取监听数据"""
        pass

    @abstractmethod
    def get_listen_data(self, key):
        """获取单个监听数据"""
        pass

    def get_queue_info(self) -> dict:
        try:
            return {
                "queue_length": self.queue_operation.get_queue_length(),
                "shard_num": self.queue_operation.shard_num,
                "db_dir": self.queue_operation.db_dir,
            }
        except Exception as e:
            logging.error(f"获取队列消息失败: {str(e)}")
            return {}
