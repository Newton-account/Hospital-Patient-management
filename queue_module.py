class PatientQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, patient):
        self.queue.append(patient)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def display(self):
        return self.queue