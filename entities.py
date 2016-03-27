from itemstack import *
#If you wish to add more entities, then...
# To print out pre and post-conversion entity information uncomment line 237 (ish) in blocks.py (search for 'EntityInfo' to locate it)

def convert_frame(e):
    from pprint import pprint
    pprint(e)
    # must read attribs and translate to entities we know from map_content.txt
    content = e.get("Item")
    x = e.get("TileX")
    y = e.get("TileY")
    z = e.get("TileZ")
    item = e.get("Item")
    if item:
        content = item.get("id")
        print(content)
        return "xdecor:itemframe", None, (None, None)
    else:
        print("empty item frame")
        return "xdecor:itemframe", None, (None, None)

e_convert = {"itemframe": convert_frame}
