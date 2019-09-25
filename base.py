from abc import ABC, abstractmethod
from threading import Thread


class BaseThread(ABC, Thread):
    """Базовый класс для вызова операций в отдельных потоках"""
    def __init__(self):
        """Инициализация потока"""
        Thread.__init__(self)
        self.is_stopped = False

    @abstractmethod
    def run(self):
        """Запуск потока"""
        raise NotImplementedError

    def stop(self):
        self.is_stopped = True
