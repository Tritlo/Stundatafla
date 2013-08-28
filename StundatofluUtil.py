def getLocations(listrep, checkFunc):
    t = listrep
    locs = []
    for i in range(len(t)):
        for j in range(len(t[0])):
            locs.append((i,j))
    places = filter(lambda (i,j): checkFunc(listrep[i][j]), locs)
    return places
