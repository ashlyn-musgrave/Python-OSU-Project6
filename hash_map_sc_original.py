# Name: Ashlyn Musgrave
# OSU Email: musgraas@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Separate Chaining
# Due Date: December 8, 2023
# Description:


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

        If the key exists, the associated value is replaced with the new value
        If the key does not exist, a new key/value pair is added

        When executed, the table's capacity is doubled if the current load factor is >= 1.0
        """

        # Check if resizing is necessary by comparing hash map size to its capacity
        if self._size >= self._capacity:
            self._resize()

        # Calculate the index using the hash function
        index = self._hash_function(key) % self._capacity

        # Get the linked list at the calculated index
        linked_list = self._buckets[index]

        # Check if the key already exists in the linked list
        node = linked_list.contains(key)

        if node:
            # Key already exists, update its value
            node.value = value
        else:
            # Key does not exist, add a new key/value pair
            linked_list.insert(key, value)
            self._size += 1

    def _resize(self) -> None:
        """
        This helper method...
        """

        # Double the capacity and find the next prime number
        new_capacity = self._next_prime(2 * self._capacity)

        # Create a new array of linked lists with the updated capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # Rehash all key/value pairs into the new buckets
        for i in range(self._capacity):
            old_linked_list = self._buckets[i]
            for node in old_linked_list:
                new_index = self._hash_function(node.key) % new_capacity
                new_buckets[new_index].insert(node.key, node.value)

        # Update the hash map with the new capacity and buckets
        self._capacity = new_capacity
        self._buckets = new_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table
        Existing key/value pairs will remain in new hash map
        All hash table links must be rehashed using the _rehash_and_update helper method
        """
        # Check if new_capacity is less than 1
        if new_capacity < 1:
            return

        # Ensure new_capacity is a prime number
        new_capacity = self._next_prime(new_capacity)

        # Create a new array of linked lists with the updated capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        self._rehash_then_update(new_buckets, new_capacity)

    def _rehash_then_update(self, new_buckets: DynamicArray, new_capacity: int) -> None:
        """
        This helper method rehashes all key/value pairs into the new buckets and updates the hash map
        """
        # Rehash all key/value pairs into the new buckets
        for i in range(self._capacity):
            old_linked_list = self._buckets[i]
            for node in old_linked_list:
                new_index = self._hash_function(node.key) % new_capacity
                new_buckets[new_index].insert(node.key, node.value)

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
        empty_count = 0
        index = 0
        while index < self._buckets.length():
            linked_list = self._buckets[index]
            if linked_list.length() == 0:
                empty_count += 1
            index += 1
        return empty_count

    def get(self, key: str):
        """
        This method returns the value associated with the give key
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        # Check if the key exists in the linked list
        node = linked_list.contains(key)

        if node:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        # Check if the key exists in the linked list
        return linked_list.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        # Remove the key from the linked list
        linked_list.remove(key)

        # Update the size if the key was removed
        if linked_list.contains(key) is None:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map
        """
        result = DynamicArray()

        index = 0
        while index < self._buckets.length():
            linked_list = self._buckets[index]
            node = linked_list._head

            while node:
                result.append((node.key, node.value))
                node = node.next

            index += 1

        return result
    def clear(self) -> None:
        """
        This method clears the contents of the hash map
        """

        index = 0
        while index < self._buckets.length():
            # Get the linked list at the current index
            linked_list = self._buckets[index]

            # Use a while loop to iterate through the linked list
            current_node = linked_list._head
            while current_node:
                # Save the reference to the next node before removing the current one
                next_node = current_node.next
                # Remove the current node from the linked list
                linked_list.remove(current_node.key)
                # Update the size of the hash map
                self._size -= 1
                # Move to the next node in the linked list
                current_node = next_node

            # Move to the next index in the hash map
            index += 1


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This method returns a tuple containing a dynamic array comprising the mode value(s) of the given array,
    and an integer representing the highest frequency of occurrence for the mode value(s)
    """

    # Create a HashMap to store the frequency of each value in the given DynamicArray
    frequency_map = HashMap()

    # Find frequency of each value in the array using a while loop
    index = 0
    while index < da.length():
        value = da.get_at_index(index)

        # Get the current count from the frequency_map or 0 if not present
        current_count = frequency_map.get(value)

        # Update the frequency_map with the current value and its count
        if current_count is None:
            frequency_map.put(value, 1)
        else:
            frequency_map.put(value, current_count + 1)
        index += 1

    # Find the mode(s) and their frequency using a while loop
    mode_values = DynamicArray()
    max_frequency = 0

    key_values = frequency_map.get_keys_and_values()

    # Iterate through the key-value pairs to find the mode(s)
    index = 0
    while index < key_values.length():
        key = key_values.get_at_index(index)
        count = key[1]
        if count > max_frequency:
            # Found a new maximum frequency
            max_frequency = count
            # Use a new DynamicArray to store the mode values and clear the previous values
            mode_values = DynamicArray()
            mode_values.append(key[0])
        elif count == max_frequency:
            # Another value with the same frequency as the current mode
            mode_values.append(key[0])
        index += 1

    return mode_values, max_frequency


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
