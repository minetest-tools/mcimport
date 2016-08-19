import logging
from itemstack import *
#If you wish to add more entities, then...
# To see pre and post-conversion entity, raise the log level to DEBUG and look
# at the log output on stderr in category 'blocks' (search for 'EntityInfo' to
# locate them)

logger = logging.getLogger('entities')

def convert_frame(e):
    from pprint import pformat
    logger.debug(pformat(e))
    # must read attribs and translate to entities we know from map_content.txt
    content = e.get("Item")
    x = e.get("TileX")
    y = e.get("TileY")
    z = e.get("TileZ")
    item = e.get("Item")
    if item:
        logger.debug(item.get("id"))
        return "xdecor:itemframe", None, (None, None)
    else:
        logger.warning("empty item frame")
        return "xdecor:itemframe", None, (None, None)

e_convert = {"itemframe": convert_frame}
