import pygame
import numpy as np
import transformations as rot
import controls as handle

def deritivative_f(S, M):
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
        return np.array([[S[0], S[1], 3],
                        [S[2], S[3], 3],
                        [S[4], S[5], 3],])
        

def proj_2D(v, fov=400):
        x, y, z = v
        z += +2 # offset, prevents division by zero
        
        return np.array([fov * x/z, fov * y/z])

# Grid maker, size x size
def make_grid(size, step):
    pa = []
    pb = []
    y_floor = 0
     
    for i in range(-size, size+1, step):
        pa.append(np.array([-size, y_floor, i]))
        pb.append(np.array([size, y_floor, i]))
        pa.append(np.array([i, y_floor, -size]))
        pb.append(np.array([i, y_floor, size]))
    
    return (pa, pb)

def draw_grids(pa, pb):
    for a, b in zip(pa, pb):
        
        a = rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch) @ (a - camera_position)
        b = rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch) @ (b - camera_position)

        if (a[2] < -2 or b[2] < -2): continue ## Prevents Z Axis  Near Clipping Visual Bugs
        line_X  = proj_2D(a) + [cx, cy]
        line_Z  = proj_2D(b) + [cx, cy]

        pygame.draw.line(screen, (100, 100, 100),
                         line_X,
                         line_Z)


def camera_screen_projection(position, camera_position):
        camera_projection = [rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch) @ (v - camera_position) for v in position]
        screen_projection = [proj_2D(v) for v in camera_projection]
        
        return camera_projection, screen_projection

# Grids: Floor
pa, pb = make_grid(6, 1)

# Body Properties
S = np.array([0.97000436, -0.24308753, -0.97000436, 0.24308753, 0, 0,              
              0.466203685, 0.43236573, 0.466203685, 0.43236573, -0.93240737, -0.86473146]) 
M = np.array([1.0, 1.0, 1.0])
h = 0.01

body_trail = []
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Camera Properties
sensitivity = 0.001
movespeed = 0.1
camera_yaw = 0
camera_pitch = 0
camera_position = np.array([0, 0, 0], dtype=float)
camera_sensitivity = 1.0

# Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000,1000))
pygame.event.set_grab(True) 
pygame.mouse.set_visible(False)
cx, cy = (500, 500)
time = 1

while True:
    for e in pygame.event.get():
            if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()  
                    
    # Pygame Properties
    dt = clock.tick(120)/1000
    screen.fill((20, 20, 20))
    keys = pygame.key.get_pressed()
    rel_x, rel_y = pygame.mouse.get_rel()
    
    # Camera Definition
    camera_yaw += rel_x * sensitivity
    camera_pitch += rel_y * sensitivity
    camera_pitch = np.clip(camera_pitch, -np.pi/2, np.pi/2)
    
    # Movement Definition
    front = rot.Y_3D(-camera_yaw) @ rot.X_3D(-camera_pitch) @ np.array([0.0, 0.0, 1.0])
    right = rot.Y_3D(-camera_yaw) @ np.array([1.0, 0.0, 0.0])
    up = np.cross(front, right)
    

    camera_position = handle.user_CameraMovement(keys, front, right, up, movespeed, camera_position)
    S, M, body_trail = handle.user_ObjectState(keys, S, M, body_trail)
    
    
    body_positions = get_position_matrix(S)
    body_trail.append(body_positions)
    
    
    if len(body_trail) > 0:
        for trail in body_trail:
            camera_projection_trail, screen_projection_trail = camera_screen_projection(trail, camera_position)
            
            for i in range(3): 
                if camera_projection_trail[i][2] > 0.1: 
                    body_x = screen_projection_trail[i][0]
                    body_y = screen_projection_trail[i][1]
                    pygame.draw.circle(screen, colors[i], (body_x+cx, body_y+cy), 1) 
                    
    if len(body_trail) > 100:
            body_trail.pop(0)
    
    camera_projection, screen_projection = camera_screen_projection(body_positions, camera_position)
    
    for i in range(3): 
        if camera_projection[i][2] > 0.1: 
                body_x = screen_projection[i][0]
                body_y = screen_projection[i][1]
                radius_z = np.log(np.linalg.norm(camera_projection[i]))
                radius = 10/radius_z
                radius = min(radius, 100)
                #print(f"{i}: {camera_projection[i]}\n{i}: {radius_z}\nbaseline size: {M[i]*10}\nradius: {radius}")
                pygame.draw.circle(screen, colors[i], (body_x+cx, body_y+cy), radius) 
                    
    draw_grids(pa, pb)
    
    S = rk4(S, M, h) 

    pygame.display.flip()