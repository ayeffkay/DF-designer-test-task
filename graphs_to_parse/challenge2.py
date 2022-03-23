a = Node(edges=[b])
b = Node(edges=[c, d])
c = Node()
d = Node()

# everything that is not a node should be ignored
e = 12
def hello():
  return 'hello'