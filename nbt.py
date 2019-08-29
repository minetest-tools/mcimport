import struct

def _read_tag(bytes, index, tag):
    if tag <= 6:
        plen = (None, 1, 2, 4, 8, 4, 8)[tag]
        value = struct.unpack(">"+(None, "b", "h", "i", "q", "f", "d")[tag],
                                bytes[index:index+plen])[0]
        index += plen
        return value, index
    elif tag == 7:
        plen, index = _read_tag(bytes, index, 3)
        value = list(struct.unpack(">"+str(plen)+"B", bytes[index:index+plen]))
        index += plen
        return value, index
    elif tag == 11:
        plen, index = _read_tag(bytes, index, 3)
        value = list(struct.unpack(">"+str(plen)+"i", bytes[index:index+4*plen]))
        index += 4*plen
        return value, index
    elif tag == 12:
        plen, index = _read_tag(bytes, index, 3)
        value = list(struct.unpack(">"+str(plen)+"q", bytes[index:index+8*plen]))
        index += 8*plen
        return value, index
    elif tag == 8:
        plen, index = _read_tag(bytes, index, 2)
        value = bytes[index:index+plen].decode('utf-8')
        index += plen
        return value, index
    elif tag == 9:
        tagid = bytes[index]
        index += 1
        plen, index = _read_tag(bytes, index, 3)
        value = []
        for i in range(plen):
            v, index = _read_tag(bytes, index, tagid)
            value.append(v)
        return value, index
    elif tag == 10:
        return _read_named(bytes, index)
    else:
        raise Exception("Unknown tag: " + str(tag))

def _read_named(bytes, index):
    d = {}
    while True:
        if index >= len(bytes):
            return d, index
        tag = bytes[index]
        index += 1
        if tag == 0:
            return d, index
        name, index = _read_tag(bytes, index, 8)
        value, index = _read_tag(bytes, index, tag)
        d[name] = value

def read(bytes):
    return _read_named(bytes, 0)[0]
