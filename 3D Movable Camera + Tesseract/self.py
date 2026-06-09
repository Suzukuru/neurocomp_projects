import pygame, numpy as np

ZLIMIT = 5

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


# [a, b, c] =  RIGHT/LEFT, TOP/BOTTOM, FRONT/BACK
verts = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                 [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=float)
edges = np.array([(0, 1), (1, 2), (2, 3), (3, 0),
                  (4, 5), (5, 6), (6, 7), (7, 4),
                  (0, 4), (1, 5), (2, 6), (3, 7),])

camera_position = np.array([0, 0, 0], dtype=float)
camera_yaw = 0
camera_pitch = 0
movespeed = 0.01


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 1000))
cx, cy = (400, 500)
angle = 0
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

while True:
    for e in pygame.event.get():
        if e == pygame.QUIT: 
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera_position[2] += movespeed
        print("W")
    if keys[pygame.K_s]:
        camera_position[2] -= movespeed
    if keys[pygame.K_a]:
        camera_position[0] -= movespeed
    if keys[pygame.K_d]:
        camera_position[0] += movespeed
    if keys[pygame.K_q]:
        camera_position[1] += movespeed
    if keys[pygame.K_e]:
        camera_position[1] -= movespeed

    print(camera_position)


    angle += 0.001
    screen.fill((20, 20, 20))

    rotated = [rot_3D(angle) @ v for v in verts]
    projected = [project_2D(v - camera_position) + [cx, cy] for v in rotated]
    
    for a, b in edges:
        pygame.draw.line(screen, (255, 255, 255),
                         projected[a].astype(int),
                         projected[b].astype(int),)
    
    pygame.display.flip()