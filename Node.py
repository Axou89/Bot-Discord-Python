class Node:
  def __init__(self,data):
    self.data = data
    self.next_node = None
    self.previous_node = None

class list_chained:
  def __init__(self, first_data):
    self.first_node = Node(first_data)
    self.last_node = self.first_node
    self.previous_node = None
    self.sizes = 1

  def append(self,data):
    # Add element at end of list
      self.last_node.next_node = Node(data)
      self.last_node = self.last_node.next_node
      self.sizes += 1

  def insert_first(self,data):
    # Add element at start of list
      current_node = Node(data)
      current_node.next_node = self.first_node
      self.first_node = current_node
      self.sizes += 1

  def size(self):
    # Return size of list
    return self.sizes
  
  def insert(self, index, data):
    # Add element at index
    current_node = self.first_node
    i = 1
    while i < index:
      current_node = current_node.next_node
      i += 1
    new_node = Node(data)
    new_node.next_node = current_node.next_node
    current_node.next_node = new_node
    self.sizes += 1