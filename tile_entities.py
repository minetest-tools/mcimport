from itemstack import *

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
        line = te.get("Text"+str(i), "").strip()
        if line != "":
            t += line
            t += " "
    t = t.strip()
    fields = {"infotext": '"'+t+'"',
              "text": t,
              "formspec": "field[text;;${text}]"}
    return None, None, (fields, {})

te_convert = {"chest": convert_chest,
              "sign": convert_sign,
              "furnace": convert_furnace}
