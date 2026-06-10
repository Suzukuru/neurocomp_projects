import pygame
import numpy as np 

import objects
import transformations as rot
import controls as handle

AXISLIMIT = 2

def project_3D(v):
    x, y, z, w = v
    w += AXISLIMIT
    
    return np.array([x/w, y/w, z/w])

def project_2D(v, fov=400):
    x, y, z = v
    z += AXISLIMIT
    
    return np.array([x/z * fov, y/z * fov])

# Grid maker, size x size
def make_grid(size, step):
    pa = []
    pb = []
    y_floor = 2
    
    for i in range(-size, size+1, step):
        pa.append(np.array([-size, y_floor, i]))
        pb.append(np.array([size, y_floor, i]))
        pa.append(np.array([i, y_floor, -size]))
        pb.append(np.array([i, y_floor, size]))
    
    return (pa, pb)

def draw_object(projection, camera_perspective, edges):
        for a, b in edges:
            za = camera_perspective[a]
            zb = camera_perspective[b]

            if za[2] < -AXISLIMIT or zb[2] < -AXISLIMIT: continue ## Prevents Z Axis Near Clipping Visual Bugs 

            pygame.draw.line(screen, (255, 255, 255),
                            (projection[a] + [cx, cy]).astype(int),
                            (projection[b] + [cx, cy]).astype(int))

def draw_grids(pa, pb):
    for a, b in zip(pa, pb):
        
        a = rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch) @ (a - camera_position)
        b = rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch) @ (b - camera_position)
        
        if a[2] < -AXISLIMIT or b[2] < -AXISLIMIT: continue ## Prevents Z Axis  Near Clipping Visual Bugs
        
        line_X  = project_2D(a) + [cx, cy]
        line_Z  = project_2D(b) + [cx, cy]
        
        pygame.draw.line(screen, (100, 100, 100),
                         line_X,
                         line_Z)
    

# Grids: Floor
pa, pb = make_grid(6, 1)

# Camera and Movement Properties
camera_position = np.array([0, 0, 0], dtype=float)
camera_yaw = 0.0
camera_pitch = 0.0
movespeed = 0.1
sensitivity = 0.001
camera_perspective = []
full_rotation = False

# Pygame
pygame.init()
clock = pygame.time.Clock()

d_angle = 1

active_object = objects.tesseract

### Pygame Settings
screen = pygame.display.set_mode((1500, 1000)) 
cx, cy = (750, 500)
pygame.event.set_grab(True) 
pygame.mouse.set_visible(False)

# Main Loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            pygame.quit()
            exit()
    dt = clock.tick(60) / 1000.0 
    
    # Loop Settings
    screen.fill((20, 20, 20)) # Background Color

    # User Behavior
    keys = pygame.key.get_pressed()
    rel_x, rel_y = pygame.mouse.get_rel()
    camera_yaw += rel_x * sensitivity
    camera_pitch += rel_y * sensitivity
    camera_pitch = np.clip(camera_pitch, -np.pi/2, np.pi/2) # gimbal lock, prevents camera from going upside down and ivnerting controls.

    
    # Free Camera Axes
    """
    World Convention: X=right, Y=up, Z=toward viewer (right-handed)
      up (+Y)
      |
      |
      |_________ right (+X)
     /
    /
    front (+Z)
    """ 
    front = rot.Y_3D(-camera_yaw) @ rot.X_3D(-camera_pitch) @  np.array([0, 0, 1]) # Remove pitch for FPS camera / for flat plane movement only
    right = rot.Y_3D(-camera_yaw) @ np.array([1, 0, 0])
    up = np.cross(right, front) 


    active_object = handle.user_ShapeChoice(keys, active_object, screen)
    camera_position = handle.user_CameraMovement(keys, front, right, up, movespeed, camera_position)
    full_rotation, active_object.rotation = handle.user_ObjectRotation(keys, active_object, d_angle, dt, full_rotation)


    # Tesseract Object Matrix Operations
    if active_object.type == "tesseract":
        if full_rotation: 
            active_object.rotation = [rot.full_4D(d_angle * dt) @ v for v in active_object.rotation]
            
        projected_3D = [project_3D(v) for v in active_object.rotation] ## Perspective Projection from 4D->3D 
        camera_perspective = [rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch) @ (v - camera_position) for v in projected_3D] ## Camera Yaw Matrix <- Camera Pitch Matrix <- Center Camera to Position
        projected_2D = [project_2D(v) for v in camera_perspective] ## Perspective Projection from 3D->2D 
    
    # Cube Object Matrix Operations
    elif active_object.type == "cube":    
        if full_rotation: 
            active_object.rotation = [rot.full_3D(d_angle * dt) @ v for v in active_object.rotation]

        camera_perspective = [rot.Y_3D(camera_yaw) @ rot.X_3D(camera_pitch ) @ (v - camera_position) for v in active_object.rotation] ## Camera Yaw Matrix <- Camera Pitch Matrix <- Center Camera to Position
        projected_2D = [project_2D(v) for v in camera_perspective] ## Perspective Projection from 3D->2D 
        

    # Draw Cube
    draw_object(projected_2D, camera_perspective, active_object.edges)
    
    # Draw Grids
    draw_grids(pa, pb)
    
    pygame.display.flip()