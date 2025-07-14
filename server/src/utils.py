import time

def ping(id_to_ping):
    id_to_ping

def ping_all():
    pass

def send_all(mesh, module, msg:str, delay_branch=0, delay_node=0):
    """ARGS > mesh:Mesh, module:RYLR998, delay_branch:int(optional), delay_node:int(optional)"""
    for branch in mesh.mesh:
        for node in branch:
            print(f'sent to branch {branch}, node {node}, msg {msg}')
            module.send(node, msg.encode("ascii"))
            time.sleep(delay_node)
        time.sleep(delay_branch)
