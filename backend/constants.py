import enum


class VolcengineASRResponseStatusCode(enum.Enum):
    SUCCESS = 1000
    RUNNING = 2000
    PENDING = 2001


class AsrTaskStatus(enum.Enum):
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
