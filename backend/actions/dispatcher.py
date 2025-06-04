# -*- coding: UTF-8 -*-
from typing import Dict, Callable, AsyncIterable
from functools import wraps

from arkitect.types.runtime.model import Response


class ActionDispatcher:
    _instance = None
    _actions: Dict[str, Callable] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActionDispatcher, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, action_name: str):
        def decorator(func):
            cls._actions[action_name] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    async def dispatch(
        self, action_name: str, *args, **kwargs
    ) -> AsyncIterable[Response]:
        if action_name not in self._actions:
            raise ValueError(f"Action {action_name} not found")
        action = self._actions[action_name]
        async for response in action(*args, **kwargs):
            yield response
