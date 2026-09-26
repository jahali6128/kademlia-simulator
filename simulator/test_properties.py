from jproperties import Properties

p = Properties()

with open("/home/jahali6128/kademlia-simulator/simulator/config/kademlia_putget.cfg", "rb+") as f:
    p.load(f, "utf-8")
    # print(p["SIZE"])
    p["SIZE"] = "300"
    # f.seek(0)
    p["MINDELAY"] = "10"
    p["MAXDELAY"] = "10"

    for k,v in p.items():
        print(k, v)
    f.seek(0)
    f.truncate(0)
    p.store(f, "utf-8")
