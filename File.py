class node:
  def __init__(self,data):
    self.data = data
    self.next_node = None

class queue:
  def __init__(self,data):
    self.first_node = node(data)
    self.sizes = 1

  def __str__(self):
    txt = str(self.first_node.data)

    current_node = self.first_node
    while current_node.next_node != None:
      current_node = current_node.next_node
      txt += str(current_node.data)
    
    return txt

  def push(self,data):
    if self.first_node == None:
      self.first_node = node(data)
      return

    current_node = self.first_node
    while current_node.next_node != None:
      current_node = current_node.next_node

    current_node.next_node = node(data)
    self.sizes += 1

  def pop(self):
    temp_data = self.first_node.data
    self.first_node = self.first_node.next_node
    return temp_data

  def peek(self):
    return self.first_node.data

  def size(self):
    return self.sizes

Queue = queue(None)