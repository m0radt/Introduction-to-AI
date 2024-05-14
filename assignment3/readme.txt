install python 3.10.12


you should write the input in input.txt file in this following format:
 

#X <Maximum x coordinate>               
#Y <Maximum y coordinate>  

Package at Vertex (x,y) :          
#V <x> <y> <p>        ; Vertex (x,y) probability of package given low demand season p.

to add a blocked edge write this line :  
#B <x1> <y1> <x2> <y2>                   ; Edge from (x1,y1) to (x2,y2) is always blocked.

to add a fragile edge write this line :  
#F <x1> <y1> <x2> <y2>                   ; Edge from (x1,y1) to (x2,y2) is fragile, with p = 1-qi .
 
to add Global leakage probability :
#L <p>        ; Global leakage probability p.

to add distribution for season:
#S <l-p> <m-p> <h-p> ; Prior distribution over season: l-p for low, m-p for medium, h-p for high.
*******************************************************************************************

run the code type your evidence according to this instructions:

Insert evidence separated by | for each variable followed by its boolean value 
(i.e V(1, 0)=F|E((1, 0), (1, 1))=T|Season=medium for vertex (1, 0) NOT containing packages,
  edge between (1, 0) and (1, 1) is blocked and season is medium )

Insert Enter, and Type your query.

*******************************************************************************************
Explanation of the method for constructing the BN:
there is one node called "Season" in BN.

for every vertex (x, y)in the grid we built a node called "V(x, y)" in the BN:
if contain package with probability the node that represent this vertex have one parent the "Season".
else the node that represent this vertex have no parent with probability 0.

for every edge between  (x1, y1) and (x2, y2) in the grid we built a node called "E((x1, y1), (x2, x2))" in the BN:
if it is fragile with probability the node that represent this edge have two parent the "V(x1, y)1" "V(x2, y2)".
if it is blockedthe node that represent this edge have no parent with probability 1.
else the node that represent this edge have no parent with probability 0.
*******************************************************************************************
the algorithm i used is simple enumerarion
