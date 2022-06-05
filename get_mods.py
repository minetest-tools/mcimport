#!/usr/bin/env python3

import io
import os
import shutil
import sys
import urllib.request
import zipfile

worldmods = os.path.join(os.getcwd(), "worldmods")
if not os.path.exists(worldmods):
    print("The provided path does not exist.")
    exit(1)

mods = (
    ("https://codeload.github.com/minetest-mods/mesecons/zip/master", "mesecons"),
    ("https://codeload.github.com/LNJ2/carpet/zip/master", "carpet"),
    ("https://codeload.github.com/minetest-mods/crops/zip/master", "crops"),
    ("https://codeload.github.com/minetest-mods/flowerpot/zip/master", "flowerpot"),
    ("https://codeload.github.com/minetest-mods/lapis/zip/master", "lapis"),
    ("https://codeload.github.com/minetest-mods/quartz/zip/master", "quartz"),
    ("https://codeload.github.com/minetest-mods/xdecor/zip/master", "xdecor"),
    ("https://codeload.github.com/oOChainLynxOo/hardenedclay/zip/master", "hardenedclay"),
    ("https://codeload.github.com/minetest-mods/nether/zip/master", "nether"),
    ("https://codeload.github.com/ShadowNinja/minetest_bedrock/zip/master", "minetest_bedrock"),
    ("https://gitlab.com/VanessaE/basic_materials/-/archive/master/basic_materials-master.zip", "basic_materials"),
    ("https://gitlab.com/VanessaE/biome_lib/-/archive/master/biome_lib-master.zip", "biome_lib"),
    ("https://gitlab.com/VanessaE/plantlife_modpack/-/archive/master/plantlife_modpack-master.zip", "plantlife_modpack"),
    ("https://gitlab.com/VanessaE/signs_lib/-/archive/master/signs_lib-master.zip", "signs_lib")
    )

# Some servers don't recognize the default Python-urllib user agent
headers = { 'User-Agent':'Mozilla' }

for url, mod in mods:
    print("Fetching:", mod);
    request = urllib.request.Request(url, None, headers)
    with urllib.request.urlopen(request) as response:
        with zipfile.ZipFile(io.BytesIO(response.read()), 'r') as mod_zip:
            mod_zip.extractall(worldmods)
            mod = os.path.normpath(worldmods+"/"+mod)
            os.rename(mod+"-master", mod)
minetest_bedrock = os.path.normpath(worldmods+"/"+"minetest_bedrock")
bedrock = os.path.normpath(worldmods+"/"+"bedrock")
os.rename(minetest_bedrock, bedrock)

# Remove unneeded/unwanted submods
prune = ( "dryplants", "along_shore", "molehills", "woodsoils", "bushes", "bushes_classic", "youngtrees", "3dmushrooms", "cavestuff", "poisonivy", "trunks" )
for ex in prune:
    ex = "plantlife_modpack/" + ex
    print("Pruning:", ex)
    ex = os.path.normpath(worldmods+"/"+ex)
    shutil.rmtree(ex)
