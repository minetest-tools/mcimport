def convert_chest(te):
    meta = """{fields={infotext="Chest",\
        formspec="size[8,9]\
                  list[current_name;main;0,0;8,4;]\
                  list[current_player;main;0,5;8,4;]"},\
        inventory={main=\
            {"","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""}}}"""
    return None, None, meta

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
    meta = '''{fields={src_totaltime="'''+str(src_totaltime)+'''",\
    src_time="'''+str(src_time)+'''",fuel_time="'''+str(fuel_time)+'''",\
    fuel_totaltime="'''+str(fuel_totaltime)'''",\
    formspec="size[8,9]image[2,2;1,1;default_furnace_fire_bg.png]\
              list[current_name;fuel;2,3;1,1;]\
              list[current_name;src;2,1;1,1;]\
              list[current_name;dst;5,1;2,2;]\
              list[current_player;main;0,5;8,4;]",\
    infotext="'''+infotext+'''"},\
    inventory={fuel={""},dst={"","","",""},src={""}}}'''
    return None, None, meta

def convert_sign(te):
    t = ""
    for i in range(1, 5):
        line = te.get("Text"+str(i), "").strip()
        if line != "":
            t += line
            t += " "
    t = t.strip()
    text = escape(t)
    meta = '''{fields={infotext="\\"'''+text+'''\\"",text="'''+text+'''",\
        formspec="field[text;;${text}]"},\
        inventory={}}'''
    return None, None, meta

te_convert = {"chest": convert_chest,
              "sign": convert_sign,
              "furnace": convert_furnace}
