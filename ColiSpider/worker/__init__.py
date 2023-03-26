from abc import abstractmethod
from enum import Enum


class RunTypeEnum(Enum):
    PROCESS = 1
    THREAD = 2
    ASYNC = 3


class Worker(object):
    def __init__(self):
        self.check_context = None

    def _merge_config(self):
        pass

    def run(self, *args, **kwargs):
        self._self_check()
        self._run(*args, **kwargs)

    @abstractmethod
    def _self_check(self, *args, **kwargs):
        ...

    @abstractmethod
    def _run(self, *args, **kwargs):
        ...

    class _Config:
        run_type = RunTypeEnum.PROCESS
