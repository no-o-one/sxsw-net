import time

def ping(id_to_ping):
    pass

def ping_all():
    pass

#send to all nodes with delay for animations, to sent to all insantaniously send to id 0
def send_all(mesh, module, msg:str, delay_node=0, delay_branch=0):
    """ARGS > mesh:Mesh, module:RYLR998, delay_node:int(optional), delay_branch:int(optional)"""
    for branch in mesh.mesh:
        for node in branch:
            print(f'sent to branch {branch}, node {node}, msg {msg}')
            module.send(node, msg.encode("ascii"))
            time.sleep(delay_node)
        time.sleep(delay_branch)
