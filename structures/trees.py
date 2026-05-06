import json
from pathlib import Path
from .snapshot import PickleSnapshots

class Node:
    def __init__(self, key, value ):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree(PickleSnapshots):
    def __init__(self):
        self.root = None

    def  __insert_rec(self, node, key, value):
        if node is None:
            return Node(key, value)
        
        if key == node.key:
            node.value = value
            return node

        if node.key > key:
            node.left = self.__insert_rec(node.left, key, value)
        
        else:
            node.right = self.__insert_rec(node.right, key, value)

        return node
    
    def insert(self, key, value):
        self.root = self.__insert_rec(self.root, key, value)
        self.log_history(key)

    def __search_rec(self, node, key ):
        if node is None:
            raise KeyError(f"Key {key} is not found ") 
        
        if key == node.key:
            return node.value
        
        if node.key > key:
            return self.__search_rec(node.left, key)
        else:
            return self.__search_rec(node.right, key)
        

    def search(self, key):
            return self.__search_rec(self.root, key)
    

    def __find_min_rec(self, node):

        if node.left is None:
            return node
        
        return self.__find_min_rec(node.left)
    
    def find_min(self):

        if self.root is None:
            return None
        
        min_node = self.__find_min_rec(self.root)

        return (min_node.key, min_node.value)
    

    def __find_max_rec(self, node):
        if node.right is None: 
            return node
        
        return self.__find_max_rec(node.right)
    
    def find_max(self):
        if self.root is None:
            return None
        
        max_node = self.__find_max_rec(self.root)

        return (max_node.key, max_node.value)

    def __InOrder(self, node):

        if node is None:
            return  
        
        yield from self.__InOrder(node.left)
        yield (node.key, node.value)
        yield from self.__InOrder(node.right)

    def inorder_traversal(self):
        return self.__InOrder(self.root)
    

    def __get_height_rec(self, node):
        if node is None:
            return 0
        
        height = max(self.__get_height_rec(node.left), self.__get_height_rec(node.right)) + 1

        return height

    def __find_node(self, node, key):

        if node is None or node.key == key:
            return node
    
        if node.key > key:
            return self.__find_node(node.left, key)
        else:
            return self.__find_node(node.right, key)
    

    def get_height(self, key=None):
        if key is None:
            return self.__get_height_rec(self.root)
        
        target_node = self.__find_node(self.root, key)
        if target_node is None:
            raise KeyError(f"Key {key} is not found")
        
        return self.__get_height_rec(target_node)
    

    def __find_range(self, node, min_key, max_key, result):
      if node is None:
          return

      if node.key > min_key:
          self.__find_range(node.left, min_key, max_key, result)

      if min_key <= node.key <= max_key:
          result.append((node.key, node.value))
          
      
      if node.key < max_key:
          self.__find_range(node.right, min_key, max_key, result)
      
      

    def find_range(self, min_key, max_key):
       result = []
       self.__find_range(self.root, min_key, max_key, result)
    
       return result


    def __deleted_rec(self, node, key):
        
        if node is None:
            raise KeyError(f"Key {key} is not found ")
        
        if node.key > key:
            node.left = self.__deleted_rec(node.left, key)

        elif node.key < key:
            node.right = self.__deleted_rec(node.right, key)

        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            repl = self.__find_min_rec(node.right)

            node.key = repl.key
            node.value = repl.value

            node.right = self.__deleted_rec(node.right, repl.key)

        return node
    
    def delete(self, key):
        self.root = self.__deleted_rec(self.root, key)  

    def __validate(self, node, min_v, max_v):
        if node is None:
            return True
        
        if not(min_v < node.key < max_v):
            return False
        
        result = (self.__validate(node.left, min_v, node.key) and self.__validate(node.right, node.key, max_v))

        return result

    def is_valid_bst(self):
        return self.__validate(self.root, float('-inf'), float('inf'))
    
    def save_to_json(self, file_path):
        path = Path(file_path)

        data = []
        for k, v in self.inorder_traversal():
           node_dict = {"key": k, "value" : v}

           data.append(node_dict)            

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, file_path):
        path = Path(file_path)

        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)

                for item in data:
                    self.insert(item["key"], item["value"])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
        except json.JSONDecodeError:
            raise ValueError(f"File {file_path} corrupted")
            

   

class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self.__push_left(root)

    def __push_left(self, node):
        while node is not None:
            self.stack.append(node)
            node = node.left

    def hasNext(self):
        return len(self.stack) > 0
    
    def next(self):
        node = self.stack.pop()

        if node.right is not None:
            self.__push_left(node.right)

        return (node.key, node.value)