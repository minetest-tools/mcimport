#!/bin/env python

import os
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

if not os.path.exists(sys.argv[2]+"/get-mods.sh"):
    path = sys.argv[2]+"/get-mods.sh"
    with open(path, "w") as md:
        md.write("#!/bin/sh\n")
        md.write("# run this script to automatically get all the required mods\n")
        md.write("cd worldmods\n")
        md.write("for mod in LNJ2/carpet minetest-mods/signs_lib kilbith/xdecor minetest-mods/plantlife_modpack minetest-mods/homedecor_modpack Jeija/minetest-mod-mesecons minetest-mods/moreblocks pilzadam/nether minetest-mods/crops minetest-mods/quartz minetest-mods/biome_lib oOChainLynxOo/hardenedclay; do\n")
        md.write("    echo \"Fetching: $mod\"\n")
        md.write("    s=`basename $mod`\n")
        md.write("    curl -q -L -o master.zip https://codeload.github.com/$mod/zip/master\n")
        md.write("    unzip -qq master.zip\n")
        md.write("    rm master.zip\n")
        md.write("    mv $s-master $s\n")
        md.write("done\n")
        md.write("for ex in plantlife_modpack/dryplants plantlife_modpack/along_shore plantlife_modpack/molehills plantlife_modpack/woodsoils plantlife_modpack/bushes plantlife_modpack/bushes_classic plantlife_modpack/youngtrees plantlife_modpack/3dmushrooms plantlife_modpack/cavestuff plantlife_modpack/poisonivy plantlife_modpack/trunks homedecor_modpack/fake_fire homedecor_modpack/computer homedecor_modpack/plasmascreen homedecor_modpack/lavalamp homedecor_modpack/building_blocks homedecor_modpack/inbox homedecor_modpack/homedecor_3d_extras homedecor_modpack/chains homedecor_modpack/lrfurn; do\n");
        md.write("    echo \"Pruning: $ex\"\n")
        md.write("    rm -rf $ex\n")
        md.write("done\n")
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IXUSR)

mcmap = MCMap(sys.argv[1])
mtmap = MTMap(sys.argv[2])

nimap, ct = content.read_content(["NETHER", "QUARTZ"])
mtmap.fromMCMap(mcmap, nimap, ct)
mtmap.save()

print("Conversion finished!\n")
print("Run \"sh get-mods.sh\" in the new world folder to automatically download all required mods.")
