import os
import machine


def file_system_setup(isverbose=False):
    filestofind = ['boot.py', 'reyax.py', 'utils.py', 'jewelutils.py', 'servoutils.py', 'animationutils.py', 'animations.py']
    for name in filestofind:
        if name not in os.listdir() and isverbose:
            print("!WARNING! "+name+" was not found in ./ directory")
    if 'src' not in os.listdir():
        os.mkdir('src')
    for name in filestofind:
        if not name == 'boot.py':
            try: 
                os.rename(name, 'src/'+name)
            except:
                if isverbose:
                    print(f'!WARNING! {name} has not been relocated')

def file_system_show():
    __traverse('', 1)


def __traverse(path, indent):
    for item in os.listdir(path):
        fullpath = path+'/'+item
        if not item.endswith('.py'):
            print('  '*indent + fullpath)
            __traverse(fullpath, indent+1)
        elif item.endswith('.py'):
            print('  '*indent + fullpath)

def pack_octal(d0, d1, d2, d3, d4) -> bytes:
    """Packs 5 octal digits (0–7 each) into exactly 2 bytes (15 bits).
    all digits MUST be 0-7, so it must be an octal number"""
    digits = [d0, d1, d2, d3, d4]
    bits = 0
    for digit in digits:
        bits = (bits << 3) | digit  # shift left 3 bits, OR in the digit
    return bits.to_bytes(2, 'big')  # 2-byte big-endian representation


def unpack_octal(packed: bytes) -> list:
    """Unpacks 2 bytes into a list of 5 octal digits (as integers)."""
    if len(packed) != 2:
        return []

    bits = int.from_bytes(packed, 'big') & 0x7FFF  # 15 bits mask
    digits = []
    for shift in range(12, -1, -3):
        digits.append((bits >> shift) & 0b111)
    return digits


