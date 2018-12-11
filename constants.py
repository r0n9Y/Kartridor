class Winfo:
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    w = 0
    h = 0

def PrintWinfo():
    print("window frame info: topx:{}, topy:{}, botx:{}, boty{}, width: {}, height:{}".format(Winfo.x0, Winfo.y0, Winfo.x1, Winfo.y1, Winfo.w, Winfo.h))