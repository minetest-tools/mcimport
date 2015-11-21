from itemstack import *
#If you wish to add more entities, then...
# To print out pre and post-conversion entity information uncomment line 237 (ish) in blocks.py (search for 'EntityInfo' to locate it)

def convert_chest(te):
    formspec = "size[8,9]"+\
               "list[current_name;main;0,0;8,4;]"+\
               "list[current_player;main;0,5;8,4;]"
    fields = {"infotext": "Chest",
              "formspec": formspec}
    inventory = {"main": (0, [MTItemStack()]*32)}
    return None, None, (fields, inventory)

def escape(s):
    s2 = ""
    for c in s:
        if c in ["'", '"', "\\"]:
            s2 += "\\"
            s2 += c
        elif c == "\n":
            s2 += "\\n"
        elif c == "\t":
            s2 += "\\t"
        else:
            s2 += c
    return s2

def convert_furnace(te):
    src_time = 0
    src_totaltime = 0
    fuel_time = 0
    fuel_totaltime = 0
    infotext = "Furnace out of fuel"
    formspec = "size[8,9]"+\
               "image[2,2;1,1;default_furnace_fire_bg.png]"+\
               "list[current_name;fuel;2,3;1,1;]"+\
               "list[current_name;src;2,1;1,1;]"+\
               "list[current_name;dst;5,1;2,2;]"+\
               "list[current_player;main;0,5;8,4;]"
    fields = {"infotext": infotext,
              "formspec": formspec,
              "src_totaltime": src_totaltime,
              "src_time": src_time,
              "fuel_totaltime": fuel_totaltime,
              "fuel_time": fuel_time}
    inventory = {"fuel": (0, [MTItemStack()]),
                 "src": (0, [MTItemStack()]),
                 "dst": (0, [MTItemStack()]*4)}
    return None, None, (fields, inventory)

def convert_sign(te):
    t = ""
    for i in range(1, 5):
        line = te.get("Text"+str(i), "").strip('"')
        if line != "":
            t += line
            t += "\n"
    t = t.strip()
    fields = {"infotext": t,
              "text": t,
              "__signslib_new_format": "1",
              "formspec": "size[6,4]textarea[0,-0.3;6.5,3;text;;${text}]button_exit[2,3.4;2,1;ok;Write]background[-0.5,-0.5;7,5;bg_signs_lib.jpg]"}
    return None, None, (fields, {})

def convert_nodeblock(te):
    pitch = te.get("note")
    return None, int(pitch) % 12, None

te_convert = {"chest": convert_chest,
              "sign": convert_sign,
              "furnace": convert_furnace,
              "music": convert_nodeblock}
