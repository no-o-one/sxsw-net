def ping(id_to_ping):
    id_to_ping

def ping_all():
    pass

def send_all(mesh, module, msg:str):
    for branch in mesh.mesh:
        for node in branch:
            msg = f'{str(node)}  {msg}'
            print(f'sent to branch {branch}, node {node}, msg {msg}')
            module.send(node, msg.encode("ascii"))
