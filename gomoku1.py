#!/usr/bin/python

import random

import pygame, sys
from pygame.locals import *





MAX_X = 600
MAX_Y = 600

HORIZ = 20
VERT =  20


STEP_X = int ( MAX_X / HORIZ)
STEP_Y = int (MAX_Y / VERT)


def draw_go(x,y,type):
  if type == 0:
    pygame.draw.rect(DISPLAYSURF, BLACK, (1+x*STEP_X,1+y*STEP_Y,STEP_X-1, -1+STEP_Y))
  if type == 1:
    pygame.draw.line(DISPLAYSURF, GREEN, (1+x*STEP_X,1+y*STEP_Y), (-1+(x+1)*STEP_X, -1+(y+1)*STEP_Y),1)
    pygame.draw.line(DISPLAYSURF, GREEN, (-1+(x+1)*STEP_X,1+y*STEP_Y),  (x*STEP_X+1, -1+(y+1)*STEP_Y),1)
  if type == 2:
    pygame.draw.ellipse(DISPLAYSURF, RED, (x*STEP_X +2 ,y*STEP_Y +2 , STEP_X - 4, STEP_Y - 4), 1)	


a ={}
cX={}
cY={}
costW={}
costL={}

moves = []


rand = random.Random()

max_X = 20
max_Y = 20

def init(a):
	for i in range(max_X):
		for j in range(max_Y):
			a[i,j] = 0;

def print_p(a):
	for j in range(max_Y):
		str = "";		
		for i in range(max_X):
		
			if a[i,j] == 0 :	
				str+= "."
			elif a[i,j] == 1:
				str+="X"
			elif a[i,j] == 2:
				str+="O"
			else:
				str+="?"
		print (str)




def sequence(a,x,y,dir_x, dir_y, Len):  #return sequence wtih length = len
    Seq=[]
    for i in range (Len):
      if map(x+i*dir_x,y+i*dir_y) >= 0:
	Seq.append(a[x+i*dir_x,y+i*dir_y])
    if (len(Seq) == Len):
        return Seq
    return [] 


def in_sequence(x,y,x1,y1,dir_x, dir_y, Len):  #return True if x,y in sequence with length = len
    in_seq=False
    for i in range (Len):
      if (x==x1+i*dir_x) and (y==y1+i*dir_y):
	    in_seq = True;
    return in_seq


def check_win(a):
	for i in range(max_X):
		for j in range(max_Y):
			if   (i< (max_X - 4)) and (a[i,j] != 0) and  (a[i,j]==a[i+1,j]) and (a[i,j]== a [i+2,j]) and (a[i,j] == a [i+3,j]) and (a[i,j] == a [i+4,j]):
##				print ("(Y=const)i,j=", i+1,j+1)
				return a[i,j]
			elif (j < (max_Y - 4)) and (a[i,j] != 0) and (a[i,j] == a[i,j+1] == a[i,j+2] == a[i,j+3] == a [i,j+4]):
#				print ("(X=const)i,j=", i+1,j+1)
				return a[i,j]	
			elif ((i < (max_X - 4)) and (j < max_Y - 4)) and ((a[i,j] !=0) and (a[i,j] == a[i+1,j+1] == a[i+2,j+2] == a[i+3,j+3] == a[i+4,j+4])):
#				print ("(diagon1)i,j=", i+1,j+1)
				return a[i,j]
			elif ((i < (max_X - 4)) and (j <  (max_Y - 4) )) and (a[i+4,j] != 0) and (a[i+4,j] == a[i+3,j+1]== a[i+2, j+2] == a[i+1,j+3] == a[i,j+4]):
#				print ("(diagon2)i-4,j=", i-3,j+1)
				return a[i+4,j]
							
	return 0

def  map(x,y):
       if ((x <   0) or (x >= max_X) or (y < 0) or (y >= max_Y)):
	       return -9999;
       return a[x,y]

def cost_go(x1,y1,a, playG):
      antiplayG = anti_g(playG)	
      cost =0
      if (map(x1,y1) ==0):
     	     a[x1,y1]	= playG
      else:
	    return -9999
      for x in range (x1-6,x1+6):
       for y in range (y1 -6, y1+6):
         for i in range(-1,2):
   	  for j in range(-1,2):
	    if (i!=0) or (j!=0):
#5 sec probe
             if in_sequence(x1,y1,x,y,i,j,5):
                sec = sequence(a,x,y,i,j,5)
		if sec ==[playG,antiplayG,antiplayG,antiplayG,antiplayG]:
		    cost = max(460,cost)
		elif sec ==[playG,antiplayG,antiplayG,antiplayG,0]:
		    cost = max(440,cost)
		elif sec ==[0,antiplayG,antiplayG,antiplayG,playG]:
		    cost = max(440,cost)
	        elif sec==[0,antiplayG,antiplayG,playG,antiplayG,0]:
		    cost = max(cost,300)
		elif sec==[playG,antiplayG,antiplayG,antiplayG,0]:
		    cost = max(cost,300)
		elif sec==[0,antiplayG,antiplayG,antiplayG,playG]:
		    cost = max(cost,300)
		elif sec ==[playG,playG,playG,playG,playG]:
		    cost = 500
	        elif sec==[0,playG,playG,0,playG,0]:
		    cost = max(cost,300)
		elif sec==[0,playG,playG,playG,0]:
		    cost = max(cost,300)

		
