#! /usr/bin/env python3

import os

from procFunc import ProcFunc


def print_func(
    conn,
    max_requests: int,
) -> None:
    n = 0
    while True:
        n += 1
        try:
            request = conn.recv()
            reply = f"The name of the given continent is: {request}. Says process {os.getpid()} with count {n}"
            conn.send(reply)
        except EOFError as e:
            _ = e
            exit(0)

        if n >= max_requests:
            break


def main():
    names = [
        "Europe",
        "Azia",
        "Africa",
        "America",
        "Antarctica",
        "Atlantis",
        "Mu",
        "Heaven",
        "Hell",
        "Purgatory",
        "Nirvana",
    ]

    pf = ProcFunc()
    # every 5 calls of func we start a new process to avoid memory leaks
    # f = pf.makeHandler(print_func, 5)
    f = pf.makeHandler(print_func)

    n = 0
    while True:
        n += 1
        for item in names:
            v = f(item)
            print(v)
        if n >= 26:
            break


if __name__ == "__main__":
    retcode = main()
    exit(retcode)
