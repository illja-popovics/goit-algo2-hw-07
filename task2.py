import timeit
from functools import lru_cache
import matplotlib.pyplot as plt
import pandas as pd

# LRU Cache implementation of Fibonacci
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Splay Tree Node
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


# Splay Tree class
class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        # Key lies in left subtree
        if key < root.key:
            if root.left is None:
                return root

            # Zig-Zig (Left Left)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)

            # Zig-Zag (Left Right)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)

                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root

        # Key lies in right subtree
        else:
            if root.right is None:
                return root

            # Zag-Zig (Right Left)
            if key < root.right.key:
                root.right.left = self._splay(root.right.left, key)

                if root.right.left:
                    root.right = self._rotate_right(root.right)

            # Zag-Zag (Right Right)
            elif key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)

            return self._rotate_left(root) if root.right else root

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            self.root.value = value
            return

        new_node = SplayNode(key, value)

        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node


# Splay Tree implementation of Fibonacci
def fibonacci_splay(n, tree):
    result = tree.search(n)
    if result is not None:
        return result

    if n <= 1:
        tree.insert(n, n)
        return n

    value = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, value)
    return value


# Test parameters
fib_numbers = range(0, 951, 50)
lru_times = []
splay_times = []
results_table = []

for n in fib_numbers:
    # Measure LRU Cache time
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10)
    lru_times.append(lru_time)

    # Measure Splay Tree time
    tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
    splay_times.append(splay_time)

    # Append results to table
    results_table.append({"n": n, "LRU Cache Time (s)": lru_time, "Splay Tree Time (s)": splay_time})

# Convert results to a DataFrame for display
results_df = pd.DataFrame(results_table)
import ace_tools as tools; tools.display_dataframe_to_user(name="Порівняння часу виконання LRU Cache та Splay Tree", dataframe=results_df)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(fib_numbers, lru_times, label="LRU Cache", marker="o")
plt.plot(fib_numbers, splay_times, label="Splay Tree", marker="x")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)
plt.show()
