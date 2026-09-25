import numpy as np
import matplotlib.pyplot as plt
import qutip as qt

# ----------------------------------------------------------------------
# Operators
# ----------------------------------------------------------------------
ket_0 = qt.basis(2,0) # TODO
ket_1 = qt.basis(2,1) # TODO

sigma_x = qt.sigmax() # TODO
sigma_z = qt.sigmaz() # TODO

P0_op = ket_0 * ket_0.dag()
P1_op = ket_1 * ket_1.dag()

# Qubit Frequency:
w0 = 5


# ----------------------------------------------------------------------
# Helper Function: Build the Time Dependent Hamiltonian:
#   H(t) = (w0/2) sigma_z + (Omega0*cos(wd*t)/2)
#   H(t) = H0 + H1 * f(t)
# ----------------------------------------------------------------------
def build_hamiltonian(w0, Omega0, wd):
    H0 = (w0/2)*sigma_z # TODO

    def drive_coefficient(t): # f(t)
        return np.cos(wd*t) # TODO

    H1 = (Omega0/2)*sigma_x # TODO

    return [H0, [H1, drive_coefficient]]


def run_sim(w0, psi0, Omega0, wd, t_max, n_points):
    """Solve the Schrodinger equation and return t, P0(t), P1(t)."""
    H = build_hamiltonian(w0, Omega0, wd)
    tlist = np.linspace(0, t_max, n_points)
    result = qt.sesolve(H, psi0, tlist, e_ops=[P0_op, P1_op]) # TODO
    P0_t, P1_t = result.expect
    return tlist, P0_t, P1_t


# ========================================================================
# TASK 1 — No drive (Omega0 = 0), start in |0>
# ========================================================================
initial_state = ket_0 # TODO
Omega0 = 0 # TODO

t1, P0_no_drive, P1_no_drive = run_sim(w0 = w0, psi0=initial_state, Omega0 = Omega0, wd=0.0,
                                       t_max=3, n_points=2000)

plt.figure()
plt.plot(t1, P0_no_drive, label="P0(t)")
plt.plot(t1, P1_no_drive, label="P1(t)", linestyle="--")
plt.xlabel("time")
plt.ylabel("population")
plt.title("Task 1: No drive")
plt.legend()
plt.savefig("task1_no_drive.png", dpi=150)

# TODO: Explain the Physical Meaning of this Plot:
#print("Your Explanation")
print("Since there is no drive (Omega0 = 0), the Hamiltonian is purely H = (w0/2) * sigma_z. Here, |0> is an energy eigenstate so it only acquires a global phase e^{-i w0 t/2} over time, which has no observable effect. Without a transverse sigma_x driving field, there is no term to couple |0> and |1>, so the populations stay frozen at P0 = 1 and P1 = 0")

# ========================================================================
# TASK 2 — Resonant drive (wd = w0), Rabi oscillations
# ========================================================================
wd = w0 # TODO: Fill in resonance condition

Omega0 = 5
t2, P0_resonance, P1_resonance = run_sim(w0=w0, psi0=initial_state, Omega0=Omega0, wd=wd,
                                         t_max=15, n_points=6000)

plt.figure()
plt.plot(t2, P1_resonance)
plt.xlabel("time")
plt.ylabel("P1(t)")
plt.title("Task 2: Oscillations on resonance")
plt.savefig("task2_resonant_drive.png", dpi=150)

# TASK 2 Part 2 - Bit Flip Duration

# First time P1_resonance reaches its maximum (~1.0)
above = P1_resonance >= 0.9*P1_resonance.max()
start = np.argmax(above)
end = start +np.argmin(above[start:]) if not above[start:].all() else len(P1_resonance)
peak_idx = start + np.argmax(P1_resonance[start:end])
t_pi = t2[peak_idx]

print("TASK 2:")
print(f"Bit Flip Pulse duration: t_flip      = {t_pi:.4f}")
print(f"Theoretical Answer: t_flip           = {2*np.pi/Omega0:.4f}")
print("Peak value of P1:", np.max(P1_resonance))

# TODO: Explain what the Driving Pulse' Amplitude Signifies
# Clue - Try changing Omega0 and check what your plots produce
#print("Your Explanation")
print("The drive amplitude Omega0 controls the coupling strength between the qubit and the field, setting the speed of the Rabi oscillations. The bit-flip time is inversely proportional to it, t_flip = 2*pi/Omega0: doubling Omega0 halves the time needed to flip |0> to |1>. Because Omega0 is comparable to w0 here, counter-rotating terms cause small wiggles on top of the main oscillation so the first peak reaches P1 ~ 0.989 instead of exactly 1 and the simulated flip time differs slightly from the ideal theory")
