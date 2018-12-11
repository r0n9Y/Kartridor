from constants import Winfo

# parameter 
# returns the area info with width and height
def calculateWH(area):
    assert(len(area) == 4)
    area.append(area[2] - area[0])
    area.append(area[3] - area[1])
    assert(area[4] > 0 and area[5] > 0)
    return area

def WithinWinowFrame(x, y):
    # debug output
    # print("({}, {}) : ({}, {}, {}, {})".format(x, y, Winfo.x0, Winfo.y0, Winfo.x1, Winfo.y1))
    if x > Winfo.x0 and x < Winfo.x1 and y > Winfo.y0 and y < Winfo.y1:
        return True
    return False