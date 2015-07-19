# mcimport
This mod provides a layer to make use of minecraft texture packs.
It also provides basic conversions for approximately 1000 nodes which will fit the names of the .pngs found in the current minetest (1.81) and associated texture packs. 

I've also provided a map_content.txt file which will enable worlds to be imported by mcimport - [url]https://forum.minetest.net/viewtopic.php?f=5&t=11146[/url]. You'll need to replace the one in mcimport with this file to fully enable mcblocks during an import.

To use the mod, download a texture pack and extract the assets folder into the mod folder.
On the first run, the mod will automatically move the files from the relevant directories into the texture folder. 

NB not all texture packs are complete, so if you have missing textures, try another pack. Any existing files will be overwritten, but files which don't have a replacement won't be deleted. Please follow the licenses, so although you could also start by extracting the assets folder directly from minecraft I'm not sure that using these textures in minetest would be licensed) 


Caveats:
Currently there is no functionality for the blocks (eg furnaces don't burn, chests don't work, nor do crafting tables, crops don't grow, etc)
I haven't tested for texture packs from previous versions.
The names of nodes within the mod aren't exactly the same as the newer style of minecraft, there were some inconsistencies in my sources and it took me a while to realise what was correct. Anyone who wishes too is welcome to rename them all and push to git (but you'll have to do it in one go, I'm not going to import them piecemeal).

-- TODO:
-- Correctly display Fences, Doors, Gates, Beds, Rails, animated blocks
-- Enable Special Block Functions (doors, chests, enchanting table, crafting table/workbench, furnace, anvil, cake, signs)
-- correct plants: Double-height plants, tallgrass, waterlillies, mushrooms, growing Crops

--More Difficult:
-- utilise 3D models: /assets/minecraft/models, and 3D textures /assets/minecraft/textures/entity
-- Functioning Redstone
-- Mobs

License: all code is licensed under the CC0
