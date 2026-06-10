import pygame
import numpy as np
import transformations as rot

def deritivative_f(S, M):
    x1,y1,x2,y2,x3,y3,vx1,vy1,vx2,vy2,vx3,vy3 = S
    m1, m2, m3 = M
    g = 1 # this for simulation, acl val is 6.6743 * 10**-11
    epsilon = 0.1
    displacement = [x2-x1, y2-y1, # r12 
                    x3-x1, y3-y1, # r13 
                    x3-x2, y3-y2] # r23 
    
    softened_denominator = []
    
    for i in range(0, 6, 2):
        softened_denominator.append(((displacement[i])**2 + (displacement[i+1])**2 + epsilon**2) ** (3/2))
    
    ax1 = g*m2*displacement[0]/softened_denominator[0] + g*m3*displacement[2]/softened_denominator[1]
            #x2-x1                                         #x3-x1            
    ay1 = g*m2*displacement[1]/softened_denominator[0] + g*m3*displacement[3]/softened_denominator[1]
            #y2-y1                                         #y3-y1            
            
    ax2 = g*m3*displacement[4]/softened_denominator[2] + g*m1*-displacement[0]/softened_denominator[0]
            #x3-x2                                         #x1-x2            
    ay2 = g*m3*displacement[5]/softened_denominator[2] + g*m1*-displacement[1]/softened_denominator[0]
            #y3-y2                                         #y1-y2            
    
    ax3 = g*m1*-displacement[2]/softened_denominator[1] + g*m2*-displacement[4]/softened_denominator[2]
            #x1-x3                                         #x2-x3            
    ay3 = g*m1*-displacement[3]/softened_denominator[1] + g*m2*-displacement[5]/softened_denominator[2]
            #y1-y3                                         #y2-y3            
    
    return np.array([vx1,vy1,vx2,vy2,vx3,vy3,ax1,ay1,ax2,ay2,ax3,ay3])

def rk4(S, M, h):
    k1 = deritivative_f(S, M)
    k2 = deritivative_f(S+(h/2*k1), M)
    k3 = deritivative_f(S+h/2*k2, M)
    k4 = deritivative_f(S+h*k3, M)
    return S + (h/6*(k1 + 2*k2 + 2*k3 + k4))

def conservation_momentum(S, M):
    x1,y1,x2,y2,x3,y3,vx1,vy1,vx2,vy2,vx3,vy3 = S
    
    p_x = M[0]*vx1 + M[1]*vx2 + M[2]*vx3 
    p_y = M[0]*vy1 + M[1]*vy2 + M[2]*vy3 
        
    return np.array([p_x, p_y])

def get_position_matrix(S):
        return np.array([[S[0], S[1], 0],
                        [S[2], S[3], 0],
                        [S[4], S[5], 0],])
        

def proj_2D(v, fov=400):
        x, y, z = v
        z += 2 # offset, prevents division by zero
        
        return np.array([fov * x/z, fov * y/z])

rng = np.random.default_rng()

# State Vector and Mass
S = np.array([0.97000436, -0.24308753, -0.97000436, 0.24308753, 0, 0, 
             0.466203685, 0.43236573, 0.466203685, 0.43236573, -0.93240737, -0.86473146])

M = np.array([1.0, 1.0, 1.0])
h = 0.0001
#S = rng.uniform(low=1, high=5, size=12)
#M = rng.uniform(low=1, high=2, size=3)

# Camera Properties
# Pygame
pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True) 
screen = pygame.display.set_mode((1000,1000))
cx, cy = (500, 500)

while True:
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                        pygame.quit()
                        exit()  
        
        screen.fill((20, 20, 20))
        
        screen_projection = [proj_2D(v) for v in get_position_matrix(S)]
        print(screen_projection)
        
        for i in screen_projection:
                pygame.draw.circle(screen, (255, 0, 0), ((i[0])+cx, (i[1])+cy), 10)
        
        S = rk4(S, M, h)

        pygame.display.flip()