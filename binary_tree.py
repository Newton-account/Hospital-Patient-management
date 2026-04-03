class TreeNode:
    def __init__(self, patient):
        self.patient = patient
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, patient):
        if not self.root:
            self.root = TreeNode(patient)
        else:
            self._insert_recursive(self.root, patient)

    def _insert_recursive(self, node, patient):
        if patient["severity"] < node.patient["severity"]:
            if node.left:
                self._insert_recursive(node.left, patient)
            else:
                node.left = TreeNode(patient)
        else:
            if node.right:
                self._insert_recursive(node.right, patient)
            else:
                node.right = TreeNode(patient)

    # RECURSION USED HERE
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.patient)
            self._inorder_recursive(node.right, result)

    def search(self, severity):
        return self._search_recursive(self.root, severity)

    def _search_recursive(self, node, severity):
        if not node:
            return None

        if node.patient["severity"] == severity:
            return node.patient

        if severity < node.patient["severity"]:
            return self._search_recursive(node.left, severity)

        return self._search_recursive(node.right, severity)
