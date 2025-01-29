import random
import time
from functools import lru_cache
from collections import OrderedDict

class LRUCache:
    
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Remove the least recently used item
        self.cache[key] = value

    def invalidate(self):
        """Clear cache."""
        self.cache.clear()


# Function without caching
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

# LRU Cache for Range Sum Queries
cache = LRUCache(1000)

def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate() 


# Generate test data
N = 100_000
Q = 50_000
array = [random.randint(1, 1000) for _ in range(N)]
queries = []

for _ in range(Q):
    if random.random() < 0.5:  
        L = random.randint(0, N-1)
        R = random.randint(L, N-1)
        queries.append(('Range', L, R))
    else: 
        index = random.randint(0, N-1)
        value = random.randint(1, 1000)
        queries.append(('Update', index, value))


start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
end_time = time.time()
no_cache_time = end_time - start_time

# Measure performance with cache
start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(array, query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
end_time = time.time()
cache_time = end_time - start_time

# Print results
print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")
