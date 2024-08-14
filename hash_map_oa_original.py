# Name: Ashlyn Musgrave
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Open Addressing
# Due Date: December 8, 2023
# Description:

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map
        """
        # Check if resizing is needed

        load_factor = self._size / self._capacity
        if load_factor >= 0.5:
            self._resize()

        # Hash the key to get the index
        index = self._hash_function(key) % self._capacity

        # Quadratic probing to handle collisions
        current_index = index
        probe_count = 0

        while probe_count < self._capacity:
            entry = self._buckets[current_index]

            if entry is None or entry.is_tombstone:
                # Found an empty slot or a tombstone, insert the new entry
                self._buckets[current_index] = HashEntry(key, value)
                self._size += 1
                return

            elif entry.key == key:
                # Key already exists, update the value
                entry.value = value
                return

            # Quadratic probing: increment the probe count and recalculate index
            probe_count += 1
            current_index = (index + probe_count ** 2) % self._capacity

        # If we reach here, it means we couldn't find an empty slot or tombstone after probing
        # This should not happen with proper resizing, but it's good to check for safety
        raise DynamicArrayException("HashMap is full and resizing didn't help.")

    def _resize(self) -> None:
        """
        Resize the hash map to double its current capacity.
        Rehash all existing entries to the new table.
        """
        # Double the capacity and find the next prime
        new_capacity = self._next_prime(self._capacity * 2)

        # Create a new array with the updated capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        # Rehash existing entries to the new array
        index = 0
        while index < self._capacity:
            entry = self._buckets[index]
            if entry and not entry.is_tombstone:
                new_index = self._hash_function(entry.key) % new_capacity
                new_probe_count = 0

                while True:
                    new_index = (new_index + new_probe_count ** 2) % new_capacity

                    if new_buckets[new_index] is None or new_buckets[new_index].is_tombstone:
                        # Found an empty slot or tombstone, insert the entry
                        new_buckets[new_index] = entry
                        break

                    # Increment probe count for quadratic probing
                    new_probe_count += 1

            index += 1

        # Update the hash map with the new capacity and buckets
        self._capacity = new_capacity
        self._buckets = new_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table
        """
        # Check if new_capacity is less than the current number of elements
        if new_capacity < self._size:
            return

        # Ensure new_capacity is a prime number
        new_capacity = self._next_prime(new_capacity)

        # Create a new array with the updated capacity
        new_buckets = DynamicArray()

        # Initialize index for while loop
        index = 0
        while index < new_capacity:
            new_buckets.append(None)
            index += 1

        # Rehash existing entries to the new array
        index = 0
        while index < self._capacity:
            entry = self._buckets[index]
            if entry and not entry.is_tombstone:
                new_index = self._hash_function(entry.key) % new_capacity
                new_probe_count = 0

                while True:
                    new_index = (new_index + new_probe_count ** 2) % new_capacity

                    if new_buckets[new_index] is None or new_buckets[new_index].is_tombstone:
                        # Found an empty slot or tombstone, insert the entry
                        new_buckets[new_index] = entry
                        break

                    # Increment probe count for quadratic probing
                    new_probe_count += 1

            index += 1

        # Update the hash map with the new capacity and buckets
        self._capacity = new_capacity
        self._buckets = new_buckets

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table
        """
        count_empty = 0
        index = 0

        while index < self._capacity:
            entry = self._buckets[index]
            if entry is None:
                count_empty += 1
            index += 1

        return count_empty

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key
        """
        index = self._hash_function(key) % self._capacity
        probe_count = 0

        while probe_count < self._capacity:
            entry = self._buckets[index]

            if entry is None:
                # Reached an empty slot, key is not in the hash map
                return None

            elif entry.key == key:
                # Found the key, return its associated value
                return entry.value

            # Quadratic probing: increment the probe count and recalculate index
            probe_count += 1
            index = (index + probe_count ** 2) % self._capacity

        # If we reach here, it means we couldn't find the key after probing
        return None

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        index = self._hash_function(key) % self._capacity
        probe_count = 0

        while probe_count < self._capacity:
            entry = self._buckets[index]

            if entry is None:
                # Reached an empty slot, key is not in the hash map
                return False

            elif entry.key == key:
                # Found the key
                return True

            # Quadratic probing: increment the probe count and recalculate index
            probe_count += 1
            index = (index + probe_count ** 2) % self._capacity

        # If we reach here, it means we couldn't find the key after probing
        return False

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        index = self._hash_function(key) % self._capacity
        probe_count = 0

        while probe_count < self._capacity:
            entry = self._buckets[index]

            if entry is None:
                # Reached an empty slot, key is not in the hash map
                return

            elif entry.key == key:
                # Found the key, mark the entry as tombstone
                entry.is_tombstone = True
                self._size -= 1
                return

            # Quadratic probing: increment the probe count and recalculate index
            probe_count += 1
            index = (index + probe_count ** 2) % self._capacity

        # If we reach here, it means we couldn't find the key after probing
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        key_value_pairs = DynamicArray()

        index = 0
        while index < self._capacity:
            entry = self._buckets[index]
            if entry and not entry.is_tombstone:
                key_value_pairs.append((entry.key, entry.value))
            index += 1

        return key_value_pairs

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        for i in range(self._capacity):
            self._buckets[i] = None

        self._size = 0

    def __iter__(self):
        """
        TODO: Write this implementation
        """
        self.index = 0
        return self

    def __next__(self):
        """
        TODO: Write this implementation
        """
        try:
            value = None
            while value is None or value.is_tombstone is True:
                value = self._buckets.get_at_index(self.index)
                self.index += 1
        except DynamicArrayException:
            raise StopIteration

        return value

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
