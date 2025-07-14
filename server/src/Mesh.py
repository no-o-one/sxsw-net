class Mesh:
    #ids can be 0-65535
    #65535 is reseved for the server's module
    def __init__(self, mesh = [[]], has_center = False):
        self.mesh = mesh
        self.has_center = has_center
    
    def get_nodes(self, branch_id=None):
        """ARGS > branch_id:int (optional, returns all nodes in all branches if not specified)
        returns all node ids in the mesh as a list"""
        if branch_id == None:
            toreturn = []
            for branch in self.mesh:
                for node in branch:
                    toreturn.append(node)
            return toreturn
        else:
            return self.mesh[branch_id]
    
    def get_branches(self):
        """returns all branch ids as a list"""
        toreturn = []
        for branch in self.mesh:
            toreturn.append[branch.index()]
        return toreturn

    def empty_mesh(self):
        """deletes all nodes and branches from the mesh"""
        self.has_center = False
        self.mesh = [[]]