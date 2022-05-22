class Queue(list):
    def push(self, item):
        self.append(item)

    def pop(self, index=0):
        return super().pop(index)

    def is_empty(self):
        return len(self) == 0
