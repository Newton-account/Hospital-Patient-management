class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def delete(self, key):
        current = self.head
        prev = None

        while current:
            if current.data["id"] == key:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next

        return False

    def search(self, key):
        current = self.head
        while current:
            if current.data["id"] == key:
                return current.data
            current = current.next
        return None

    def display(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result