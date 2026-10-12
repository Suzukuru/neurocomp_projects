# Random Practice and Projects

## Linear Algebra Focus
### 3D Movable Camera + Tesseract
Simulates a 3D camera by performing Euler 3D rotation matrix multiplication on the vertices of the lines drawn, the lines follow their respective vertices as they are transformed. The rotation matrix is reversed for left and right panning to adjust for the camera UX conventions. Movement is achieved by incrementing/decrementing Z for WS keys respectively, X for AD respectively, and Y for QE respectively (utilizes cross product). \
\
Tesseract is the same idea, applying a 4D rotation matrix onto the tesseract vertices and the lines follow their respective vertices as they are transformed. \
\
The calculations are done within the dimensions of the object (object space), but these two are ultimately projected onto a 2D screen (screen space). A 3D to 2D projection matrix is applied to the camera, while for the tesseract a 4D to 3D then 3D to 2D projection matrix is applied. \
\
Pitch rotation is limited to 180 degrees to prevent gimbal lock using np.clip() as exceeding it leads the matrix collapsing a dimension leading to camera bugs. 
### 3 Body Problem RK4
3D dynamical system evolving inside of world space

## Computational Neuroscience Focus
### Hodgkin-Huxley Model
Four coupled first order ODEs showing the magic inside of action potentials using RK4 (classic fixed-step fourth-order Runge-Kutta) for a numerical approximation. The following equations are derived from the HH paper with the resting voltage adjusted by -65mV to fit current standards.

#### **Rate functions** ($`V`$ in mV) 
Adjusting resting potential the  adjusted by -65mV, requires adjusting the the rate functions of the voltage-dependent gates so they behave as expected.
```math
\begin{aligned}
\alpha_n(V) &= \frac{0.01(V + 55)}{1 - e^{-(V + 55)/10}} & \beta_n(V) &= 0.125 e^{-(V + 65)/80} \\[6pt]
\alpha_m(V) &= \frac{0.1(V + 40)}{1 - e^{-(V + 40)/10}} & \beta_m(V) &= 4 e^{-(V + 65)/18} \\[6pt]
\alpha_h(V) &= 0.07 e^{-(V + 65)/20} & \beta_h(V) &= \frac{1}{1 + e^{-(V + 35)/10}}
\end{aligned}
```

#### **Initial conditions**

Gates start at their steady-state values for $`V_0 = -65`$ mV, executed by the initialize_resting() function:
```math
x_\infty = \frac{\alpha_x(V_0)}{\alpha_x(V_0) + \beta_x(V_0)}, \qquad x \in \{n, m, h\}
```

```math
\mathbf{S}_{i+1} = \mathbf{S}_i + \frac{\Delta t}{6}\left(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4\right)
```

#### **Constants**
| Parameter | Symbol | Value | Units |
|---|---|---|---|
| Sodium reversal potential | $`E_{\text{Na}}`$ | 50 | mV |
| Potassium reversal potential | $`E_{\text{K}}`$ | -77 | mV |
| Leak reversal potential | $`E_{\text{L}}`$ | -54 | mV |
| Max sodium conductance | $`\bar{g}_{\text{Na}}`$ | 120 | mS/cm² |
| Max potassium conductance | $`\bar{g}_{\text{K}}`$ | 36 | mS/cm² |
| Leak conductance | $`\bar{g}_{\text{L}}`$ | 0.3 | mS/cm² |
| Membrane capacitance | $`C_m`$ | 1 | µF/cm² |
| Time step | $`\Delta t`$ | 0.001 | ms |

#### **State and functions**
- **`S`** (snapshot of the system's state) contains:
  - `V`: neuron's voltage
  - `n`: K channel activation
  - `m`: Na channel activation
  - `h`: Na channel inactivation
- **`derive_f()`** takes in `S` (snapshot of the state), utilizing the equations from the HH paper and the adjusted rate functions. It returns the rate of change of each variable in the state.
- **`rk4()`** numerically approximates by adding to the current state the final approximation of change from `derive_f()` at each step size.

