# python3

import sys
import errno

from socket import error as SocketError

import multiprocessing as mp

MAX_CLIENT_RUNS_BEFORE_EXIT = 2


class ProcFunc:
    def __init__(self, ctx=None):
        if ctx is None:
            ctx = mp.get_context("spawn")
        self.ctx = ctx

    def startProc(self, f, max_requests):
        # start the whole parent part
        self.parent_conn, self.child_conn = mp.Pipe()

        self.proc = self.ctx.Process(
            target=f,
            args=(self.child_conn, max_requests),
        )

        self.proc.start()
        self.child_conn.close()

        return self.proc, self.parent_conn

    def oneItem(self, item):
        self.parent_conn.send(item)
        return self.parent_conn.recv()

    def makeHandler(
        self,
        f,
        max_requests: int = MAX_CLIENT_RUNS_BEFORE_EXIT,
    ):
        self.startProc(f, max_requests)

        def inner_func(item):
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
                return v

        return inner_func
