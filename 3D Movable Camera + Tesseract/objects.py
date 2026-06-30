import numpy as np

class Shape:
    def __init__(self, type, verts, edges):
        self.type = type
        self.verts = verts
        self.edges = edges
        self.rotation = verts.copy()

    def __repr__(self):
        return self.name
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
cube = Shape(
    type = "cube",
    ### Vertices: points in the cube
    ### [a, b, c] =  RIGHT/LEFT, TOP/BOTTOM, FRONT/BACK
    verts=np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
                    #0 LeBoBa      #1 RiBoBa   #2 RiToBa    #3 LeToBa
                    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], dtype=float),
                    #4 LeBoFro   #5 RiBoFro  #6 RiToFro   #7 LeToFro
                    
    ### Edges: lines in the cube
    edges=np.array([(0, 1), (1, 2), (2, 3), (3, 0), # Back
                    (4, 5), (5, 6), (6, 7), (7, 4), # Front
                    (0, 4), (1, 5), (2, 6), (3, 7),]) # Connecting 
)

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
tesseract = Shape(
    type = "tesseract",
    ### Vertices: points in the cube
    ### [x, y, z, w] =  RIGHT/LEFT, TOP/BOTTOM, FRONT/BACK, OUTER/INNER
    verts = np.array([[-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
                        #0 LeBoBaOut      #1 RiBoBaOut   #2 RiToBaOut    #3 LeToBaOut
                        [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1],
                        #4 LeBoFroOut   #5 RiBoFroOut  #6 RiToFroOut   #7 LeToFroOut
                        [-1, -1, -1, -1], [1, -1, -1, -1], [1, 1, -1, -1], [-1, 1, -1, -1],
                        #8 LeBoBaIn      #9 RiBoBaIn   #10 RiToBaIn    #11 LeToBaIn
                        [-1, -1, 1, -1], [1, -1, 1, -1], [1, 1, 1, -1], [-1, 1, 1, -1]], dtype=float),
                        #12 LeBoFroIn   #13 RiBoFroIn  #14 RiToFroIn   #15 LeToFroIn
            
    ### Edges: lines in the cube
    edges = np.array([(0, 1), (1, 2), (2, 3), (3, 0),           # Outer Back ; Differs in X, Y, X, Y
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
)