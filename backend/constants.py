import enum


class VolcengineASRResponseStatusCode(enum.Enum):
    SUCCESS = "20000000"
    RUNNING = "20000001"
    PENDING = "20000002"


class AsrTaskStatus(enum.Enum):
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
