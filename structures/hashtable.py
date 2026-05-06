class MyHashTable:
    _DELETED = object()

    def __init__(self, capacity=11):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def put(self, key, value):

        if (self.size / self.capacity) > 0.7:
            self.rehash()

        h1 = hash(key) % self.capacity
        h2 = 1 + hash(key) % (self.capacity - 1)

        first_deleted = None
        
        for i in range(self.capacity):

            index = (h1 + i * h2) % self.capacity

            if self.table[index] is None:

                target_ind = first_deleted if first_deleted is not None else index
                self.table[target_ind] = (key, value)
                self.size += 1
                return 
            
            if self.table[index] is self._DELETED:
                if first_deleted is None:
                    first_deleted = index

                continue 

            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return

        if first_deleted is not None:
            self.table[first_deleted] = (key, value)
            self.size += 1
        else:
            raise Exception("Table is full ")

    def rehash(self):
        old_table = self.table
        self.capacity = self.capacity * 2 + 1
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None and item is not self._DELETED:
                self.put(item[0], item[1])

    
    def get(self, key):
        h1 = hash(key) % self.capacity
        h2 = 1 + hash(key) % (self.capacity - 1)

        for i in range(self.capacity):
            index = (h1 + i * h2) % self.capacity

            if self.table[index] is None:
                break

            if self.table[index] is not self._DELETED and self.table[index][0] == key:
                return self.table[index][1]
            
        raise KeyError(f"Key {key} is not found")
        
    def __len__(self):
        return self.size

    def remove(self, key):
        h1 = hash(key) % self.capacity
        h2 = 1 + hash(key) % (self.capacity - 1)

        for i in range(self.capacity):
            index = (h1 + i * h2) % self.capacity

            if self.table[index] is None:
                break

            if self.table[index] is not self._DELETED and self.table[index][0] == key:
               self.table[index] = self._DELETED
               self.size -= 1 
               return 
            
        raise KeyError(f"Key {key} is not found")
    
    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __iter__(self):
        for item in self.table:
            if item is not None and item is not self._DELETED:
                yield item[0]

    def items(self):
        for item in self.table:
            if item is not None and item is not self._DELETED:
                yield item