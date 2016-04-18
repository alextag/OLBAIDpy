class Anode:
    def __init__(self, x, y, can_pass):
        self.x = x
        self.y = y
        self.g_score = 0.0
        self.f_score = 0.0
        self.can_pass = can_pass
        self.in_o = False
        self.in_c = False
        return

    def __gt__(self, node):
        return self.f_score>node.f_score

    def __lt__(self, node):
        return self.f_score<node.f_score

    def __eq__(self,node):
        return self.f_score==node.f_score

def heuristic( start, dest):
    return (start.x - dest.x)**2 + (start.y - dest.y)**2


def Astar( start, dest, world):
    width = len(world)
    height = len(world[0])

    if start[0]<0 or start[1]<0 or start[0]>=width or start[1]>=height:
        return False
    if dest[0]<0 or dest[1]<0 or dest[0]>=width or dest[1]>=height:
        return False
    
    aworld = []
    for x in range(width):
        aworld.append([])
        for y in range(height):
            aworld[x].append(Anode(x,y,world[x][y]))

    cset = []
    oset = [aworld[start[0]][start[1]]]
    aworld[start[0]][start[1]].in_o = True
    aworld[start[0]][start[1]].f_score = 1.0*heuristic(aworld[start[0]][start[1]],aworld[dest[0]][dest[1]])

    while len(oset)>0:
        oset.sort(reverse=True)
        current = oset[-1]
        if current == aworld[dest[0]][dest[1]]:
            return True

        temp = oset.pop()
        temp.in_o = False
        temp.in_c = True
        cset.append(temp)
        for i in [(0,1),(1,0),(-1,0),(0,-1)]:
            if current.x+i[0]<0 or current.y+i[1]<0 or current.x+i[0]>=width or current.y+i[1]>=height:
                continue
            if not aworld[current.x+i[0]][current.y+i[1]].can_pass:
                continue
            if aworld[current.x+i[0]][current.y+i[1]].in_c:
                continue

            tempgscore = current.g_score + 2

            if ((not aworld[current.x+i[0]][current.y+i[1]].in_o) or (tempgscore < aworld[current.x+i[0]][current.y+i[1]].g_score)):
                aworld[current.x+i[0]][current.y+i[1]].g_score = tempgscore
                aworld[current.x+i[0]][current.y+i[1]].f_score = tempgscore + 1.0*heuristic(aworld[current.x+i[0]][current.y+i[1]],aworld[dest[0]][dest[1]])
                if not aworld[current.x+i[0]][current.y+i[1]].in_o:
                    aworld[current.x+i[0]][current.y+i[1]].in_o = True
                    oset.append(aworld[current.x+i[0]][current.y+i[1]])
    return False


if __name__=='__main__':
    i=0
    world=[]
    while(i<11):
            j=0
            tempidi=[]
            while(j<11):
                tempidi.append(True)
                j=j+1
            world.append(tempidi)
            i=i+1
    print Astar((0,5),(10,7),world)
    print Astar((10,0),(1,0),world)


