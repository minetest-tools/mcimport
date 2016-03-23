#!/bin/env python

import os
import sys
from block import *
import content

if (sys.version_info < (3, 0)):
    print("This script does not work with Python < 3.0, sorry.")
    exit(1)

if not os.path.exists(sys.argv[1]):
    print("the minecraft world path does not exist.")
    exit(1)

if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

if not os.path.exists(sys.argv[2] + "/world.mt"):
    wo = open(sys.argv[2] + "/world.mt", "w")
    wo.write("backend = sqlite3\n")
    wo.write("gameid = minetest\n")
    wo.close()

if not os.path.exists(sys.argv[2] + "/worldmods"):
    os.makedirs(sys.argv[2]+"/worldmods")
if not os.path.exists(sys.argv[2] + "/worldmods/mcimport"):
    os.makedirs(sys.argv[2]+"/worldmods/mcimport")
if not os.path.exists(sys.argv[2]+"/worldmods/mcimport/init.lua"):
    sn = open(sys.argv[2]+"/worldmods/mcimport/init.lua", "w")
    sn.write("-- map conversion requires a special water level\n")
    sn.write("minetest.set_mapgen_params({water_level = -2})\n\n")
    sn.write("-- comment the line below if you want to enable mapgen (will destroy things!)\n")
    sn.write("minetest.set_mapgen_params({mgname = \"singlenode\"})\n")
    sn.close()

if not os.path.exists(sys.argv[2]+"/get-mods.sh"):
    md = open(sys.argv[2]+"/get-mods.sh", "w")
    md.write("#!/bin/sh\n")
    md.write("# run this script to automatically get all the required mods\n")
    md.write("cd worldmods\n")
    md.write("for mod in VanessaE/signs_lib VanessaE/plantlife_modpack VanessaE/homedecor_modpack Jeija/minetest-mod-mesecons calinou/moreblocks sofar/nether minetest-mods/crops minetest-mods/quartz VanessaE/biome_lib oOChainLynxOo/hardenedclay; do\n")
    md.write("    s=`basename $mod`\n")
    md.write("    curl -L -o master.zip https://codeload.github.com/$mod/zip/master\n")
    md.write("    unzip master.zip\n")
    md.write("    rm master.zip\n")
    md.write("    mv $s-master $s\n")
    md.write("done\n")
    md.close()

mcmap = MCMap(sys.argv[1])
mtmap = MTMap(sys.argv[2])

nimap, ct = content.read_content(["NETHER", "QUARTZ"])
mtmap.fromMCMap(mcmap, nimap, ct)
mtmap.save()

print("Conversion finished!\n")
print("Run \"sh get-mods.sh\" in the new world folder to automatically download all required mods.")
