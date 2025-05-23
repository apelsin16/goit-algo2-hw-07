class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

    def invalidate_range(self, index):
        keys_to_delete = [key for key in self.cache if isinstance(key, tuple) and key[0] <= index <= key[1]]
        for key in keys_to_delete:
            node = self.cache.pop(key)
            self.list.remove(node)

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R, cache: LRUCache):
    result = cache.get((L, R))
    if result != -1:
        return result
    result = sum(array[L:R+1])
    cache.put((L, R), result)
    return result

def update_with_cache(array, index, value, cache: LRUCache):
    array[index] = value
    cache.invalidate_range(index)


import random
import time

if __name__ == "__main__":
    # Генерація масиву і запитів
    N = 100_000
    Q = 50_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = []

    for _ in range(Q):
        if random.random() < 0.7:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))

    # --- Без кешу ---
    array_nc = array.copy()
    start = time.time()
    for q in queries:
        if q[0] == 'Range':
            range_sum_no_cache(array_nc, q[1], q[2])
        else:
            update_no_cache(array_nc, q[1], q[2])
    end = time.time()
    print(f"Час виконання без кешування: {end - start:.2f} секунд")

    # --- З кешем ---
    array_wc = array.copy()
    lru_cache = LRUCache(1000)
    start = time.time()
    for q in queries:
        if q[0] == 'Range':
            range_sum_with_cache(array_wc, q[1], q[2], lru_cache)
        else:
            update_with_cache(array_wc, q[1], q[2], lru_cache)
    end = time.time()
    print(f"Час виконання з LRU-кешем: {end - start:.2f} секунд")