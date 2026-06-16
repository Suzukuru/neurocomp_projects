import numpy as np

def derivative_f(S, M):
    x1,y1,x2,y2,x3,y3,vx1,vy1,vx2,vy2,vx3,vy3 = S
    m1, m2, m3 = M
    g = 1 # this for simulation, acl val is 6.6743 * 10**-11
    epsilon = 0.1

    dx12, dy12 = x2-x1, y2-y1
    dx13, dy13 = x3-x1, y3-y1
    dx23, dy23 = x3-x2, y3-y2 
    
    softened_r12 = ((dx12)**2 + (dy12)**2 + epsilon**2) ** (3/2)
    softened_r13 = ((dx13)**2 + (dy13)**2 + epsilon**2) ** (3/2)
    softened_r23 = ((dx23)**2 + (dy23)**2 + epsilon**2) ** (3/2)
    
    ax1 = g*m2*dx12/softened_r12 + g*m3*dx13/softened_r13            
    ay1 = g*m2*dy12/softened_r12 + g*m3*dy13/softened_r13           
            
    ax2 = g*m3*dx23/softened_r23 + g*m1*-dx12/softened_r12         
    ay2 = g*m3*dy23/softened_r23 + g*m1*-dy12/softened_r12         
    
    ax3 = g*m1*-dx13/softened_r13 + g*m2*-dx23/softened_r23           
    ay3 = g*m1*-dy13/softened_r13 + g*m2*-dy23/softened_r23          
    
    return np.array([vx1,vy1,vx2,vy2,vx3,vy3,ax1,ay1,ax2,ay2,ax3,ay3])

def rk4(S, M, h):
    k1 = derivative_f(S, M)
    k2 = derivative_f(S+(h/2*k1), M)
    k3 = derivative_f(S+h/2*k2, M)
    k4 = derivative_f(S+h*k3, M)
    return S + (h/6*(k1 + 2*k2 + 2*k3 + k4))

def conservation_momentum(S, M):
    x1,y1,x2,y2,x3,y3,vx1,vy1,vx2,vy2,vx3,vy3 = S

    p_x = M[0]*vx1 + M[1]*vx2 + M[2]*vx3 
    p_y = M[0]*vy1 + M[1]*vy2 + M[2]*vy3 
        
    return np.array([p_x, p_y])