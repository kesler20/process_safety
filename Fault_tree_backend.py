
class FaultTree(object):

    def __init__(self,height):

        height : int

        self.height = height
        self.structure = []
        self.tree_architecture = self.init_tree_architecture(self.height, 0)

    def __str__(self):
        return f'''
            FaultTree (
                structure : {self.tree_architecture}
            )
        '''
        
    def init_tree_architecture(self,height, width):
        if len(self.structure) < height:
            for i in range(height + 1):
                self.structure.append([])
        else:
            for i in range(width + 1):
                try:
                    self.structure[height].append([])
                except IndexError:
                    for i in range(height + 1):
                        self.structure.append([])
                    for i in range(width + 1):
                        self.structure[height].append([])
        return self.structure

    
    def find_leaf_by_location(self,height, width):
        leaf = self.tree_architecture[height][width]
        return leaf

        
    def add_leaf_to_tree(self, leaves_objcts, operator):
        if operator == 'OR':
            leaves_objcts_values = []
            for leaf in leaves_objcts:
                leaves_objcts_values.append(leaf['value'])
            leaf_obj = {
                'value': sum(leaves_objcts_values),
                'operator': operator,
                'width': leaves_objcts[0]['width'],
                'height': leaves_objcts[0]['height']
            }
        else:
            leaf_obj_value = 1
            for leaf in leaves_objcts:
                leaf_obj_value *= leaf['value']
            leaf_obj = {
                'value': leaf_obj_value,
                'operator': operator,
                'width': leaves_objcts[0]['width'],
                'height': leaves_objcts[0]['height']
            }
            
        try:
            self.tree_architecture[leaf_obj['height']][leaf_obj['width']].append(leaf_obj)
        except IndexError:
            print(self.tree_architecture)
            self.init_tree_architecture(leaf_obj['height'],leaf_obj['width'])
            self.tree_architecture[leaf_obj['height']][leaf_obj['width']].append(leaf_obj)
        return self.tree_architecture

class Leaf(object):

    def __init__(self, value, height, width):
        
        value : int
        height : int
        width : int

        self.value = value
        self.height = height
        self.width = width
    
    def __repr__(self):
        return f'''
            Leaf (
                'value' : {self.value},
                'height' : {self.height},
                'width' : {self.width},
            )

        '''

    def insert_leaf(self):
        return {
            'value' : self.value,
            'height' : self.height,
            'width' : self.width,
            'operator' : None
        }

# initialize a leaf 
# initialize fault tree with number of levels
ft = FaultTree(4)
lf1 = Leaf(0.1,0,0)
lf2 = Leaf(0.02,0,0)
lf3 = Leaf(0.09,0,0)

lf4 = Leaf(1,0,1).insert_leaf()

lf5 = Leaf(0.2,0,2)
lf6 = Leaf(0.05,0,2)
lf7 = Leaf(0.1,0,2)
#iniytialise a block where to store the leaves 
fuel = []
fuel.append(lf1.insert_leaf())
fuel.append(lf2.insert_leaf())
fuel.append(lf3.insert_leaf())

ignition = []
ignition.append(lf5.insert_leaf())
ignition.append(lf6.insert_leaf())
ignition.append(lf7.insert_leaf())
# compute the result by adding boxes to tree
or_1 = ft.add_leaf_to_tree(fuel, 'OR')
or_2 = ft.add_leaf_to_tree(ignition, 'OR')

output_leaf = []
output_leaf.append(or_1[0][0][0])
output_leaf.append(or_2[0][2][0]) # UNDERSTAND HOW ALL THIS RELATE 
output_leaf.append(lf4)
print(output_leaf)
ft.add_leaf_to_tree(output_leaf, 'AND')
print(ft)

http = 'https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas-methods.html'