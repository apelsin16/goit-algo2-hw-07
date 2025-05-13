import timeit
import functools
import matplotlib.pyplot as plt


# Реалізація Splay Tree
class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Вставка нового елемента в дерево."""
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        """Рекурсивна вставка елемента у дерево."""
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        """Пошук елемента в дереві із застосуванням сплайювання."""
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None  # Якщо елемент не знайдено.

    def _splay(self, node):
        """Реалізація сплайювання для переміщення вузла до кореня."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig ситуація
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


# Реалізація Fibonacci з LRU Cache
@functools.lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Реалізація Fibonacci з Splay Tree
def fibonacci_splay(n, tree):
    result = tree.find(n)
    if result is None:
        if n <= 1:
            result = n
        else:
            result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
        tree.insert(n)
        tree.insert(result)
    return result


# Функція для вимірювання часу виконання обчислення Fibonacci
def measure_time(fib_function, n, tree=None):
    if fib_function == fibonacci_lru:
        return timeit.timeit(lambda: fib_function(n), number=1)
    return timeit.timeit(lambda: fib_function(n, tree), number=1)


# Вимірювання часу для різних значень n
n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

tree = SplayTree()

for n in n_values:
    lru_time = measure_time(fibonacci_lru, n)
    splay_time = measure_time(fibonacci_splay, n, tree)

    lru_times.append(lru_time)
    splay_times.append(splay_time)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label='LRU Cache Time')
plt.plot(n_values, splay_times, label='Splay Tree Time', linestyle='--')
plt.xlabel('n (Fibonacci Number)')
plt.ylabel('Time (seconds)')
plt.title('Fibonacci Calculation Time Comparison: LRU Cache vs Splay Tree')
plt.legend()
plt.grid(True)
plt.savefig("fibonacci.png")
# plt.show()

# Виведення таблиці
print("n         LRU Cache Time (s)  Splay Tree Time (s)")
print("--------------------------------------------------")
for i in range(len(n_values)):
    print(f"{n_values[i]:<10} {lru_times[i]:<20} {splay_times[i]:<20}")