#7 seq
	     if (cost < 450) and in_sequence(x1,y1,x,y,i,j,7):
             
		sec = sequence(a,x,y,i,j,7)


		if sec==[0,antiplayG,antiplayG,antiplayG,playG,antiplayG,0]:
		       cost=max(cost,430)
		elif sec==[playG,antiplayG,antiplayG,antiplayG,playG,antiplayG,0]:
		       cost=max(cost,430)
		elif sec==[0,antiplayG,antiplayG,antiplayG,playG,antiplayG,playG]:
		       cost=max(cost,430)
	        elif sec==[0,antiplayG,antiplayG,playG,antiplayG,antiplayG,0]:
		       cost=max(cost,430)
		elif sec==[0,antiplayG,playG,antiplayG,antiplayG,antiplayG,0]:
        	       cost=max(cost,430)
	        elif sec==[antiplayG,antiplayG,antiplayG,playG,antiplayG,antiplayG,0]:
		       cost=max(cost,410)
		elif sec==[0,playG,playG,playG,0,playG,0]:
		       cost=max(cost,400)
	        elif sec==[0,playG,playG,0,playG,playG,0]:
		       cost=max(cost,400)
		elif sec==[0,playG,0,playG,playG,playG,0]:
        	       cost=max(cost,400)
	#	elif sec==[0,playG,playG,playG,playG,playG,0]:
         #	       print "0 p 0 p p p 0", sec
        #	       cost=max(cost,500)
	#	elif sec==[playG,playG,playG,playG,playG,playG,0]:
         #	       print "0 p 0 p p p 0", sec
        #	       cost=max(cost,500)






#6 seq


    	     if (cost < 455) and in_sequence(x1,y1,x,y,i,j,6):
		sec = sequence(a,x,y,i,j,6)
		if sec ==[playG,antiplayG,antiplayG,antiplayG,antiplayG,playG]:
		    cost = max(cost,450)
	        elif sec==[playG,antiplayG,antiplayG,antiplayG,antiplayG,0]:
		    cost=max(cost,400)
	        elif sec==[0,antiplayG,antiplayG,antiplayG,antiplayG,playG]:
		    cost=max(cost,400)
	        elif sec==[playG,antiplayG,antiplayG,antiplayG,antiplayG,playG]:
		    cost=max(cost,430)
		elif sec==[0,antiplayG,playG,antiplayG,antiplayG,0]:
		    cost = max(cost,400)
		elif sec==[0,antiplayG,antiplayG,playG,antiplayG,0]:
		    cost = max(cost,400)
	        elif sec==[0,playG,playG,playG,playG,0]:
		   cost=max(cost,455)
		elif sec==[0,playG,0,playG,playG,0]:
		    cost = max(cost,200)
		elif sec==[0,playG,playG,0,playG,0]:
		    cost = max(cost,200)



#4 seq

    	     if (cost < 100) and in_sequence(x1,y1,x,y,i,j,4):
		sec = sequence(a,x,y,i,j,4)
		if sec==[playG,antiplayG,antiplayG,antiplayG]:
		    cost = max(cost,100)
		elif sec==[playG,antiplayG,antiplayG,antiplayG]:
		    cost = max(cost,100)
		elif x>0 and y > 0 and sec==[antiplayG,playG,antiplayG,antiplayG]:
		    cost = max(cost,100)
		elif  x> 0 and y> 0  and  sec==[antiplayG,antiplayG,playG,antiplayG]:
		    cost = max(cost,100)
		elif sec==[playG,antiplayG,antiplayG,0]:
		    cost = max(cost,30)
		elif sec==[0,antiplayG,playG,antiplayG]:
		    cost = max(cost,10)
		elif x>0 and sec==[antiplayG,antiplayG,playG,0]:
		    cost = max(cost,10)
		elif sec==[antiplayG,playG,playG,playG]:
		    cost = max(cost,10)



