#!/usr/bin/env python3

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
        md.write('''\
#!/bin/sh

# run this script to automatically get all the required mods

mods=(
    https://codeload.github.com/minetest-mods/mesecons/zip/master,mesecons
    https://codeload.github.com/LNJ2/carpet/zip/master,carpet
    https://codeload.github.com/minetest-mods/crops/zip/master,crops
    https://codeload.github.com/minetest-mods/flowerpot/zip/master,flowerpot
    https://codeload.github.com/minetest-mods/lapis/zip/master,lapis
    https://codeload.github.com/minetest-mods/quartz/zip/master,quartz
    https://codeload.github.com/minetest-mods/xdecor/zip/master,xdecor
    https://codeload.github.com/oOChainLynxOo/hardenedclay/zip/master,hardenedclay
    https://codeload.github.com/minetest-mods/nether/zip/master,nether
    https://codeload.github.com/ShadowNinja/minetest_bedrock/zip/master,minetest_bedrock
    https://gitlab.com/VanessaE/basic_materials/-/archive/master/basic_materials-master.zip,basic_materials
    https://gitlab.com/VanessaE/biome_lib/-/archive/master/biome_lib-master.zip,biome_lib
    https://gitlab.com/VanessaE/plantlife_modpack/-/archive/master/plantlife_modpack-master.zip,plantlife_modpack
    https://gitlab.com/VanessaE/signs_lib/-/archive/master/signs_lib-master.zip,signs_lib
)

cd worldmods

for item in ${mods[@]} ; do
(
    url=$(echo $item | cut -d, -f1)
    mod=$(echo $item | cut -d, -f2)
    echo "Fetching: $mod"
    curl -q -L -o $mod.zip $url
    unzip -qq $mod.zip
    rm $mod.zip
    mv $mod-master $mod
    mv minetest_bedrock bedrock
)
done

# remove unneeded/unwanted submods
for ex in plantlife_modpack/dryplants plantlife_modpack/along_shore plantlife_modpack/molehills plantlife_modpack/woodsoils plantlife_modpack/bushes plantlife_modpack/bushes_classic plantlife_modpack/youngtrees plantlife_modpack/3dmushrooms plantlife_modpack/cavestuff plantlife_modpack/poisonivy plantlife_modpack/trunks; do
    echo "Pruning: $ex"
    rm -rf $ex
done
''')
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IXUSR)

mcmap = MCMap(sys.argv[1])
mtmap = MTMap(sys.argv[2])

nimap, ct = content.read_content(["NETHER", "QUARTZ"])
mtmap.fromMCMap(mcmap, nimap, ct)
mtmap.save()

print("Conversion finished!\n")
print("Run \"sh get-mods.sh\" in the new world folder to automatically download all required mods.")
