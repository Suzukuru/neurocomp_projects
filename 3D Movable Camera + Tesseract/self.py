import pygame, numpy as np

AXISLIMIT = 2

# 3D Rotation Matrices
## XX XY XZ
## YX YY YZ
## ZX ZY ZZ
def rot3D_X(a):
    return np.array([[1,             0,          0],
                    [0,     np.cos(a),  -np.sin(a)],
                    [0,     np.sin(a),  np.cos(a) ]])

def rot3D_Y(a):
    return np.array([[np.cos(a),     0,  np.sin(a)],
                    [0,             1,          0],
                    [-np.sin(a),    0,  np.cos(a)]])

def rot3D_Z(a):
    return np.array([[np.cos(a),  -np.sin(a),    0],
                    [np.sin(a),  np.cos(a),     0],   
                    [0,             0,          1]])
    
def rot_3D(a):
    return rot3D_Z(a) @ rot3D_Y(a) @ rot3D_X(a) 

# 4D Rotation Matrices
## XX XT XZ XW
## YX YY YZ YW
## ZX ZY ZZ ZW
## WX WY WZ WW
def rot4D_XW(a):
    #print("XW:",a)
    # Rotated: XX XW WX WW
    # No Rotation: YY ZZ
    return np.array([[np.cos(a),    0,     0,     -np.sin(a)],
                     [0,            1,     0,              0],
                     [0,            0,     1,              0],
                     [np.sin(a),    0,     0,      np.cos(a)]])

def rot4D_YW(a):
    #print("YW:", a)
    # Rotated: YY YW WY WW
    # No Rotation: XX ZZ
    return np.array([[1,    0,              0,              0],
                     [0,    np.cos(a),      0,     -np.sin(a)],
                     [0,    0,              1,              0],
                     [0,    np.sin(a),      0,      np.cos(a)]])

def rot4D_ZW(a):
    #print("ZW:", a)
    # Rotated: ZZ ZW WZ WW
    # No Rotation: XX YY
    return np.array([[1,            0,     0,                      0],
                     [0,            1,     0,                      0],
                     [0,            0,     np.cos(a),     -np.sin(a)],
                     [0,            0,     np.sin(a),      np.cos(a)]])
    
def rot4D_XZ(a):
    #print("XZ:",a)
    # Rotated: XX ZX XZ ZZ
    # No Rotation: YY WW
    return np.array([[np.cos(a),    0,   -np.sin(a),    0],
                    [0,             1,    0,            0],
                    [-np.sin(a),    0,    np.cos(a),    0],
                    [0,             0,    0,            1]])
    
def rot4D_YZ(a):
    #print("YZ:",a)
    # Rotated: YY ZY YZ ZZ
    # No Rotation: XX WW
    return np.array([[1,           0,   0,              0],
                    [0,     np.cos(a),  -np.sin(a),     0],
                    [0,     np.sin(a),  np.cos(a),      0],
                    [0,             0,  0,              1]])


def rot4D_XY(a):
    #print("XY:",a)
    # Rotated: XX YX XY YY
    # No Rotation: ZZ WW
    return np.array([[np.cos(a),    -np.sin(a),     0,      0],
                    [np.sin(a),     np.cos(a),      0,      0],   
                    [0,             0,              1,      0],
                    [0,             0,              0,      1]])

def rot_4D(a):
    matrix = rot4D_XY(a) @ rot4D_XZ(a) @ rot4D_YZ(a) @ rot4D_ZW(a) @ rot4D_XW(a) @ rot4D_YW(a)
    #print(matrix, end='\n\n')
    return matrix

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

# Cube
""" 
Le = Left ; Ri = Right
Bo = Bottom ; To = Top
Ba = Back ; Fro = Front

       3----2
      /|   /|
     7----6 |
     | 0--|-1
     |/   |/
     4----5
"""

