#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   async_listen_data_scheduler.py
@Time    :   2025-09-27 17:04:54
@Author  :   chakcy
@Email   :   947105045@qq.com
@description   :   异步监听数据调度器
"""


from ...queue_operation.listen_operation import ListenOperation
import asyncio
from ...mounter.listen_mounter import ListenMounter
import threading
import multiprocessing
import concurrent.futures
import logging


class AsyncListenDataScheduler:
    def __init__(self, listen_operation: ListenOperation):
        self.listen_operation = listen_operation
        self.is_running = False
        self.thread_num = multiprocessing.cpu_count()
        self.listen_thread = None
        self.process_lock = threading.Lock()
        self.last_processed_id = 0

    async def _process_listen_data(self, key, value, delete_id):
        listen_function = ListenMounter.get_Listener_function(key)
        if listen_function:
            if asyncio.iscoroutinefunction(listen_function):
                await listen_function(value)
            else:
                try:
                    loop = asyncio.get_event_loop()
                    with concurrent.futures.ThreadPoolExecutor(
                        max_workers=self.thread_num
                    ) as executor:
                        await loop.run_in_executor(executor, listen_function, value)
                    # listen_function(value)
                except Exception as e:
                    ValueError(f"Error in {key} listener function: {e}")
                finally:
                    self.listen_operation.delete_change_log(delete_id=delete_id)

    async def listen(self):
        async with asyncio.Semaphore(self.thread_num):
            while self.is_running:
                status, change_data_items = self.listen_operation.listen_data()
                tasks = []
                if status and isinstance(change_data_items, list):
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
                        with self.process_lock:
                            if delete_id > self.last_processed_id:
                                self.last_processed_id = delete_id
                        tasks.append(
                            asyncio.create_task(
                                self._process_listen_data(key, new_value, delete_id)
                            )
                        )
                    if tasks and self.is_running:
                        await asyncio.gather(*tasks, return_exceptions=True)

                else:
                    await asyncio.sleep(0.05)

    def _run_listen_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self.listen())
        except Exception as e:
            logging.error(f"监听调度出错: {str(e)}")
        finally:
            loop.close()

    def start_listen_data(self):
        if self.is_running:
            return
        self.is_running = True
        self.last_processed_id = 0
        self.listen_thread = threading.Thread(target=self._run_listen_loop, daemon=True)
        self.listen_thread.start()

    def stop_listen_data(self):
        if not self.is_running:
            return
        self.is_running = False
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)
