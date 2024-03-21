# python3

import sys
import errno
from typing import (
    Tuple,
    Any,
)

from socket import error as SocketError

import multiprocessing as mp

MAX_CLIENT_RUNS_BEFORE_EXIT = 2


class ProcFunc:
    def __init__(self, ctx: Any = None) -> None:
        if ctx is None:
            ctx = mp.get_context("spawn")
        self.ctx = ctx

    def startProc(self, f: Any, max_requests: int) -> Tuple[Any, Any]:
        # start the whole parent part
        self.parent_conn, self.child_conn = mp.Pipe()

        self.proc = self.ctx.Process(
            target=f,
            args=(self.child_conn, max_requests),
        )

        self.proc.start()
        self.child_conn.close()

        return self.proc, self.parent_conn

    def oneItem(self, item: str) -> str:
        self.parent_conn.send(item)
        return str(self.parent_conn.recv())

    def makeHandler(
        self,
        f: Any,
        max_requests: int = MAX_CLIENT_RUNS_BEFORE_EXIT,
    ) -> Any:
        self.startProc(f, max_requests)

        def inner_func(item: str) -> str:
            nonlocal self
            try:
                v = self.oneItem(item)
                return v
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    print(f"restart process {e}", file=sys.stderr)
                    raise
                self.startProc(f, max_requests)
                v = self.oneItem(item)
                return str(v)

        return inner_func
