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

#if not os.path.exists(sys.argv[2] + "/map_meta.txt"):
#    mg = open(sys.argv[2] + "/map_meta.txt", "w")
#    mg.write("chunksize = 5\n")
#    mg.write("#mg_name = v6\n")
#    mg.write("mg_name = singlenode\n")
#    mg.write("mgv6_spflags = nojungles, biomeblend, mudflow, nosnowbiomes\n")
#    mg.write("mapgen_singlenode = \"ignore\"\n")
#    mg.write("waterlevel = -2\n")
#    mg.write("[end_of_params]\n")
#    mg.close()

if not os.path.exists(sys.argv[2] + "/world.mt"):
    wo = open(sys.argv[2] + "/world.mt", "w")
    wo.write("backend = sqlite3\n")
    wo.write("gameid = minetest\n")
    wo.write("load_mod_mcimport = true\n")
    wo.write("load_mod_biome_lib = true\n")
    wo.write("load_mod_bushes_classic = true\n")
    wo.write("load_mod_crops = true\n")
    wo.write("load_mod_ferns = true\n")
    wo.write("load_mod_flowers_plus = true\n")
    wo.write("load_mod_homedecor = true\n")
    wo.write("load_mod_junglegrass = true\n")
    wo.write("load_mod_mesecons = true\n")
    wo.write("load_mod_mesecons_button = true\n")
    wo.write("load_mod_mesecons_commandblock = true\n")
    wo.write("load_mod_mesecons_delayer = true\n")
    wo.write("load_mod_mesecons_doors = true\n")
    wo.write("load_mod_mesecons_lamp = true\n")
    wo.write("load_mod_mesecons_lightstone = true\n")
    wo.write("load_mod_mesecons_materials = true\n")
    wo.write("load_mod_mesecons_mvps = true\n")
    wo.write("load_mod_mesecons_noteblock = true\n")
    wo.write("load_mod_mesecons_pistons = true\n")
    wo.write("load_mod_mesecons_pressureplates = true\n")
    wo.write("load_mod_mesecons_receiver = true\n")
    wo.write("load_mod_mesecons_solarpanel = true\n")
    wo.write("load_mod_mesecons_switch = true\n")
    wo.write("load_mod_mesecons_torch = true\n")
    wo.write("load_mod_mesecons_walllever = true\n")
    wo.write("load_mod_moreblocks = true\n")
    wo.write("load_mod_moretrees = false\n")
    wo.write("load_mod_nether = true\n")
    wo.write("load_mod_poisonivy = true\n")
    wo.write("load_mod_quartz = true\n")
    wo.write("load_mod_vines = true\n")
    wo.write("load_mod_signs = true\n")
    wo.write("load_mod_signs_lib = true\n")
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

if not os.path.exists(sys.argv[2]+"/moretrees_settings.txt"):
    mo = open(sys.argv[2]+"/moretrees_settings.txt", "w")
    mo.write("-- comment these lines if you want moretrees to spawn naturally\n")
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

if not os.path.exists(sys.argv[2]+"/get-mods.sh"):
    md = open(sys.argv[2]+"/get-mods.sh", "w")
    md.write("#!/bin/sh\n")
    md.write("# run this script to automatically get all the required mods\n")
    md.write("git clone https://github.com/VanessaE/plantlife_modpack worldmods/plantlife_modpack\n")
    md.write("git clone https://github.com/VanessaE/homedecor_modpack worldmods/homedecor_modpack\n")
    md.write("git clone https://github.com/Jeija/minetest-mod-mesecons worldmods/mesecons\n")
    md.write("git clone https://github.com/calinou/moreblocks worldmods/moreblocks\n")
    md.write("git clone https://github.com/sofar/nether worldmods/nether\n")
    md.write("git clone https://github.com/minetest-mods/quartz worldmods/quartz\n")
    md.write("git clone https://github.com/VanessaE/biome_lib worldmods/biome_lib\n")
    md.close()

mcmap = MCMap(sys.argv[1])
mtmap = MTMap(sys.argv[2])

nimap, ct = content.read_content(["NETHER", "QUARTZ"])
mtmap.fromMCMap(mcmap, nimap, ct)
mtmap.save()

print("Conversion finished!\n\n")
print("Run the \"get-mods.sh\" script in the converted world to automatically download\n")
print("the required mods.")
