install python 3.10.12


you should write the input in input.txt file in this following format:
 

#X <Maximum x coordinate>               
#Y <Maximum y coordinate>  

to add a Package write this line :          
#P <x1> <y1> <t> D <x2> <y2> <dl>        ; Package at (x1,y1) from time t, deliver to (x2,y2) on or before time dl

to add a blocked edge write this line :  
#B <x1> <y1> <x2> <y2>                   ; Edge from (x1,y1) to (x2,y2) is always blocked

to add a fragile edge write this line :  
#F <x1> <y1> <x2> <y2>                   ; Edge from (x1,y1) to (x2,y2) is fragile (can only be traversed once)
 


************************************************************************************************************************************
For Adversarial with Alpha-Beta Pruning write this line:
#Adversarial <x1> <y1> <x2> <y2>         ; first agent starts at (x1,y1) and the second starts at (x2,y2)

For Semi-Cooperative write this line:
#Semi-Cooperative <x1> <y1> <x2> <y2>    ; first agent starts at (x1,y1) and the second starts at (x2,y2)

for Fully-Cooperative write this line:
#Fully-Cooperative <x1> <y1> <x2> <y2>   ; first agent starts at (x1,y1) and the second starts at (x2,y2)

