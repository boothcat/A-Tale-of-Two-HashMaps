# Name: Katie Booth
# OSU Email: boothcat@oregonstate.edu
# Course: CS261 - Data Structures, Section 401
# Description: Defines class HashMap, implemented with a dynamic array and
#              singly chained linked list, with methods put, empty buckets,
#              table_load, clear, resize_table, get, contains_key, remove,
#              get_keys_and_values for adding, removing, and manipulating
#              elements of a hash map. Defines function find_mode which uses
#              a hash map to find the mode of a given dynamic array.


from hash_map_include import (DynamicArray, LinkedList,
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
        Adds a key/value pair to the hash map.  If the given key exists in
        the map, the value is updated.
        :param key:     string to represent key
        :param value:   object representing value of key
        :return:        key/value pair added or updated in hash map
        """
        # Calculate index in hash table based on hash function
        index = self._hash_function(key) % self._capacity

        # Check whether key exists in bucket's linked list
        node = self._buckets[index].contains(key)

        # If key does not exist, add new key/value pair
        # Otherwise, update the key's value
        if node is None:
            self._buckets[index].insert(key,value)
            self._size += 1     # Increment number of elements in hash map
        else:
            node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        :return:    integer representing number of empty buckets
        """
        empty_count = 0

        # For each bucket in the table, check the length of the linkedlist
        for num in range(self._buckets.length()):
            list = self._buckets[num]
            if list.length() == 0:      # Zero length = empty bucket
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Returns the hash table load factor.
        :return:    float representing load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears contents of the hash map.  All buckets reset to empty
        linked list.
        :return:    Contents of hash map cleared
        """
        # Reset size of hashmap to zero and clear array
        self._size = 0
        self._buckets = DynamicArray()

        # Add empty linked list to each bucket
        for index in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the hash table's capacity to the given new_capacity or
        next closest prime number. All key/value pairs remain in table
        and hash table links are rehashed.
        :param new_capacity:    integer representing new capacity
        :return:                capacity is changed and links rehashed
        """
        # New capacity must be greater than or equal to 1
        if new_capacity < 1:
            return

        # If new_capacity is not prime, find the next closest prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Store all hash map key/value pairs in an array
        array_key_values = self.get_keys_and_values()

        # Update hash table capacity and clear the hash table
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

        # Check whether key exists in bucket's linked list
        node = self._buckets[index].contains(key)

        # If key does not exist, return None, otherwise return value
        if node is None:
            return
        return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map and False otherwise.
        :param key:     string representing key
        :return:        True if key is in hash map, False otherwise
        """
        # Calculate index in hash table based on hash function
        index = self._hash_function(key) % self._capacity

        # Check whether key exists in bucket's linked list
        node = self._buckets[index].contains(key)

        # If key does not exist, return False, otherwise True
        if node is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash map.
        :param key:     string representing key
        :return:        key/value pair is removed from hash map
        """
        # Check if key exists in the hash map
        if self.contains_key(key) is False:
            return

        # If key exists, calculate index and remove key from the bucket
        index = self._hash_function(key) % self._capacity
        self._buckets[index].remove(key)
        self._size -= 1        # Decrement number of elements in hash map

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns an array where each index contains a tuple of a key/value pair
        in the hash map.
        :return:        Array of key/value pairs
        """
        # Create a new DynamicArray
        array = DynamicArray()

        # Search each bucket's linked list for key/value pairs
        # Store key/value pairs as a tuple and append to new array
        for index in range(self._capacity):
            for node in self._buckets[index]:
                key_value = (node.key, node.value)
                array.append(key_value)

        return array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode and mode frequency of the given DynamicArray. Returns a
    tuple containing a DynamicArray of mode values and an integer representing
    the frequency of the values.
    :param da:     DynamicArray object
    :return:       Tuple of mode Dynamic array and frequency integer
    """
   # Create a new HashMap and new DynamicArray for mode values
    map = HashMap()
    mode_array = DynamicArray()

    # Add first element to mode array and initialize max frequency to 1
    mode_array.append(da[0])
    max_frequency = 1

    # Add key/value pair of first element/frequency to hash map
    map.put(da[0], 1)

    # Iterate through array da elements
    # If new element, add element/frequency to hash map
    # Otherwise, update element's frequency value in hash map
    for index in range(1, da.length()):
        key = da[index]
        if map.contains_key(key) is False:
            count = 1
            map.put(key, count)
        else:
            count = map.get(key) + 1
            map.put(key, count)

        # Check if element's frequency equals max_frequency
        if count == max_frequency:
            mode_array.append(key)

        # Check if element's frequency exceeds max_frequency
        elif count > max_frequency:
            max_frequency = count           # Update max frequency
            mode_array = DynamicArray()     # Clear mode array
            mode_array.append(key)

    return (mode_array, max_frequency)

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
            print("\nAfter the " + str(i+1) + "th entry calling the put() method:")
            print("\tNumber of empty Buckets:", m.empty_buckets(), ", Load Factor:", round(m.table_load(), 2),
                  ", Hashmap Size:", m.get_size(), ", Hashmap Capacity:", m.get_capacity())
    print("\tNotice how the capacity was adjusted to next prime number: 23")
    print("\tFor this implementation capacity does not change based on load factor.")
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

    print("find_mode example")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
