# Random Practice and Projects

## Linear Algebra Focus

## Computational Neuroscience Focus
### Hodgkin-Huxley Model
Four coupled first order ODEs showing the magic inside of action potentials using RK4 (classic fixed-step fourth-order Runge-Kutta) for a numerical approximation. The following equations are derived from the HH paper with the resting voltage adjusted by -65 to fit current standards.

#### Equations and Constants

**Membrane voltage**

```math
C_m \frac{dV}{dt} = I_{\text{ext}} - I_{\text{Na}} - I_{\text{K}} - I_{\text{L}}
```

**Ionic currents**

```math
\begin{aligned}
I_{\text{Na}} &= \bar{g}_{\text{Na}} m^3 h (V - E_{\text{Na}}) \\
I_{\text{K}} &= \bar{g}_{\text{K}} n^4 (V - E_{\text{K}}) \\
I_{\text{L}} &= \bar{g}_{\text{L}} (V - E_{\text{L}})
\end{aligned}
```

**Gating variables**

Each gate $`x \in \{n, m, h\}`$ is the fraction of open gates and follows first-order kinetics:

```math
\frac{dx}{dt} = \alpha_x(V)(1 - x) - \beta_x(V)x
```

**Rate functions** ($`V`$ in mV, resting potential at $`-65`$ mV)

```math
\begin{aligned}
\alpha_n(V) &= \frac{0.01(V + 55)}{1 - e^{-(V + 55)/10}} & \beta_n(V) &= 0.125 e^{-(V + 65)/80} \\[6pt]
\alpha_m(V) &= \frac{0.1(V + 40)}{1 - e^{-(V + 40)/10}} & \beta_m(V) &= 4 e^{-(V + 65)/18} \\[6pt]
\alpha_h(V) &= 0.07 e^{-(V + 65)/20} & \beta_h(V) &= \frac{1}{1 + e^{-(V + 35)/10}}
\end{aligned}
```

**Conductances**

```math
g_{\text{K}}(t) = \bar{g}_{\text{K}} n^4
\qquad
g_{\text{Na}}(t) = \bar{g}_{\text{Na}} m^3 h
```

**Initial conditions**

Gates start at their steady-state values for $`V_0 = -65`$ mV:

```math
x_\infty = \frac{\alpha_x(V_0)}{\alpha_x(V_0) + \beta_x(V_0)}, \qquad x \in \{n, m, h\}
```

**Numerical integration (RK4)**

With state vector $`\mathbf{S} = [V, n, m, h]^T`$ and $`\mathbf{S}' = \mathbf{f}(\mathbf{S})`$:

```math
\begin{aligned}
\mathbf{k}_1 &= \mathbf{f}(\mathbf{S}_i) \\
\mathbf{k}_2 &= \mathbf{f}\left(\mathbf{S}_i + \tfrac{\Delta t}{2}\mathbf{k}_1\right) \\
\mathbf{k}_3 &= \mathbf{f}\left(\mathbf{S}_i + \tfrac{\Delta t}{2}\mathbf{k}_2\right) \\
\mathbf{k}_4 &= \mathbf{f}\left(\mathbf{S}_i + \Delta t \mathbf{k}_3\right)
\end{aligned}
```

```math
\mathbf{S}_{i+1} = \mathbf{S}_i + \frac{\Delta t}{6}\left(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4\right)
```

**Constants**

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

#### Simulation Protocol

| Phase | Duration | $`I_{\text{ext}}`$ |
|---|---|---|
| Settle at rest | 30 ms | 0 µA/cm² |
| Stimulus | 100.8 ms | 20 µA/cm² |
| Recovery | 100 ms | 0 µA/cm² |

The state variables are V (neuron's voltage), n (K channel activation), m (Na channel activation), and h (Na channel inactivation). This is returned by derive_f() function. 
