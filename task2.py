import timeit
from functools import lru_cache
import matplotlib.pyplot as plt
import pandas as pd


# LRU Cache Fibonacci
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


# Splay Tree
class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
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


# Fibonacci using Splay Tree
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


# Benchmarking
fib_numbers = range(0, 951, 50)
lru_times = []
splay_times = []
results_table = []

for n in fib_numbers:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10)
    lru_times.append(lru_time)

    tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
    splay_times.append(splay_time)

    results_table.append(
        {"n": n, "LRU Cache Time (s)": lru_time, "Splay Tree Time (s)": splay_time}
    )

results_df = pd.DataFrame(results_table)

# Print results
print(results_df)

# Save results to CSV
results_df.to_csv("fibonacci_comparison.csv", index=False)
print("Results saved to fibonacci_comparison.csv")

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(fib_numbers, lru_times, label="LRU Cache", marker="o")
plt.plot(fib_numbers, splay_times, label="Splay Tree", marker="x")
plt.xlabel("Fibonacci Number (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Performance Comparison: LRU Cache vs Splay Tree")
plt.legend()
plt.grid(True)
plt.show()
