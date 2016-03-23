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

def convert_frame(te):


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
        if '{"text":"' in line:
            parts = line.split('"')
            line = parts[3]
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

def convert_pot(te):
    c = str(te.get("Item"))+":"+str(te.get("Data"))
    # translation table for flowers
    # highly approximate, based on color only
    t = {
        ":0" : 0, # air
        "minecraft:brown_mushroom:0" : 1,
        "minecraft:red_mushroom:0" : 2,
        "minecraft:cactus:0" : 3,
        "minecraft:deadbush:0" : 4,
        "minecraft:red_flower:0" : 5,
        "minecraft:red_flower:1" : 6,
        "minecraft:red_flower:2" : 7,
        "minecraft:red_flower:3" : 8,
        "minecraft:red_flower:4" : 9,
        "minecraft:red_flower:5" : 10,
        "minecraft:red_flower:6" : 11,
        "minecraft:red_flower:7" : 12,
        "minecraft:red_flower:8" : 13,
        "minecraft:sapling:0" : 14,
        "minecraft:sapling:1" : 15,
        "minecraft:sapling:2" : 16,
        "minecraft:sapling:3" : 17,
        "minecraft:sapling:4" : 18,
        "minecraft:sapling:5" : 19,
        "minecraft:tallgrass:2" : 20,
        "minecraft:yellow_flower:0" : 21
    }
    try:
        fields = { "_plant": t[c] }
        return None, None, (fields, {})
    except:
        print('Unknown flower pot type: '+c)
        return None, None, None

def convert_cmdblock(te):
    c = te.get("Command")
    c = c.replace("/tp ", "teleport ")
    c = c.replace("/tell ", "tell ")
    c = c.replace(" @p ", " @nearest ")
    c = c.replace(" @r ", " @random ")
    fields = {"infotext" : "Command block, commands: \""+c+"\"",
              "commands": c,
              "owner": "no owner",
              "formspec": "invsize[9,5;]textarea[0.5,0.5;8.5,4;commands;Commands;"+c+"]label[1,3.8;@nearest, @farthest, and @random are replaced by the respective player names]button_exit[3.3,4.5;2,1;submit;Submit]"
    }
    return None, None, (fields, {})

te_convert = {"chest": convert_chest,
              "ItemFrame": convert_frame,
              "sign": convert_sign,
              "furnace": convert_furnace,
              "music": convert_nodeblock,
              "flowerpot": convert_pot,
              "control": convert_cmdblock}
