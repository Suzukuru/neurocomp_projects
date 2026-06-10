import numpy as np

# 3D Rotation Matrices
## XX XY XZ
## YX YY YZ
## ZX ZY ZZ
def X_3D(a):
    return np.array([[1,             0,          0],
                    [0,     np.cos(a),  -np.sin(a)],
                    [0,     np.sin(a),  np.cos(a) ]])
def Y_3D(a):
    return np.array([[np.cos(a),     0,  np.sin(a)],
                    [0,             1,          0],
                    [-np.sin(a),    0,  np.cos(a)]])
def Z_3D(a):
    return np.array([[np.cos(a),  -np.sin(a),    0],
                    [np.sin(a),  np.cos(a),     0],   
                    [0,             0,          1]])
    
# 4D Rotation Matrices
## XX XY XZ XW
## YX YY YZ YW
## ZX ZY ZZ ZW
## WX WY WZ WW
def XW_4D(a):
    # Rotated: XX XW WX WW
    # No Rotation: YY ZZ
    return np.array([[np.cos(a),    0,     0,     -np.sin(a)],
                     [0,            1,     0,              0],
                     [0,            0,     1,              0],
                     [np.sin(a),    0,     0,      np.cos(a)]])
def YW_4D(a):
    # Rotated: YY YW WY WW
    # No Rotation: XX ZZ
    return np.array([[1,    0,              0,              0],
                     [0,    np.cos(a),      0,     -np.sin(a)],
                     [0,    0,              1,              0],
                     [0,    np.sin(a),      0,      np.cos(a)]])
def ZW_4D(a):
    # Rotated: ZZ ZW WZ WW
    # No Rotation: XX YY
    return np.array([[1,            0,     0,                      0],
                     [0,            1,     0,                      0],
                     [0,            0,     np.cos(a),     -np.sin(a)],
                     [0,            0,     np.sin(a),      np.cos(a)]])
def XZ_4D(a):
    # Rotated: XX ZX XZ ZZ
    # No Rotation: YY WW
    return np.array([[np.cos(a),    0,   -np.sin(a),    0],
                    [0,             1,    0,            0],
                    [np.sin(a),    0,    np.cos(a),    0],
                    [0,             0,    0,            1]])
def YZ_4D(a):
    # Rotated: YY ZY YZ ZZ
    # No Rotation: XX WW
    return np.array([[1,           0,   0,              0],
                    [0,     np.cos(a),  -np.sin(a),     0],
                    [0,     np.sin(a),  np.cos(a),      0],
                    [0,             0,  0,              1]])
def XY_4D(a):
    # Rotated: XX YX XY YY
    # No Rotation: ZZ WW
    return np.array([[np.cos(a),    -np.sin(a),     0,      0],
                    [np.sin(a),     np.cos(a),      0,      0],   
                    [0,             0,              1,      0],
                    [0,             0,              0,      1]])

# Composition Rotation Matrices
def full_3D(a):
    return Z_3D(a) @ Y_3D(a) @ X_3D(a)

def full_4D(a):
    return XY_4D(a) @ XZ_4D(a) @ YZ_4D(a) @ ZW_4D(a) @ XW_4D(a) @ YW_4D(a)