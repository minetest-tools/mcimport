import zlib, gzip
import struct
import os
import sys
from io import StringIO

def nbt_read_tag(bytes, index, tag):
    if tag <= 6:
        plen = (None, 1, 2, 4, 8, 4, 8)[tag]
        value = struct.unpack(">"+(None, "b", "h", "i", "q", "f", "d")[tag],
                                bytes[index:index+plen])[0]
        index += plen
        return value, index
    elif tag == 7:
        plen, index = nbt_read_tag(bytes, index, 3)
        value = list(struct.unpack(">"+str(plen)+"B", bytes[index:index+plen]))
        index += plen
        return value, index
    elif tag == 11:
        plen, index = nbt_read_tag(bytes, index, 3)
        value = list(struct.unpack(">"+str(plen)+"i", bytes[index:index+4*plen]))
        index += 4*plen
        return value, index
    elif tag == 8:
        plen, index = nbt_read_tag(bytes, index, 2)
        value = bytes[index:index+plen].decode('utf-8')
        index += plen
        return value, index
    elif tag == 9:
        tagid = bytes[index]
        index += 1
        plen, index = nbt_read_tag(bytes, index, 3)
        value = []
        for i in range(plen):
            v, index = nbt_read_tag(bytes, index, tagid)
            value.append(v)
        return value, index
    elif tag == 10:
        return nbt_read_named(bytes, index)

def nbt_read_named(bytes, index):
    d = {}
    while True:
        if index >= len(bytes):
            return d, index
        tag = bytes[index]
        index += 1
        if tag == 0:
            return d, index
        name, index = nbt_read_tag(bytes, index, 8)
        value, index = nbt_read_tag(bytes, index, tag)
        d[name] = value

def nbt_read(bytes):
    return nbt_read_named(bytes, 0)[0]

def to_int(bytes):
    s = 0
    for x in bytes:
        s = (s<<8) + x
    return s

def remove_half_bytes(d, key):
    l = []
    for x in d[key]:
        l.append(x&0xf)
        l.append((x>>4)&0xf)
    d[key] = l

def to_anvil_data(block, key):
    data = block[key]
    del block[key]
    l = [block["Sections"][i][key] for i in range(8)]
    for yslice in range(8):
        l_yslice = l[yslice]
        k = 0
        k2 = yslice << 4
        for y in range(16):
            for z in range(16):
                for x in range(16):
                    l_yslice[k] = data[k2]
                    k += 1
                    k2 += 2048
                k2 = (k2&0x7ff)+128
            k2 = (k2&0x7f)+1
                    
def format_block(block):
    if block.get("isFormatted", False):
        return block
    block["isFormatted"] = True
    if block.get("Sections", None) != None:
        for section in block["Sections"]:
            remove_half_bytes(section, "Data")
            remove_half_bytes(section, "BlockLight")
            remove_half_bytes(section, "SkyLight")
        return block
    remove_half_bytes(block, "Data")
    remove_half_bytes(block, "BlockLight")
    remove_half_bytes(block, "SkyLight")
    block["Sections"] = [{"Y":i, "Blocks":[0]*4096, "Data":[0]*4096,
                          "BlockLight":[0]*4096, "SkyLight":[0]*4096}
                          for i in range(8)]
    to_anvil_data(block, "Blocks")
    to_anvil_data(block, "Data")
    to_anvil_data(block, "BlockLight")
    to_anvil_data(block, "SkyLight")
    return block
    

def read_block(f, blockx, blockz):
    ofs = (blockx%32 + (blockz%32)*32)*4
    f.seek(ofs)
    offset = to_int(f.read(3))<<12
    if offset == 0:
        return
    f.seek(offset)
    length = struct.unpack(">i", f.read(4))[0]
    ctype = struct.unpack(">b", f.read(1))[0]
    data = f.read(length - 1)
    udata = zlib.decompress(data)
    block = nbt_read(udata)['']["Level"]
    return block

def read_dir(dirname):
    filenames = [i for i in os.listdir(dirname) if i.endswith(".mcr") or i.endswith(".mca")]
    blocks = {}
    for filename in filenames:
        s = filename.split(".")
        chkx, chkz = int(s[1])*32, int(s[2])*32
        with open(dirname+filename, "rb") as f:
            for blockx in range(chkx, chkx+32):
                for blockz in range(chkz, chkz+32):
                    block = read_block(f, blockx, blockz)
                    if block != None:
                        blocks[(blockx, blockz)] = block
    return blocks

def read_content():
    f = open("map_content.txt", "r")
    lines = f.readlines()
    f.close()

    lines.reverse()

    bd = {}
    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]
        line = line.split("#")[0] # Remove comment
        s = line.split("\t")
        if len(s) >= 2:
            r = s[1].split(" ")
            if len(r) == 0:
                print(line)
                raise ValueError("Malformed data")
            name = r[0]
            param2 = 0
            for i in range(1, len(r)):
                if r[i] != "":
                    param2 = int(r[i])
                    break
            t = s[0].split(" ")
            if len(t) == 2:
                bd[(int(t[0]), int(t[1]))] = (name, param2)
            elif len(t) == 1:
                for data in range(16):
                    bd[(int(t[0]), data)] = (name, param2)

    blocks_len = max([i[0] for i in bd.keys()])+1
    blocks = [[(None, 0),]*16 for i in range(blocks_len)]
    for (id, data), value in bd.items():
        blocks[id][data] = value
    return blocks

blocks_id = read_content()

def get_name(id, data):
    if id >= len(blocks_id):
        return None, 0
    return blocks_id[id][data]

def convert_section(section, tileentities, yslice):
    n = len(section["Blocks"])
    blocksdata = section["Blocks"]
    data = section["Data"]
    blocks = [None]*n
    param1 = [0]*n
    param2 = [0]*n
    metadata = [None]*n
    for i in range(n):
        blocks[i], param2[i] = get_name(blocksdata[i], data[i])
    return (blocks, param1, param2, metadata)

def convert_block(block, yslice):
    for section in block["Sections"]:
        if section["Y"] == yslice:
            return convert_section(section, block.get("TileEntities", []), yslice)
    return None
 
def export_we(b, f):
    blocks, param1, param2, metadata = b
    L = []
    f.write("return {")
    write_comma = False
    for i in range(len(blocks)):
        x = i%16
        z = (i//16)%16
        y = i//256
        if blocks[i] != None:
            if write_comma:
                f.write(",")
            else:
                write_comma = True
            f.write("{x="+str(x)+",y="+str(y)+",z="+str(z)+',name="'+blocks[i]+'",param1='+str(param1[i])+",param2="+str(param2[i])+",meta={fields={},inventory={}}}")
    f.write("}")

inputdir = sys.argv[1] + "region/"
blocks = read_dir(inputdir)
print("Reading done")

outputdir = sys.argv[2] + "blocks/"
if not os.path.exists(outputdir):
    os.mkdir(outputdir)

done = 0
max_number = len(blocks)
for key, value in blocks.items():
    done += 1
    if done%20 == 0:
        print("Exported {} blocks on {}".format(done, max_number))
    if value == None:
        continue
    for yslice in range(16):
        value = format_block(value)
        b = convert_block(value, yslice)
        if b == None:
            continue
        with open(outputdir+str(key[0])+"."+str(yslice-4)+"."+str(key[1])+".we", "w") as f:
            export_we(b, f)
