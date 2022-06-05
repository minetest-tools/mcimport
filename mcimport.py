#!/usr/bin/env python3

import os
import shutil
import stat
import sys
import logging
from block import *
import content

logging.basicConfig(level=logging.INFO)

if (sys.version_info < (3, 0)):
    print("This script does not work with Python < 3.0, sorry.")
    exit(1)

if not os.path.exists(sys.argv[1]):
    print("The provided minecraft world path does not exist.")
    exit(1)

if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

if os.path.exists(sys.argv[2] + "map.sqlite"):
    print("A minetest world already exists - refusing to overwrite it.")
    exit(1)

if not os.path.exists(sys.argv[2] + "/world.mt"):
    with open(sys.argv[2] + "/world.mt", "w") as wo:
        wo.write("backend = sqlite3\n")
        wo.write("gameid = minetest\n")

if not os.path.exists(sys.argv[2] + "/worldmods"):
    os.makedirs(sys.argv[2]+"/worldmods")
if not os.path.exists(sys.argv[2] + "/worldmods/mcimport"):
    os.makedirs(sys.argv[2]+"/worldmods/mcimport")
if not os.path.exists(sys.argv[2]+"/worldmods/mcimport/init.lua"):
    with open(sys.argv[2]+"/worldmods/mcimport/init.lua", "w") as sn:
        sn.write("-- map conversion requires a special water level\n")
        sn.write("minetest.set_mapgen_params({water_level = -2})\n\n")
        sn.write("-- prevent overgeneration in incomplete chunks, and allow lbms to work\n")
        sn.write("minetest.set_mapgen_params({chunksize = 1})\n\n")
        sn.write("-- comment the line below if you want to enable mapgen (will destroy things!)\n")
        sn.write("minetest.set_mapgen_params({mgname = \"singlenode\"})\n\n")
        sn.write("-- below lines will recalculate lighting on map block load\n")
        sn.write("minetest.register_on_generated(function(minp, maxp, seed)\n")
        sn.write("        local vm = minetest.get_voxel_manip(minp, maxp)\n")
        sn.write("        vm:set_lighting({day = 15, night = 0}, minp, maxp)\n")
        sn.write("        vm:update_liquids()\n")
        sn.write("        vm:write_to_map()\n")
        sn.write("        vm:update_map()\n")
        sn.write("end)\n\n")

get_mods = os.path.join(os.path.dirname(sys.argv[0]), "get_mods.py")
shutil.copy(get_mods, sys.argv[2])

mcmap = MCMap(sys.argv[1])
mtmap = MTMap(sys.argv[2])

nimap, ct = content.read_content(["NETHER", "QUARTZ"])
mtmap.fromMCMap(mcmap, nimap, ct)
mtmap.save()

print("Conversion finished!\n")
print("Run \"python3 get_mods.py\" in the new world folder to automatically download all required mods.")