### Vertices: points in the cube
### [a, b, c] =  RIGHT/LEFT, TOP/BOTTOM, FRONT/BACK
cube_verts = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                        #0 LeBoBa      #1 RiBoBa   #2 RiToBa    #3 LeToBa
                       [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=float)
                         #4 LeBoFro   #5 RiBoFro  #6 RiToFro   #7 LeToFro
                  
### Edges: lines in the cube
cube_edges = np.array([(0, 1), (1, 2), (2, 3), (3, 0), # Back
                  (4, 5), (5, 6), (6, 7), (7, 4), # Front
                  (0, 4), (1, 5), (2, 6), (3, 7),]) # Connecting

# Tesseract
""" 
Le = Left ; Ri = Right
Bo = Bottom ; To = Top
Ba = Back ; Fro = Front
Out = Outer ; In = Inner

	   3---------------------2
     / |   \              / /|
    /  |    \            / / |
   7---|-----11-------10--6  |
   | \ |   / |       / | /|  |
   |   \  /  |      / /|  |  |
   |   | 15--|-----14  |  |  |
   |   | | |       |   |  |  |
   |   | | 8-------|---9 \|  |
   |   | |//       |  /   |\ |
   |   0-|---------|-/----|--1
   |  /  12---------13    |  /
   | / /               \  | /
   |//                   \|/
   4----------------------5
"""

