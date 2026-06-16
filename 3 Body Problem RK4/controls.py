import pygame, numpy as np

rng = np.random.default_rng()
_key_cooldowns = {}
COOLDOWN = 1000

def can_press(key):
    now = pygame.time.get_ticks()
    if key not in _key_cooldowns or now - _key_cooldowns[key] > COOLDOWN:
        _key_cooldowns[key] = now
        return True
    return False

def user_CameraMovement(keys, front, right, up, movespeed, camera_position):
    if keys[pygame.K_w]:
        camera_position += (front * movespeed)
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
    
    return camera_position

def user_ObjectState(keys, S, M, body_trail):
    if keys[pygame.K_r] and can_press(pygame.K_r):
        S = rng.uniform(low=-1, high=1, size=12)
        M = rng.uniform(low=1, high=3, size=3)
        body_trail = []
    if keys[pygame.K_1] and can_press(pygame.K_1):
        S = np.array([0.97000436, -0.24308753, -0.97000436, 0.24308753, 0, 0,
                        0.466203685, 0.43236573, 0.466203685, 0.43236573, -0.93240737, -0.86473146]) 
        M = np.array([1.0, 1.0, 1.0])
        body_trail = []
        
    return S, M, body_trail