import ast
import itertools

class NodeTransformer(ast.NodeTransformer):
    def __init__(self, assign_class: str = 'Node', keyword_name: str = 'edges'):
        self.assign_class = assign_class
        self.keyword_name = keyword_name
        self.neighbors = dict()
        self.parsing_errors = []
        self.is_valid_now = True
    
    def is_valid(self) -> bool:
        # each name initialized with Node() assignment will be in self.neighbors.keys()
        nodes = set(itertools.chain.from_iterable(self.neighbors.values()))
        for node in nodes:
            if node not in self.neighbors.keys():
                self.parsing_errors.append(f'Missing node error: {node} was not initialized!')
        status = '\n'.join(self.parsing_errors) if len(self.parsing_errors) else 'OK'
        return status

    def get_graph(self) -> dict:
        return self.neighbors

    def visit_Assign(self, node: ast.Assign):
        if not self.is_valid_now:
            return
        # incorrect initialization: `source = Node`
        if isinstance(node.value, ast.Name) and node.value.id == self.assign_class:
            source_node = node.targets[0].id
            err = f'Node initialization error: node {source_node} initialized incorrectly! Try Node() notation.'
            self.is_valid_now = False
            self.parsing_errors.append(err)
            return
        if isinstance(node.value, ast.Call) and node.value.func.id == self.assign_class:
            source_node = node.targets[0].id
            if source_node not in self.neighbors:
                self.neighbors[source_node] = []
            for keyword in node.value.keywords:
                if keyword.arg != self.keyword_name:
                    self.parsing_errors.append(f'Unexpected keyword {keyword.arg} detected during node {source_node} initialization. \n' 
                                                'Expected empty list or `edges` keyword.')
                    self.is_valid_now = False
                    return
                if keyword.arg == self.keyword_name and isinstance(keyword.value, ast.List):
                    new_neighbors = [name.id for name in keyword.value.elts]
                    if len(new_neighbors) > 0:
                        self.neighbors[source_node].extend(new_neighbors)
