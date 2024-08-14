# Name: Ashlyn Musgrave
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Open Addressing
# Due Date: December 8, 2023
# Description: This program implements an optimized HashMap class that implements Open Addressing with
# Quadratic Probing

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
        Update the key/value pair in the hash map

        If the key already exists, replace its associated value
        If the key is not in the hash map, add a new key/value pair

        Resize the table if the load factor is >= 0.5
        """
        # Calculate the hash index of the key
        hash_index = self._hash_function(key) % self._capacity

        # Check if the key already exists
        probe_index = hash_index
        while self._buckets[probe_index] is not None:
            if self._buckets[probe_index].key == key:
                # Update existing value
                self._buckets[probe_index].value = value
                return
            probe_index = (probe_index + 1) % self._capacity

        # Check load factor and resize if needed
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Add new key-value pair
        self._buckets[probe_index] = HashEntry(key, value)
        self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs remain in the new hash map and all hash table links are rehashed.
        new_capacity must be > current number of elements in the hash map. If not, the method does nothing.
        Checks if new_capacity is a prime number. If not, it rounds up to the nearest prime number.
        """
        if new_capacity <= self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_table = HashMap(new_capacity, self._hash_function)

        # this is to prevent next_prime from going to 3, when it should stay at 2 (since 2 is prime)
        if new_capacity == 2:
            new_table._capacity = 2

        # be sure to not add size + 1 if rehashing tombstone values
        for item in self:
            if item:
                new_table.put(item.key, item.value)

        # Reassigning new values to self
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table.get_capacity()


    def table_load(self) -> float:
        """
        This method returns the current hash table load factor
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table
        """
        # Keeps track of the # of buckets
        count_empty = 0

        # Used to iterate through the buckets
        index = 0

        while index < self._capacity:
            # Check if the current bucket is empty
            entry = self._buckets[index]
            if entry is None:
                # Increment the count if the bucket is empty
                count_empty += 1
            index += 1

        return count_empty


    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key
        """

        # Calculate the hash index of the key
        hash_index = self._hash_function(key) % self._capacity

        # Check if the key exists
        probe_index = hash_index
        while self._buckets[probe_index] is not None:
            if self._buckets[probe_index].key == key:
                return self._buckets[probe_index].value
            probe_index = (probe_index + 1) % self._capacity

        # Key not found
        return None


    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False
        """
        return self.get(key) is not None


    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        """

        # Calculate the hash index of the key
        hash_index = self._hash_function(key) % self._capacity

        # Check if the key exists
        probe_index = hash_index
        while self._buckets[probe_index] is not None:
            if self._buckets[probe_index].key == key:
                # Found the key, mark it as deleted
                self._buckets[probe_index] = None
                self._size -= 1

                # Perform rehashing if necessary
                next_probe_index = (probe_index + 1) % self._capacity
                while self._buckets[next_probe_index] is not None:
                    next_hash_index = self._hash_function(self._buckets[next_probe_index].key) % self._capacity
                    if next_probe_index <= next_hash_index <= probe_index or next_hash_index <= probe_index < next_probe_index:
                        # Move the entry to the current probe index
                        self._buckets[probe_index] = self._buckets[next_probe_index]
                        self._buckets[next_probe_index] = None
                        probe_index = next_probe_index
                    next_probe_index = (next_probe_index + 1) % self._capacity

                return
            probe_index = (probe_index + 1) % self._capacity

        # Key not found
        return None


    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map
        """
        key_value_pairs = DynamicArray()
        for i in range(self._capacity):
            if self._buckets[i] is not None:
                key_value_pairs.append((self._buckets[i].key, self._buckets[i].value))
        return key_value_pairs


    def clear(self) -> None:
        """
        This method clears the contents of the hash map
        """

        for i in range(self._capacity):
            self._buckets[i] = None
            self._size = 0

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself
        """
        self.index = 0
        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, based on the current location of the iterator
        """
        # Iterate through the buckets starting from the current index
        while self.index < self._capacity:
            # Get the entry at the current index
            entry = self._buckets[self.index]

            # Check if the entry is non-empty and not a tombstone
            if entry and not entry.is_tombstone:
                # Move the index to the next position before returning the entry
                self.index += 1
                return entry

            # Move to the next index in case of tombstone or empty entry
            self.index += 1

        # If the loop completes without finding a valid entry, raise StopIteration
        raise StopIteration

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
