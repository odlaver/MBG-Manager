from collections import deque


class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.items:
            return None
        return self.items.popleft()

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        if self.is_empty():
            return "Antrean kosong."
        return " ← ".join(self.items)
