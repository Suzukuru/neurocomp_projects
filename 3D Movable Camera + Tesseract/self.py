import pygame, numpy as np

ZLIMIT = 2

# Matrix Rotations
def rot_x(a):
    return np.array([[1,             0,          0],
                    [0,     np.cos(a),  -np.sin(a)],
                    [0,     np.sin(a),  np.cos(a) ]])

def rot_y(a):
    return np.array([[np.cos(a),     0,  np.sin(a)],
                    [0,             1,          0],
                    [-np.sin(a),    0,  np.cos(a)]])

def rot_z(a):
    return np.array([[np.cos(a),  -np.sin(a),    0],
                    [np.sin(a),  np.cos(a),     0],   
                    [0,             0,          1]])
    
def rot_3D(a):
    return rot_z(a) @ rot_y(a) @ rot_x(a) 


def project_2D(v, fov=400):
    x, y, z = v
    z += ZLIMIT
    
    return np.array([x/z * fov, y/z * fov])

def make_grid(size, step):
    pa = []
    pb = []
    y_floor = 1.0
    
    for i in range(-size, size+1, step):
        pa.append(np.array([-size, y_floor, i]))
        pb.append(np.array([size, y_floor, i]))
        pa.append(np.array([i, y_floor, -size]))
        pb.append(np.array([i, y_floor, size]))
    
    return (pa, pb)

# [a, b, c] =  RIGHT/LEFT, TOP/BOTTOM, FRONT/BACK
verts = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                 [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=float)
edges = np.array([(0, 1), (1, 2), (2, 3), (3, 0),
                  (4, 5), (5, 6), (6, 7), (7, 4),
                  (0, 4), (1, 5), (2, 6), (3, 7),])

pa, pb = make_grid(3, 1)

pygame.init()
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0
screen = pygame.display.set_mode((800, 1000))
cx, cy = (400, 500)
angle = 0
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

camera_position = np.array([0, 0, 0], dtype=float)
camera_yaw = 0.0
camera_pitch = 0.0
movespeed = 0.1
sensitivity = 0.001


print(np.shape(pa), "\n\n", np.shape(pb))
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    rel_x, rel_y = pygame.mouse.get_rel()
    camera_yaw += rel_x * sensitivity
    camera_pitch += rel_y * sensitivity
    camera_pitch = np.clip(camera_pitch, -np.pi/2, np.pi/2)
    
    front = rot_y(-camera_yaw) @ rot_x(-camera_pitch) @  np.array([0, 0, 1])
    right = rot_y(-camera_yaw) @ np.array([1, 0, 0])

    if keys[pygame.K_w]:
        camera_position += front * movespeed
    if keys[pygame.K_s]:
        camera_position -= front * movespeed
    if keys[pygame.K_a]:
        camera_position -= right * movespeed
    if keys[pygame.K_d]:
        camera_position += right * movespeed
        
    print(camera_position)
        
    # Y-axis movement
    if keys[pygame.K_q]:
        camera_position[1] += movespeed
    if keys[pygame.K_e]:
        camera_position[1] -= movespeed

    angle += 0.01
    screen.fill((20, 20, 20))

    rotated = [rot_3D(angle) @ v for v in verts]
    camera_perspective = [rot_y(camera_yaw) @ rot_x(camera_pitch) @ (v - camera_position) for v in rotated]
    projected = [project_2D(v) for v in camera_perspective]
    
    #print(projected)
    
    for a, b in edges:
        va = camera_perspective[a]
        vb = camera_perspective[b]

        if va[2] < -ZLIMIT or vb[2] < -ZLIMIT: continue
        
        pygame.draw.line(screen, (255, 255, 255),
                         (projected[a] + [cx, cy]).astype(int),
                         (projected[b] + [cx, cy]).astype(int))
    
    for a, b in zip(pa, pb):
        
        a = rot_y(camera_yaw) @ rot_x(camera_pitch) @ (a - camera_position)
        b = rot_y(camera_yaw) @ rot_x(camera_pitch) @ (b - camera_position)
        
        if a[2] < -ZLIMIT or b[2] < -ZLIMIT: continue
        
        grid_X  = project_2D(a) + [cx, cy]
        grid_Z  = project_2D(b) + [cx, cy]
        
        pygame.draw.line(screen, (100, 100, 100),
                         grid_X,
                         grid_Z)
    
    pygame.display.flip()
    clock.tick(60)