#3 seq

    	     if (cost < 10) and in_sequence(x1,y1,x,y,i,j,3):
		sec = sequence(a,x,y,i,j,3)
		if sec==[playG,antiplayG,0]:
		    cost = max(cost,5)
		elif sec==[0,playG,antiplayG]:
		    cost = max(cost,3)
		elif sec==[playG,antiplayG,0]:
		    cost = max(cost,3)
		elif sec==[antiplayG,playG,0]:
		    cost = max(cost,2)
		elif sec==[antiplayG,playG,antiplayG]:
		    cost = max(cost,3)
		if sec==[0,playG,0]:
		    cost = max(cost,5)
		elif sec==[0,0,playG]:
		    cost = max(cost,3)
		elif sec==[0,playG,0]:
		    cost = max(cost,3)
		elif sec==[playG,0,0]:
		    cost = max(cost,2)
		elif sec==[playG,0,playG]:
		    cost = max(cost,3)

        


      a[x1,y1] = 0
      return cost    
    	    




def rand_go(a,g):
	X = rand.randint(0,max_X-1)
	Y = rand.randint(0,max_Y-1)
	if a[X,Y] == 0:
		a[X,Y] =g
		return True;
	else:
		return False #unable make go

def max_i(ax):
	max_k = 0
	for k in range (1, len(ax) ):
	 if ax[k] > ax[max_k]:
	    max_k = k

	return max_k

def min_i(ax):
	min_k = 0
	for k in range (1, len(ax) ):
	 if ax[k] < ax[min_k]:
	    min_k = k

	return min_k


def anti_g(g):
	if g == 2:
           return 1
	return 2

def beginner_go(a,g):
	cX = {}
	cY = {}
	costW = {}
	costL = {}

	if g == 2:
           anti_g=1
	else:
	   anti_g=2;

	for k in  range(len(moves)*24+50) :
		(cX[k], cY[k] ) =  moves[k %  len(moves)]
		iterator =0
                while (map(cX[k],cY[k]) != 0 and (iterator < 50)):
 		   cX[k] += rand.randint(-2,3)
		   cY[k] += rand.randint(-2,3)
		   iterator += 1    
		costW[k] = cost_go(cX[k] ,cY[k], a, g)


	best_strike = max_i(costW)
	a[cX[best_strike], cY[best_strike]] = g;
	draw_go(cX[best_strike], cY[best_strike], g);
	moves.append((cX[best_strike], cY[best_strike]));		
#	cX=cY=costW=costL=[]
	return (cX[best_strike], cY[best_strike], costW[best_strike])

def impedance_go(a,g):
	cX = {}
	cY = {}
	costNext = {}

	if g == 2:
           anti_g=1
	else:
	   anti_g=2

	for k in  range(len(moves)*24+50):
		(cX[k], cY[k],costNext[k] ) =   moves[k %  len(moves)]
		iterator =0
                while (map(cX[k],cY[k]) != 0 and (iterator < 50)):
 		   cX[k] += rand.randint(-2,3)
		   cY[k] += rand.randint(-2,3)
		   iterator += 1    
		beginner_go(a,anti_g)
		beginner_go(a,g)
		costW[k] = cost_go(cX[k] ,cY[k], a, g)
		
	best_strike = max_i(costW)
	a[cX[best_strike], cY[best_strike]] = g;
	draw_go(cX[best_strike], cY[best_strike], g);
	moves.append((cX[best_strike], cY[best_strike]));		
	return (cX[best_strike], cY[best_strike], costW[best_strike])
    
	




pygame.init()


# set up the window
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y), 0, 32)
pygame.display.set_caption('Drawing')
# set up the colors

BLACK = (0,0,0)
WHITE = (255, 255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# draw on the surface object
DISPLAYSURF.fill(BLACK)

for i in range (STEP_X, MAX_X , STEP_X):
   pygame.draw.line(DISPLAYSURF, BLUE, (i, 0), (i, MAX_Y), 1)


for j in range (STEP_Y, MAX_Y , STEP_Y):
     pygame.draw.line(DISPLAYSURF, BLUE, (0, j), (MAX_X, j), 1)

 
init(a)

  # run the game loop
while True:
   for event in pygame.event.get():
      if event.type == QUIT:
              pygame.quit()
              sys.exit()
      elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                x = int (mousex / STEP_X)
                y = int (mousey /STEP_Y)
                if a[x,y] == 0 and check_win(a) == 0:
                        draw_go (x,y, 1)
			pygame.display.update()
                        a[x,y] = 1
                        moves.append([x,y])		
			status_game = check_win(a)
                        if (status_game  ==  1):
                                print ("win X")
			else:
                                beginner_go(a,2)
				status_game = check_win(a)
                    		if status_game == 2:
                            	    print("win O");



					
   pygame.display.update()

#for i in range(1500):
#  while(not rand_go(a,1)):
#     mmm=2

#  beginner_go(a,1);	
#  if (check_win(a) ==  1):
#        print ("win X")
#        break

#  while not rand_go(a,2):   
#    mm = 3
#  beginner_go(a,2);	
#  if (check_win(a) == 2 ):
#        print ("win O")
#        break
 
 # print_p(a)
#  print ("==================move ", i)

#print("************last position******************************", i)
#print_p(a)
