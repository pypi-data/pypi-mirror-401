#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   listen_data_scheduler.py
@Time    :   2025-09-27 17:03:39
@Author  :   chakcy
@Email   :   947105045@qq.com
@description   :   监听数据调度器
"""


from ...queue_operation.listen_operation import ListenOperation
from concurrent.futures import ThreadPoolExecutor
from ...mounter.listen_mounter import ListenMounter
import threading
import multiprocessing
import time
import logging


class ListenDataScheduler:
    def __init__(self, listen_operation: ListenOperation):
        self.listen_operation = listen_operation
        self.is_running = False
        self.executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        self.listen_thread = None
        # 使用一个线程锁来确保监听逻辑的原子性
        self.process_lock = threading.Lock()
        # 记录最后处理的ID，避免重复处理
        self.last_processed_id = 0

    def _process_listen_data(self, key, value, delete_id):
        listen_function = ListenMounter.get_Listener_function(key)
        if listen_function:
            try:
                listen_function(value)
            except Exception as e:
                ValueError(f"Error in {key} listener function: {e}")
            finally:
                # 确保变更日志被删除
                try:
                    self.listen_operation.delete_change_log(delete_id=delete_id)
                except Exception as e:
                    # 记录错误但不抛出异常
                    logging.error(f"Error in deleting change log: {e}")

    def listen(self):
        while self.is_running:
            # 获取比上次处理ID更大的变更记录，避免重复处理
            status, change_data_items = self.listen_operation.listen_data()
            if status and isinstance(change_data_items, list):
                # 过滤出ID大于上次处理ID的记录
                new_change_data_items = [
                    data
                    for data in change_data_items
                    if data[0] > self.last_processed_id
                ]
                # 按ID升序排序，确保按顺序处理
                new_change_data_items.sort(key=lambda x: x[0])

                for data in new_change_data_items:
                    key = data[3]
                    new_value = data[5]
                    delete_id = data[0]

                    if self.is_running:
                        # 提交任务处理
                        self.executor.submit(
                            self._process_listen_data, key, new_value, delete_id
                        )

                        # 更新最后处理ID
                        with self.process_lock:
                            if delete_id > self.last_processed_id:
                                self.last_processed_id = delete_id

            # 添加小延迟，避免过度占用CPU
            time.sleep(0.001)

    def start_listen_data(self):
        if self.is_running:
            return
        self.is_running = True
        self.last_processed_id = 0  # 重置最后处理ID
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def stop_listen_data(self):
        if not self.is_running:
            return
        self.is_running = False
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)

        self.executor.shutdown(wait=True)
