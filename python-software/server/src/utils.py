def ping(id_to_ping):
    id_to_ping

def pingall():
    pass

def send_all_nodes(mesh, lora_module, msg:str):
    for branch in mesh.mesh:
        for node in branch:
            print(f'sent to branch {branch}, node {node}, msg {msg}')
            lora_module.send(node, msg.encode("ascii"))
