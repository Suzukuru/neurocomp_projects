import numpy as np
import matplotlib.pyplot as plt

# Constants defined in HH model paper
E_na = 50
E_k= -77
E_l = -54

g_na = 120 
g_k = 36
g_l = 0.3

c_membrane = 1

dt = 0.001 # in ms
I_ext = 0

def calculate_alpha_beta(V):
    alpha_n = (0.01*(V+55))/(1-np.exp(-((V+55)/10)))
    beta_n = 0.125*np.exp(-((V+65)/80))
        
    alpha_m = (0.1*(V+40))/(1-np.exp(-((V+40)/10)))
    beta_m = 4*np.exp(-((V+65)/18))
        
    alpha_h = 0.07*np.exp(-((V+65)/20))
    beta_h = (1/(1+np.exp(-(V+35)/10)))
    
    return np.array([alpha_n, alpha_m, alpha_h]), np.array([beta_n, beta_m, beta_h])

def derive_f(S):
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

def rk4(S, h):
    k1 = derive_f(S)
    k2 = derive_f(S+h/2*k1)
    k3 = derive_f(S+h/2*k2)
    k4 = derive_f(S+h*k3)
    return S + ((h/6)*(k1 + 2*k2 + 2*k3 + k4))

def initialize_resting():
    V = -65
    a, b = calculate_alpha_beta(V)
    n, m, h = a / (a + b)
    
    return np.array([V, n, m, h])

if __name__ == "__main__":
    # State vector components: V, n, m, h
    S = initialize_resting()
    signal = []
    signal.append(S)
    
    I_ext = 0
    for i in range(30000):
        S = rk4(S, dt)
        signal.append(S)
    print(signal[-1])
    
    I_ext = 20
    for i in range(100800):
        S = rk4(S, dt)
        signal.append(S)
    print(signal[0])
    print(signal[-1])

    I_ext = 0
    for i in range(100000):
        S = rk4(S, dt)
        signal.append(S)
    print(signal[-1])

    signal = np.array(signal)
    time = np.arange(len(signal)) * (dt)

    voltage_sim = signal[:, 0]
    gates_sim = signal[:, 1:4]
    conductance_k = g_k*signal[:, 1]**4
    conductance_na = g_na*signal[:, 2]**3*signal[:, 3]
    na_gate = signal[:, 2]**3*signal[:, 3]
    k_gate = signal[:, 1]**4

    fig, axes = plt.subplots(2, 3, figsize=(15,10))

    axes[0][0].plot(time, voltage_sim)
    axes[0][0].set_title("V_membrane over time")
    axes[0][0].set_ylabel("mV")
    axes[0][0].set_xlabel("ms")
    axes[0][0].legend(["mV"])
    
    axes[0][1].plot(time, gates_sim)
    axes[0][1].set_title("raw gate proportions")
    axes[0][1].set_ylabel("proportion")
    axes[0][1].set_xlabel("ms")
    axes[0][1].legend(["n", "m", "h"])
    
    axes[0][2].plot(time, k_gate)
    axes[0][2].plot(time, na_gate)
    axes[0][2].set_title("na vs k gates opened")
    axes[0][2].set_ylabel("% open")
    axes[0][2].set_xlabel("ms")
    axes[0][2].legend(["n", "m**3*h"])

    axes[1][0].plot(time, conductance_k)
    axes[1][0].set_title("K conductance")
    axes[1][0].set_ylabel("m*mho/cm^3")
    axes[1][0].set_xlabel("ms")
    axes[1][0].legend(["C"])

    axes[1][1].plot(time, conductance_na)
    axes[1][1].set_title("Na conductance")
    axes[1][1].set_ylabel("m*mho/cm^3")
    axes[1][1].set_xlabel("ms")
    axes[1][1].legend(["C"])
    plt.show()