import copy as c

d= {((1,0),(0,0)):[False,True],((1,0),(1,0)):[False,False]}
dc =c.deepcopy(d)
d[((1,0),(1,0))][0] = True
print(d[((1,0),(1,0))])
print(dc[((1,0),(1,0))])
# print(list(map(lambda x : x[0] or x[1],d.values())))
# print(all([]))
if ((1,0),(0,0))in d:
    print('ss')