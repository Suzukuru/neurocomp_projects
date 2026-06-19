import numpy as np
import matplotlib.pyplot as plt

def calculate_alpha_beta(V):
    alpha_n = (0.01*(V+75))/(np.expm1((V+75)/10))
    beta_n = 0.125*np.exp(V/80)
        
    alpha_m = (0.1*(V+90))/(np.expm1((V+90)/10))
    beta_m = 4*np.exp((V+65)/18)
        
    alpha_h = 0.07*np.exp((V+65)/20)
    beta_h = (1/(np.expm1((V+95)/10)+1))
    
    return np.array([alpha_n, alpha_m, alpha_h]), np.array([beta_n, beta_m, beta_h])

def derive_f(S, c_membrane, I_ext):
    V, n, m, h = S
    a, b = calculate_alpha_beta(V)
    an, am, ah = a
    bn, bm, bh = b
    
    I_k =  g_k*n**4*(V-E_k)
    I_na =  g_na*m**3*h*(V-E_na)
    I_l = g_l*(V-E_l)  
    
    dV = ((I_ext - I_k - I_na - I_l)/ c_membrane)
    dn = an*(1-n)-bn*n
    dm = am*(1-m)-bm*m
    dh = ah*(1-h)-bh*h
    return np.array([dV, dn, dm, dh])

def rk4(S, c_membrane, I_ext, h):
    k1 = derive_f(S, c_membrane, I_ext)
    k2 = derive_f(S+h/2*k1, c_membrane, I_ext)
    k3 = derive_f(S+h/2*k2, c_membrane, I_ext)
    k4 = derive_f(S+h*k3, c_membrane, I_ext)
    return S + ((h/6)*(k1 + 2*k2 + 2*k3 + k4))

def initialize_resting():
    V = -65
    a, b = calculate_alpha_beta(V)
    gates = [] # n m h
    for i in range(3):
        gates.append(a[i]/(a[i]+b[i]))
    n, m, h = gates
    
    return np.array([V, n, m, h])

# Constants
### These are the theoretical max values that HH Model paper chose based on experimental values at V = 0, refer to page 21
E_na = 50
E_k= -77
E_l = -54

g_na = 120 
g_k = 36
g_l = 0.3

c_membrane = 1

dt = 0.01

# Calculated
I_ext = 10

# State vector components: V, n, m, h
S = initialize_resting()

signal = []
signal.append(S)
for i in range(50000):
    S = rk4(S, c_membrane, I_ext, dt)
    signal.append(S)
    
print(signal[0])
print(signal[-1])

signal.clear()
S = initialize_resting()
I_ext = 30
for i in range(50000):
    S = rk4(S, c_membrane, I_ext, dt)
    signal.append(S)
    
print(signal[0])
print(signal[-1])
