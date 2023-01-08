class BPlusTreeNode:
    def __init__(self, is_leaf=False, max_num_keys=5):
        self.is_leaf = is_leaf
        self.max_num_keys = max_num_keys
        self.keys = []
        self.children = []
 
    def is_full(self):
        return len(self.keys) == self.max_num_keys
 
class BPlusTree:
    def __init__(self, max_num_keys=5):
        self.root = BPlusTreeNode(is_leaf=True, max_num_keys=max_num_keys)
 
    def insert(self, key, value=None):
        if self.root.is_full():
            old_root = self.root
            self.root = BPlusTreeNode(is_leaf=False, max_num_keys=self.root.max_num_keys)
            self.root.children.append(old_root)
            self._split_child(self.root, 0, old_root)
        self._insert_nonfull(self.root, key, value)
 
    def _insert_nonfull(self, node, key, value=None):
        if node.is_leaf:
            self._insert_into_leaf(node, key, value)
        else:
            index = self._find_child_index(node, key)
            child = node.children[index]
            if child.is_full():
                self._split_child(node, index, child)
                if key > node.keys[index]:
                    index += 1
            self._insert_nonfull(node.children[index], key, value)
 
    def _insert_into_leaf(self, node, key, value):
        index = 0
        while index < len(node.keys) and node.keys[index] < key:
            index += 1
        node.keys.insert(index, key)
        node.children.insert(index, value)
 
    def _split_child(self, node, index, child):
        new_node = BPlusTreeNode(is_leaf=child.is_leaf, max_num_keys=child.max_num_keys)
        node.children.insert(index + 1, new_node)
        node.keys.insert(index, child.keys[child.max_num_keys // 2])
        new_node.keys = child.keys[child.max_num_keys // 2 + 1:]
        new_node.children = child.children[child.max_num_keys // 2 + 1:]
        child.keys = child.keys[:child.max_num_keys // 2]
        child.children = child.children[:child.max_num_keys // 2]
 
    def _find_child_index(self, node, key):
        index = 0
        while index < len(node.keys) and node.keys[index] < key:
            index += 1
        return index
