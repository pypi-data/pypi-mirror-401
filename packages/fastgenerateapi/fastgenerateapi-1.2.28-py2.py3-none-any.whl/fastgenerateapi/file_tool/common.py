import abc
from typing import Optional


class PushStatusInterface(abc.ABC):

    async def push_status_progress(self):
        pass

    async def push_status_success(self):
        pass

    async def push_status_error(self, msg: Optional[str]):
        pass







