import pygame, transformations as rot, controls

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
    
    return camera_position

def user_ObjectRotation(keys, active_object, d_angle, dt, full_rotation):
    ### Rotation Controls
    if active_object.type == "cube":
        if keys[pygame.K_1]:
            active_object.rotation = [rot.X_3D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_2]:
            active_object.rotation = [rot.Y_3D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_3]:
            active_object.rotation = [rot.Z_3D(d_angle * dt) @ v for v in active_object.rotation]
    elif active_object.type == "tesseract":
        if keys[pygame.K_1]:
            active_object.rotation = [rot.YW_4D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_2]:
            active_object.rotation = [rot.XW_4D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_3]:
            active_object.rotation = [rot.ZW_4D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_4]:
            active_object.rotation = [rot.YZ_4D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_5]:
            active_object.rotation = [rot.XZ_4D(d_angle * dt) @ v for v in active_object.rotation]
        if keys[pygame.K_6]:
            active_object.rotation = [rot.XY_4D(d_angle * dt) @ v for v in active_object.rotation]

    if keys[pygame.K_BACKQUOTE] and can_press(pygame.K_BACKQUOTE):
        full_rotation = not full_rotation
    
    return full_rotation, active_object.rotation

"""def user_ShapeChoice(keys, active_object, screen):
    ### Object Selection
    if keys[pygame.K_c] and can_press(pygame.K_c):
        active_object = objects.cube
        active_object.rotation = objects.cube.verts.copy()
        screen.fill((0, 0, 0))
    if keys[pygame.K_t] and can_press(pygame.K_t):
        active_object = objects.tesseract
        active_object.rotation = objects.tesseract.verts.copy()
        screen.fill((0, 0, 0))
        
    return active_object

"""