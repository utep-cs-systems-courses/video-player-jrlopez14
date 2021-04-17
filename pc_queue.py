#!/usr/bin/env python3

import threading

class pc_queue:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(10)

    def insert(self,i):
        self.empty.acquire()
        self.lock.acquire()
        self.buffer.append(i)
        self.lock.release()
        self.full.release()

    def remove(self):
        self.full.acquire()
        self.lock.acquire()
        i = self.buffer.pop(0)
        self.lock.release()
        self.empty.release()
        return i

    def end(self):
        self.insert(None)