### Vertices: points in the cube
### [x, y, z, w] =  RIGHT/LEFT, TOP/BOTTOM, FRONT/BACK, OUTER/INNER
tesseract_verts = np.array([[-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
                            #0 LeBoBaOut      #1 RiBoBaOut   #2 RiToBaOut    #3 LeToBaOut
                            [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1],
                            #4 LeBoFroOut   #5 RiBoFroOut  #6 RiToFroOut   #7 LeToFroOut
                            [-1, -1, -1, -1], [1, -1, -1, -1], [1, 1, -1, -1], [-1, 1, -1, -1],
                            #8 LeBoBaIn      #9 RiBoBaIn   #10 RiToBaIn    #11 LeToBaIn
                            [-1, -1, 1, -1], [1, -1, 1, -1], [1, 1, 1, -1], [-1, 1, 1, -1]], dtype=float)
                            #12 LeBoFroIn   #13 RiBoFroIn  #14 RiToFroIn   #15 LeToFroIn
                  
### Edges: lines in the cube
tesseract_edges = np.array([(0, 1), (1, 2), (2, 3), (3, 0),           # Outer Back ; Differs in X, Y, X, Y
                            (4, 5), (5, 6), (6, 7), (7, 4),           # Outer Front ; Differs in X, Y, X, Y
                            (0, 4), (1, 5), (2, 6), (3, 7),           # Outer Connecting ; Differs in Z only
                            (8, 9), (9, 10), (10, 11), (11, 8),       # Inner Back ; Differs in X, Y, X, Y
                            (12, 13), (13, 14), (14, 15), (15, 12),   # Inner Front ; Differs in X, Y, X Y
                            (8, 12), (9, 13), (10, 14), (11, 15),     # Inner Connecting ; Differs in Z only
                            (0, 8), (1, 9), (4, 12), (5, 13),         # Bottom Inner-Outer Connecting ; Differs in W
                            (2, 10), (3, 11), (6, 14), (7, 15)])      # Top Inner-Outer Connecting ; Differs in W
### Varies By
# X: (0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15) 
# Y: (1, 2), (3, 0), (5, 6), (7, 4), (9, 10), (11, 8), (13, 14), (15, 12) 
# Z: (0, 4), (1, 5), (2, 6), (3, 7), (8, 12), (9, 13), (10, 14), (11, 15)
# W: (0, 8), (1, 9), (4, 12), (5, 13), (2, 10), (3, 11), (6, 14), (7, 15)

# Grids: Floor
pa, pb = make_grid(6, 1)

# Camera and Movement Properties
camera_position = np.array([0, 0, 0], dtype=float)
camera_yaw = 0.0
camera_pitch = 0.0
movespeed = 0.1
sensitivity = 0.001

# Pygame
pygame.init()
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0
object_angle = 0

### Pygame Settings
screen = pygame.display.set_mode((1500, 1000)) 
cx, cy = (750, 500)
pygame.event.set_grab(True) 
pygame.mouse.set_visible(False)

print(rot_4D(0.1))

# Main Loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            pygame.quit()
            exit()
            
    # Loop Settings
    screen.fill((20, 20, 20)) # Background Color
    object_angle += 0.01 # Object Rotation Speed

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
    front = rot3D_Y(-camera_yaw) @ rot3D_X(-camera_pitch) @  np.array([0, 0, 1]) # Remove pitch for FPS camera / for flat plane movement only
    right = rot3D_Y(-camera_yaw) @ np.array([1, 0, 0])
    up = np.cross(right, front) 

    # Key Controls
    ### W/S = Z-axis ; A/D = X-azis
    if keys[pygame.K_w]:
        camera_position += front * movespeed
    if keys[pygame.K_s]:
        camera_position -= front * movespeed
    if keys[pygame.K_a]:
        camera_position -= right * movespeed
    if keys[pygame.K_d]:
        camera_position += right * movespeed
        
    ### Q/E Y-axis movement
    if keys[pygame.K_q]:
        camera_position += up * movespeed
    if keys[pygame.K_e]:
        camera_position -= up * movespeed
        
    ### Rotation Controls
    
    ### Object Selection
    

    # Cube Object Matrix Operations
    #rotated = [rot_3D(object_angle) @ v for v in cube_verts] ## Continuously applies z<-y<-x rotate matrices at fixed angle
    #camera_perspective = [rot3D_Y(camera_yaw) @ rot3D_X(camera_pitch) @ (v - camera_position) for v in rotated] ## Camera Yaw Matrix <- Camera Pitch Matrix <- Center Camera to Position
    #projected = [project_2D(v) for v in camera_perspective] ## Recalcuates for 2D screen  
    
    # Cube Object Matrix Operations
    rotated = [rot_4D(object_angle) @ v for v in tesseract_verts] ## Continuously applies z<-y<-x rotate matrices at fixed angle
    projected_3D = [project_3D(v) for v in rotated]## Recalcuates for 2D screen  
    camera_perspective = [rot3D_Y(camera_yaw) @ rot3D_X(camera_pitch) @ (v - camera_position) for v in projected_3D] ## Camera Yaw Matrix <- Camera Pitch Matrix <- Center Camera to Position
    projected_2D = [project_2D(v) for v in camera_perspective] ## Recalcuates for 2D screen  
    
    #print(projected)
    
    # Draw Cube
    for a, b in tesseract_edges:
        za = camera_perspective[a]
        zb = camera_perspective[b]

        if za[2] < -AXISLIMIT or zb[2] < -AXISLIMIT: continue ## Prevents Z Axis Near Clipping Visual Bugs 
        
        pygame.draw.line(screen, (255, 255, 255),
                         (projected_2D[a] + [cx, cy]).astype(int),
                         (projected_2D[b] + [cx, cy]).astype(int))
    
    # Draw Grids
    for a, b in zip(pa, pb):
        
        a = rot3D_Y(camera_yaw) @ rot3D_X(camera_pitch) @ (a - camera_position)
        b = rot3D_Y(camera_yaw) @ rot3D_X(camera_pitch) @ (b - camera_position)
        
        if a[2] < -AXISLIMIT or b[2] < -AXISLIMIT: continue ## Prevents Z Axis  Near Clipping Visual Bugs
        
        line_X  = project_2D(a) + [cx, cy]
        line_Z  = project_2D(b) + [cx, cy]
        
        pygame.draw.line(screen, (100, 100, 100),
                         line_X,
                         line_Z)
    
    pygame.display.flip()
    clock.tick(60)