class Node:
  def __init__(self,data,author):
    self.data = data
    self.author = author
    self.next_node = None
    self.previous_node = None

class list_chained:
  def __init__(self, first_data, first_author):
    self.first_node = Node(first_data, first_author)
    self.last_node = self.first_node
    self.previous_node = None
    self.sizes = 1

  def append(self,data,author):
    # Add element at end of list
      self.last_node.next_node = Node(data,author)
      self.last_node = self.last_node.next_node
      self.sizes += 1

  def insert_first(self,data,author):
    # Add element at start of list
      current_node = Node(data,author)
      current_node.next_node = self.first_node
      self.first_node = current_node
      self.sizes += 1

  def size(self):
    # Return size of list
    return self.sizes
  
  def insert(self, index, data, author):
    # Add element at index
    current_node = self.first_node
    i = 1
    while i < index:
      current_node = current_node.next_node
      i += 1
    new_node = Node(data, author)
    new_node.next_node = current_node.next_node
    current_node.next_node = new_node
    self.sizes += 1