import lightserver as lightserver

def ping(id_to_ping):
    id_to_ping

def ping_all():
    pass

def send_all(msg:str):
    for branch in lightserver.thismesh.mesh:
        for node in branch:
            msg = f'{str(node)}  {msg}'
            print(f'sent to branch {branch}, node {node}, msg {msg}')
            lightserver.rylr.send(node, msg.encode("ascii"))
