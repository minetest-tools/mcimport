import os
import sys
from block import *
import content

mcmap = MCMap(sys.argv[1])
mtmap = MTMap(sys.argv[2])

if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

if not os.path.exists(sys.argv[2] + "/map_meta.txt"):
    mg = open(sys.argv[2] + "/map_meta.txt", "w")
    mg.write("mg_name = singlenode\n")
    mg.write("mapgen_singlenode = \"ignore\"\n")
    mg.write("waterlevel = 63\n")
    mg.write("[end_of_params]\n")
    mg.close()

if not os.path.exists(sys.argv[2] + "/world.mt"):
    wo = open(sys.argv[2] + "/world.mt", "w")
    wo.write("backend = sqlite3\n")
    wo.write("gameid = minetest\n")
    wo.write("load_mod_biome_lib = true\n")
    wo.write("load_mod_bushes_classic = true\n")
    wo.write("load_mod_ferns = true\n")
    wo.write("load_mod_flowers_plus = true\n")
    wo.write("load_mod_homedecor = true\n")
    wo.write("load_mod_junglegrass = true\n")
    wo.write("load_mod_mesecons = true\n")
    wo.write("load_mod_moreblocks = true\n")
    wo.write("load_mod_moretrees = true\n")
    wo.write("load_mod_mushroom = true\n")
    wo.write("load_mod_nether = true\n")
    wo.write("load_mod_plants_lib = true\n")
    wo.write("load_mod_poisonivy = true\n")
    wo.write("load_mod_quartz = true\n")
    wo.write("load_mod_singlenode = true\n")
    wo.write("load_mod_vines = true\n")
    wo.close()

#os.makedirs(sys.argv[2]+"/worldmods")
#os.makedirs(sys.argv[2]+"/worldmods/singlenode")

#sn = open(sys.argv[2]+"/worldmods/singlenode/init.lua", "w")
#sn.write("minetest.set_mapgen_params({mgname = \"singlenode\"})\n")
#sn.close()

if not os.path.exists(sys.argv[2]+"/moretrees_settings.txt"):
    mo = open(sys.argv[2]+"/moretrees_settings.txt", "w")
    mo.write("moretrees.enable_apple_tree = false\n")
    mo.write("moretrees.enable_oak = false\n")
    mo.write("moretrees.enable_sequoia = false\n")
    mo.write("moretrees.enable_palm = false\n")
    mo.write("moretrees.enable_pine = false\n")
    mo.write("moretrees.enable_rubber_tree = false\n")
    mo.write("moretrees.enable_willow = false\n")
    mo.write("moretrees.enable_acacia = false\n")
    mo.write("moretrees.enable_birch = false\n")
    mo.write("moretrees.enable_spruce = false\n")
    mo.write("moretrees.enable_jungle_tree = false\n")
    mo.write("moretrees.enable_fir = false\n")
    mo.write("moretrees.enable_beech = false\n")
    mo.close()

nimap, ct = content.read_content(["MORETREES", "NETHER", "QUARTZ"])
mtmap.fromMCMap(mcmap, nimap, ct)
mtmap.save()


'''import zlib, gzip
import struct
import os
import sys
from io import StringIO
from tile_entities import te_convert

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

def read_content(enabled):
    f = open("map_content.txt", "r")
    lines = f.readlines()
    f.close()

    bd = {}
    skip_level = 0
    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]
        line = line.strip().split("//")[0].strip() # Remove comment
        if len(line) >= 1 and line[0] == "#":
            if line.startswith("#if"):
                cond = line[4:]
                if skip_level > 0 or cond not in enabled:
                    skip_level += 1
            elif line.startswith("#else"):
                if skip_level == 0:
                    skip_level = 1
                elif skip_level == 1:
                    skip_level = 0
            elif line.startswith("#endif"):
                if skip_level > 0:
                    skip_level -= 1
            continue

        if skip_level > 0:
            continue
                
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
                for data in t[1].split(","):
                    key = (int(t[0]), int(data))
                    if key not in bd:
                        bd[key] = (name, param2)
            elif len(t) == 1:
                for data in range(16):
                    key = (int(t[0]), data)
                    if key not in bd:
                        bd[key] = (name, param2)

    blocks_len = max([i[0] for i in bd.keys()])+1
    blocks = [[(None, 0),]*16 for i in range(blocks_len)]
    for (id, data), value in bd.items():
        blocks[id][data] = value
    return blocks

blocks_id = read_content(["MORETREES", "QUARTZ", "NETHER"])

def get_name(id, data):
    if id >= len(blocks_id):
        return None, 0
    return blocks_id[id][data]

def convert_section(section, tileentities, yslice):
    n = len(section["Blocks"])
    blocksdata = section["Blocks"]
    data = section["Data"]
    blocklight = section["BlockLight"]
    skylight = section["SkyLight"]
    blocks = [None]*n
    param1 = [0]*n
    param2 = [0]*n
    metadata = [None]*n
    for i in range(n):
        blocks[i], param2[i] = get_name(blocksdata[i], data[i])
        param1[i] = (max(blocklight[i], skylight[i])<<4)|blocklight[i]
    for te in tileentities:
        id = te["id"]
        x, y, z = te["x"], te["y"], te["z"]
        if y >> 4 != yslice:
            continue
        index = ((y&0xf)<<8)|((z&0xf)<<4)|(x&0xf)
        f = te_convert.get(id.lower(), lambda arg: (None,None,None))
        block, p2, meta = f(te)
        if block != None:
            blocks[index] = block
        if p2 != None:
            param2[index] = p2
        if meta != None:
            metadata[index] = meta
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
            f.write("{x="+str(x)+",y="+str(y)+",z="+str(z)+',name="'+blocks[i]+'",param1='+str(param1[i])+",param2="+str(param2[i])+",meta=")
            if metadata[i] == None:
                f.write("{fields={},inventory={}}")
            else:
                f.write(metadata[i])
            f.write("}")
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
#for key in [(i, j) for i in range(5, 9) for j in range(20, 35)]:
#    value = blocks.get(key, None)
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
'''
