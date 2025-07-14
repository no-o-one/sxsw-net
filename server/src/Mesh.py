class Mesh:
    #ids can be 0-65535
    #65535 is reseved for the server's module
    def __init__(self, mesh = [[]], has_center = False):
        self.mesh = mesh
        self.has_center = has_center
    
    def get_nodes(self, branch_id=None): #get nodes as a list; if branch not provided returns all nodes of the mesh
        if branch_id == None:
            toreturn = []
            for branch in self.mesh:
                for node in branch:
                    toreturn.append(node)
            return toreturn
        else:
            return self.mesh[branch_id]
    
    def get_branches(self):
        toreturn = []
        for branch in self.mesh:
            toreturn.append[branch.index()]
        return toreturn

    def empty_mesh(self):
        self.has_center = False
        self.mesh = [[]]