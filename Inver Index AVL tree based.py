import re


class TreeNode:
    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.right = right
        self.left = left
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.counter = 0

    def insert(self, key, value):
        if self.root is None:
            self.root = TreeNode(key, value)
            self.counter += 1
            return 1
        else:
            ids = self.insert_node(key, value)
            self.counter += 1
            return ids

    def insert_node(self, key, value, insert_point=None):
        if insert_point is None:
            insert_point = self.root
        while 1:
            if key < insert_point.key:
                if insert_point.left is None:
                    new_node = TreeNode(key, value, insert_point)
                    insert_point.left = new_node
                    self.balance(insert_point)
                    return 1
                else:
                    insert_point = insert_point.left
            elif key > insert_point.key:
                if insert_point.right is None:
                    new_node = TreeNode(key, value, insert_point)
                    insert_point.right = new_node
                    self.balance(insert_point)
                    return 1
                else:
                    insert_point = insert_point.right
            elif key == insert_point.key:
                self.counter -= 1
                return 0

    def balance(self, node):
        # Node case
        while node != self.root:
            balance = self.get_balance(node)
            if balance > 1:
                if self.get_balance(node.left) > 0:
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif balance < -1:
                if self.get_balance(node.right) < 0:
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            self.update_height(node)
            node = node.parent

        # root case
        balance = self.get_balance(self.root)
        if balance > 1:
            if self.get_balance(self.root.left) > 0:
                self.right_rotate(self.root)
            else:
                self.left_rotate(self.root.left)
                self.right_rotate(self.root)
        elif balance < -1:
            if self.get_balance(self.root.right) < 0:
                self.left_rotate(self.root)
            else:
                self.right_rotate(self.root.right)
                self.left_rotate(self.root)
        self.update_height(self.root)

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        result = self.get_height(node.left) - self.get_height(node.right)
        return result

    def update_height(self, node):
        node.height = 1 + AVLTree.max(self.get_height(node.left), self.get_height(node.right))

    def right_rotate(self, node):
        if node != self.root:
            Parent = node.parent
            left_node = node.left
            node.left = left_node.right
            if left_node.right is not None:
                left_node.right.parent = node
            left_node.right = node
            node.parent = left_node
            left_node.parent = Parent
            if Parent.left == node:
                Parent.left = left_node
            else:
                Parent.right = left_node
        else:
            left_node = node.left
            node.left = left_node.right
            if left_node.right is not None:
                left_node.right.parent = node
            left_node.parent = None
            left_node.right = node
            node.parent = left_node
            self.root = left_node
        self.update_height(node)
        self.update_height(node.parent)

    def left_rotate(self, node):
        if node != self.root:
            Parent = node.parent
            right_node = node.right
            node.right = right_node.left
            if right_node.left is not None:
                right_node.left.parent = node
            right_node.left = node
            node.parent = right_node
            right_node.parent = Parent
            if Parent.left == node:
                Parent.left = right_node
            else:
                Parent.right = right_node
        else:
            right_node = node.right
            node.right = right_node.left
            if right_node.left is not None:
                right_node.left.parent = node
            right_node.parent = None
            right_node.left = node
            node.parent = right_node
            self.root = right_node
        self.update_height(node)
        self.update_height(node.parent)

    @staticmethod
    def max(a, b):
        if a > b:
            return a
        else:
            return b

    def traverse(self, node=None):
        result = []
        while 1:
            if node is not None:
                result.append(node)
                node = node.left
            elif result:
                node = result.pop()
                print(node.key, end=' ')
                node = node.right
            else:
                break
        print()

    def search(self, current_node, key):
        while 1:
            if current_node is None:
                return current_node
            elif current_node.key == key:
                return current_node
            elif key < current_node.key and current_node.left is not None:
                current_node = current_node.left
            elif key > current_node.key and current_node.right is not None:
                current_node = current_node.right
            else:
                current_node = None
                return current_node

    def getitem(self, key, default=None):
        current_node = self.search(self.root, key)
        if current_node is not None:
            return current_node.value
        if default is None:
            return None
        if current_node is None:
            new_default = default()
            self.insert(key, new_default)
            return new_default

    def search_value(self, current_node, key):
        while 1:
            if current_node is None:
                return current_node
            elif current_node.key == key:
                return current_node.value
            elif key < current_node.key and current_node.left is not None:
                current_node = current_node.left
            elif key > current_node.key and current_node.right is not None:
                current_node = current_node.right
            else:
                current_node = None
                return current_node


class AVLSet:
    def __init__(self):
        self.avl = AVLTree()
        self.present = object()

    def add(self, doc_id):
        return self.avl.insert(doc_id, self.present)


class InvertedIndex:
    def __init__(self):
        self.avl = AVLTree()
        self.ids = 0

    def parsing(self, text):
        word_list = re.split(r' ', text)
        return word_list

    def words_normie(self, words):
        normalized_words = []
        for word in words:
            word_normie = word.lower()
            normalized_words.append(word_normie)
        return normalized_words

    def word_parsing(self, text):
        words = self.parsing(text)
        # words = self.words_normie(words)
        return words

    def index_doc(self, document, doc_id):
        words = self.word_parsing(document)
        for i in range(len(words)):
            self.ids += self.avl.getitem(words[i], AVLSet).add(doc_id)

    def search_word(self, query):
        result = self.avl.search_value(self.avl.root, query)
        if result is None:
            print(-1)
            return -1
        else:
            result.avl.traverse(result.avl.root)

    def av_id(self):
        words = self.avl.counter
        ids = self.ids
        result = round(ids / words)
        result = int(result)
        return result

    def print_key(self):
        self.avl.traverse(self.avl.root)


index = InvertedIndex()

num_documents = int(input().strip())
documents = []
i = 0
while i < num_documents:
    documents_item = input()
    documents.append(documents_item)
    i += 1

num_queries = int(input().strip())
queries = []
for _ in range(num_queries):
    queries_item = input()
    queries.append(queries_item)


for g in range(num_documents):
    index.index_doc(documents[g], g)

for g in range(num_queries):
    index.search_word(queries[g])

print(index.av_id())

try:
    print_keys_flag = input()
    should_print_keys = print_keys_flag == 'print_keys'
except:
    should_print_keys = False

if should_print_keys:
    index.print_key()
