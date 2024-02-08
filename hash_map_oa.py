# Name: Katie Booth
# OSU Email: boothcat@oregonstate.edu
# Course: CS261 - Data Structures, Section 401
# Description: Defines class HashMap, implemented with a dynamic array and
#              open addressing, with methods put, empty buckets,
#              table_load, clear, resize_table, get, contains_key, remove,
#              get_keys_and_values for adding, removing, and manipulating
#              elements of a hash map.


from hash_map_include import (DynamicArray, HashEntry,
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
        Adds a key/value pair to the hash map.  If the given key exists in
        the map, the value is updated.
        :param key:     string to represent key
        :param value:   object representing value of key
        :return:        key/value pair added or updated in hash map
        """
        # Double the hash table's capacity if load factor is >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(2*self._capacity)

        # Calculate index in hash table based on hash function
        index = self._hash_function(key) % self._capacity

        # If bucket is empty or tombstone, add the key/value pair
        if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1     # Increment number of elements in hash map
            return

        # If bucket contains the key, update the key's value
        if self._buckets[index].key == key:
            self._buckets[index].value = value
            return

        # If bucket is not empty and not the key, implement quadratic probing
        j = 0
        new_index = index

        # Continue probing until empty bucket is reached or key found
        while self._buckets[new_index] is not None:
            j += 1
            new_index = (index + j**2) % self._capacity

            if self._buckets[new_index] is None or self._buckets[new_index].is_tombstone is True:
                self._buckets[new_index] = HashEntry(key, value)
                self._size += 1
                return

            if self._buckets[new_index].key == key:
                self._buckets[new_index].value = value
                return

    def table_load(self) -> float:
        """
        Returns the hash table load factor.
        :return:    float representing load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        :return:    integer representing number of empty buckets
        """
        count = 0

        # For each bucket in table, check if bucket is empty or tombstone
        for index in range(self._capacity):
            if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the hash table's capacity to the given new_capacity or
        next closest prime number. All key/value pairs remain in table
        and hash table links are rehashed.
        :param new_capacity:    integer representing new capacity
        :return:                capacity is changed and links rehashed
        """
        # new_capacity cannot be smaller than number of elements in hash map
        if new_capacity < self._size:
            return

        # If new_capacity is not prime, find the next closest prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Store hash map's key/value pairs in array
        array_key_values = self.get_keys_and_values()

        # Update capacity and clear contents of hash table
        self._capacity = new_capacity
        self.clear()

        # Rehash all hash table links
        for index in range(array_key_values.length()):
            key, value = array_key_values[index]
            self.put(key, value)

    def get(self, key: str) -> object:
        """
        Returns the value of the given key.
        :param key:     string representing key
        :return:        object representing value of key
        """
        # Calculate index in hash table based on hash function
        index = self._hash_function(key) % self._capacity

        # Check if bucket is empty
        if self._buckets[index] is None:
            return

        # If bucket has key, return key's value
        if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            return self._buckets[index].value

        # If bucket is not empty and not the key, implement quadratic probing
        j = 0
        new_index = index

        # Keep probing until empty bucket is reached or key is found
        while self._buckets[new_index].key is not None:
            j += 1
            new_index = (index + j ** 2) % self._capacity

            if self._buckets[new_index] is None:
                return

            if self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is False:
                return self._buckets[new_index].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map and False otherwise.
        :param key:     string representing key
        :return:        True if key is in hash map, False otherwise.
        """
        # Calculate index in hash table based on hash function
        index = self._hash_function(key) % self._capacity

        # If bucket is empty, return False
        if self._buckets[index] is None:
            return False

        # If bucket contains key, return True
        if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            return True

        # If bucket is not empty and not key, implement quadratic probing
        j = 0
        new_index = index

        # Keep probing until empty bucket is reached or key is found
        while self._buckets[new_index] is not None:
            j += 1
            new_index = (index + j ** 2) % self._capacity

            if self._buckets[new_index] is None:
                return False

            if self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is False:
                return True

            if self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is True:
                return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash map.
        :param key:     string representing key
        :return:        key/value pair is removed from hash map
        """
        # Calculate index in hash table based on hash function
        index = self._hash_function(key) % self._capacity

        # Check if bucket is empty
        if self._buckets[index] is None:
            return

        # If bucket has key, update tombstone to True, decrement hash map size
        if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            self._buckets[index].is_tombstone = True
            self._size -= 1
            return

        # If bucket is not empty and does not have key, implement quadratic probing
        j = 0
        new_index = index

        # Keep probing until empty bucket is reached or key is found
        while self._buckets[new_index] is not None:
            j += 1
            new_index = (index + j ** 2) % self._capacity

            if self._buckets[new_index] is None:
                return

            if self._buckets[new_index].key == key and self._buckets[new_index].is_tombstone is False:
                self._buckets[new_index].is_tombstone = True
                self._size -= 1
                return

    def clear(self) -> None:
        """
        Clears contents of the hash map.  All buckets reset to None.
        :return:    Contents of hash map cleared
        """
        # Reset size of hashmap to zero and clear array
        self._size = 0
        self._buckets = DynamicArray()

        # Add buckets according to capacity and set contents to None
        for num in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns an array where each index contains a tuple of a key/value pair
        in the hash map.
        :return:        Array of key/value pairs
        """
        # Create new Dynamic Array
        array = DynamicArray()

        #  Search each bucket for key/value pairs
        #  Store key/value pairs as a tuple and append to new array
        for index in range(self._capacity):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                key_value = (self._buckets[index].key, self._buckets[index].value)
                array.append(key_value)

        return array

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\n Hashmap example")
    print("-------------------")
    m = HashMap(20, hash_function_1)
    print("Create a HashMap object m with capacity = 20 using Hash Function 1: m = HashMap(20, hash_function_1)")
    print("Add 30 key/value pairs with put() method:")
    for i in range(30):
        m.put('str' + str(i), i * 100)
        if i % 10 == 9:
            print("\nAfter the " + str(i + 1) + "th entry calling the put() method:")
            print("\tNumber of empty Buckets:", m.empty_buckets(), ", Load Factor:", round(m.table_load(), 2),
                  ", Hashmap Size:", m.get_size(), ", Hashmap Capacity:", m.get_capacity())
    print("\tNotice how the capacity was adjusted to next prime number.")
    print("\tFor this implementation capacity is doubled for load factor >= 0.5.")
    print("\nResize the capacity to 11: m.resize(11)")
    m.resize_table(11)
    print("\tNotice how the load factor and empty buckets changes.")
    print("\tNumber of empty Buckets:", m.empty_buckets(), ", Load Factor:", round(m.table_load(), 2),
          ", Hashmap Size:", m.get_size(), ", Hashmap Capacity:", m.get_capacity())
    print("\nCheck that key 'str10' exists: m.contains_key('str10')")
    print("\tReturned", m.contains_key('str10'))
    print("\nGet value of 'str10' key: m.get('str10')")
    print("\tReturned", m.get('str10'))
    print("\nRemove 'str10' key: m.remove('str10')")
    m.remove('str10')
    print("\tVerify key 'str10' was removed: m.contains_key('str10')")
    print("\tReturned", m.contains_key('str10'))
    print("\nGet all key/value pairs: m.get_keys_and_values()")
    print("\t", m.get_keys_and_values())
    print("\nClear the hashmap: m.clear()")
    m.clear()
    print("\tHashmap table:", m.get_keys_and_values(), "Hashmap Size:", m.get_size(), "Hashmap Capacity:",
          m.get_capacity())