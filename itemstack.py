class MCItemStack:
    def __init__(self):
        pass

class MTItemStack:
    def __init__(self):
        pass

    def fromMCItemStack(self, mcstack):
        pass

    def empty(self):
        return True

    def serialize(self, os):
        pass

def serialize_inv_list(os, inv_list):
    os.write(bytes("Width "+str(inv_list[0])+"\n", "utf-8"))
    for item in inv_list[1]:
        if item.empty():
            os.write(bytes("Empty", "utf-8"))
        else:
            os.write(bytes("Item ", "uft-8"))
            item.serialize(os)
        os.write(bytes("\n", "utf-8"))
    os.write(bytes("EndInventoryList\n", "utf-8"))

def serialize_inv(os, inv):
    for name, inv_list in inv.items():
        os.write(bytes("List "+name+" "+str(len(inv_list[1]))+"\n", "utf-8"))
        serialize_inv_list(os, inv_list)
    os.write(bytes("EndInventory\n", "utf-8"))

