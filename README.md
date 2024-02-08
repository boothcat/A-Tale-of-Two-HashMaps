# A-Tale-of-Two-HashMaps
This project was the culmination of my Data Structures course.  No built-in Python data structures and/or their methods were allowed to be used.  File hash_map_include.py contains the classes DynamicArray and LinkedList which were provided for this assignment and implemented earlier in the course. File hash_map_include.py also contains two pre-written hash functions for indexing hashmap keys in the hashmap table. 

The files hash_map_sc.py and hash_map_oa.py contain implementations for the hashmap data structure using seperate chaining and open addressing respectively.  Both implementations of the HashMap class contain the following methods:
*put() - takes a string key and an object value as parameters. Updates the key/value pair.  If the key does not exist, it creates a new key/value pair. 
*get() - takes a string key parameter.  Returns the value associated with the given key. Otherwise returns None.
*remove() - takes a string key parameter. Method removes the given key and its value. 
*contains_key() - takes a string key parameter. Returns True if the key exists in the hashmap and False otherwise.
*clear() - clears the contents of the hash map but does not change hash table capacity.
*empty_buckets() - returns the number of empty buckets in the hash table.
*resize_table() - takes an integer new capacity parameter. Changes the hash table capacity but keeps all existing key/value pairs.  Hashtable links are rehashed. 
*table_load() - returns the current hash table load factor
*get_keys_and_values() - returns a dynamic array where each index contains a tuple of a key/value pair stored in the hashmap.

A HashMap object takes two parameters: the capacity of the hash table, and the hashmap function for indexing hashmap keys. The capacity is set to be a prime number. If a non-prime number is given, the next greatest prime number is chosen. The hashmaps were tested for storing between 0 and 1,000,000 objects. 

## Separate Chaining Implementation
Class HashMap uses a dynamic array to store a hash table and uses a singly linked list to handle collisions.  Chains of key/value pairs are stored in linked list nodes. File hash_map_sc.py contains an additional function find_mode which takes a dynamic array and returns a tuple containing a dynamic array of mode values and an integer that represents the mode frequency. 
### Separate Chaining Example 
![image](https://github.com/boothcat/A-Tale-of-Two-HashMaps/assets/97126252/d43740d9-0251-45e7-a539-b8315db69246)
![image](https://github.com/boothcat/A-Tale-of-Two-HashMaps/assets/97126252/d192f505-5d4a-4512-acb6-16c994821634)

FindMode Function Example:
![image](https://github.com/boothcat/A-Tale-of-Two-HashMaps/assets/97126252/3949b304-958f-4c7f-84a2-b930548f3326)

## Open Addressing Implementation
Class HashMap uses a dynamic array to store a hash table and uses open addressing with quadratic probing to handle collision. In this implementation, the hash table's capacity is doubled when the current load factor of the table is greater than or equal to 0.5. 
![image](https://github.com/boothcat/A-Tale-of-Two-HashMaps/assets/97126252/efa03ad7-3f1a-4fe8-926a-4c673fb2e21b)
![image](https://github.com/boothcat/A-Tale-of-Two-HashMaps/assets/97126252/1d75e45a-f016-492d-a10a-ee73db469e01)



