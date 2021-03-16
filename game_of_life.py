import pygame
import random
import numpy as np

pygame.init()

def pause():
    while (True):
        x=input()
        if (x == "x"):
            break

#############################################################
#      Creates a random pixel array. returns numpy array
#############################################################
def init_random_screen_array(num_x_pixels,num_y_pixels,seed_num=0):
    
    random.seed(seed_num)
    
    A = np.ndarray((num_y_pixels,num_x_pixels),np.int8)
    
    for y in range(num_y_pixels):
    
        for x in range(num_x_pixels):
        
            bit = random.choice((0,1))
            A[y,x] = np.int8(bit)
    
    return A

##############################################################
#   returns count of adjacent neighbors to array element A[x,y]
##############################################################
def num_neighbors_adjxy(x ,y ,num_x_pixels ,num_y_pixels ,A):
    
    count = 0
    
    ################################################################
    # Test to see if x,y is inside a boundary frame 1 pixel in width
    ################################################################
    if((x>0)and(y>0)and(x<num_x_pixels-1)and(y<num_y_pixels-1)):
        within_bounds = True
    else:
        within_bounds = False
    if((num_x_pixels>=3)and(num_y_pixels>=3)):
        large_enough_array = True
    else:
        large_enough_array = False
        ###################################################
    if(within_bounds and large_enough_array):
        
        count = int(A[y-1,x-1]+A[y-1,x]+A[y-1,x+1]+A[y,x-1]+A[y,x+1]+A[y+1,x-1]+A[y+1,x]+A[y+1,x+1])
            
        return count
##################################################
#     If on the four corners of the frame.
##################################################
    ###################################
    #         Top-left corner
    ###################################
    elif((x==0)and(y==0)and(large_enough_array)):
        
        count = int(A[y+1,x]+A[y+1,x+1]+A[y,x+1])
        
        return count
    ###################################
    #        Top-right corner
    ###################################
    elif((x==num_x_pixels-1)and(y==0)and(large_enough_array)):
        
        count = int(A[y,x-1]+A[y+1,x-1]+A[y+1,x])
            
        return count
    ####################################
    #        Bottom-left corner
    ####################################
    elif((x==0)and(y==num_y_pixels-1)and(large_enough_array)):
        
        count = int(A[y-1,x]+A[y-1,x+1]+A[y,x+1])   
        
        return count
    #####################################
    #      Bottom-right corner
    #####################################
    elif((x==num_x_pixels-1)and(y==num_y_pixels-1)and(large_enough_array)):
        
        count = int(A[y-1,x-1]+A[y-1,x]+A[y,x-1])
            
        return count
######################################################
#   If along the four edges of the frame.
######################################################
             #--------Top--------#
    elif((x>0)and(x<num_x_pixels-1)and(y==0)and(large_enough_array)):
        
        count = int(A[y,x-1]+A[y+1,x-1]+A[y+1,x]+A[y+1,x+1]+A[y,x+1])
        
        return count
             #---------Bottom--------#
    elif((x>0)and(x<num_x_pixels-1)and(y==num_y_pixels-1)and(large_enough_array)):
        count = int(A[y,x-1]+A[y-1,x-1]+A[y-1,x]+A[y-1,x+1]+A[y,x+1])
            
        return count
        #---------------Left------------------#
    elif((y>0)and(y<num_y_pixels-1)and(x==0)and(large_enough_array)):
        
        count = int(A[y-1,x]+A[y-1,x+1]+A[y,x+1]+A[y+1,x+1]+A[y+1,x])
            
        return count
        #---------------Right------------------#
    elif((y>0)and(y<num_y_pixels-1)and(x==num_x_pixels-1)and(large_enough_array)):
        
        count = int(A[y-1,x]+A[y-1,x-1]+A[y,x-1]+A[y+1,x-1]+A[y+1,x])    
        
        return count
        
    else:
        print("Error:Array to small.")
        pygame.quit()
        
    return count
 
##########################################################
#     updates next generation array -> numpy array
##########################################################
def update_next_gen_array(num_x_pixels, num_y_pixels, A):
    
    
    B = np.ndarray((num_y_pixels,num_x_pixels),np.int8)
    #print(A)
    
    
    for y in range(num_y_pixels):
        for x in range(num_x_pixels):
        
            neighbors = num_neighbors_adjxy(x ,y ,num_x_pixels ,num_y_pixels ,A)
        
            if(int(A[y,x])==1):
                alive = True
            else:
                alive = False
        
            if( (alive) and ((neighbors==2)or(neighbors==3)) ):
                B[y,x] = np.int8(1)
            elif((neighbors==3)and (not alive)):
                B[y,x] = np.int8(1)
            else:
                B[y,x] = np.int8(0)
    
    #print(B)

    return B


def display_array(num_x_pixels,num_y_pixels,pixel_dim,A,num_calls):
    
    x_dim = int(num_x_pixels*pixel_dim)
    y_dim = int(num_y_pixels*pixel_dim)
    
    sf = pygame.display.set_mode((x_dim,y_dim))
    
    pxarray = pygame.PixelArray(sf)
    
    for y in range(num_y_pixels):
    
        for x in range(num_x_pixels):
            
            bit = int(A[y,x])
            
            #print(bit,end="")
            if (bit==1):
                
                pxarray[(x*pixel_dim):((x*pixel_dim)+pixel_dim),(y*pixel_dim):((y*pixel_dim)+pixel_dim)] = (255,0,0)
            else:
                
                pxarray[(x*pixel_dim):((x*pixel_dim)+pixel_dim),(y*pixel_dim):((y*pixel_dim)+pixel_dim)] = (255,255,255)
        #print()
    
    

    pygame.display.flip()
    
    if(((num_calls+1)>=490)and((num_calls+1)<=500)):
        filename = "gen_" + str(num_calls+1) + ".bmp"
        pygame.image.save(sf, filename)

#######################################################################################
#                              Main program
#######################################################################################
x_dim = 640
y_dim = 480

pixel_dim = int(input("Enter the width in actual pixels of each composite pixel. "))

seed_num = int(input("Enter an integer number to seed the random number generator. "))

generations = int(input("Input the number of generations you want. "))

#seed_num = 0
#pixel_dim = 10
#generations = 500

num_x_pixels = int(x_dim/pixel_dim)
num_y_pixels = int(y_dim/pixel_dim)

A = init_random_screen_array(num_x_pixels,num_y_pixels,seed_num)

for i in range(generations):
    #print("gen: "+str(i+1))
    display_array(num_x_pixels,num_y_pixels,pixel_dim,A,i)
    
    A = update_next_gen_array(num_x_pixels,num_y_pixels,A)

    #pygame.time.delay(1500)


pygame.quit()
