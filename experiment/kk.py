import numpy as np
import matplotlib.pyplot as plt

def initial(x):
    return 1.

def get_precise_solution(k, l, t, x):
    u = np.zeros_like(x)
    for m in range(10):
        u += 4/np.pi * np.exp(-k*np.pi**2*(2*m+1)**2*t/l**2) / (2*m+1) * np.sin(np.pi * (2*m+1) * x / l)

    return u

T, l, k, n, h, dt = 1e-2, 1, 1, 50, 1 / n, 2e-4


fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.set_title('Зависимость температуры от времени')
ax.set_xlabel('x')
ax.set_ylabel('t')

x = np.arange(0, l + h / 2, h)
u = np.zeros(len(x))
u[1:-1] = initial(x[1:-1])
u[0] = u[-1] = 0

M = (-2 * np.diag(np.ones(len(x))) + np.diag(np.ones(len(x) - 1), 1) + np.diag(np.ones(len(x) - 1), -1)) * k * dt / h ** 2
M[0, 0], M[0, 1] = 0, 0
M[-1, -1], M[-1, -2] = 0, 0

M += np.eye(M.shape[0])
# условие Куранта
dt = min(dt, h**2/k)

tc = 0
while tc < T + dt/2:
    # ax.plot(xs, u, label=f't={t:g}')
    u = np.dot(M, u)
    tc += dt
    
ax.plot(x, u, label='Численное решение')
u_pr = get_precise_solution(k, l, T, x)
ax.plot(x, u_pr, label='Фурье-решение')

ax.legend()
ax.grid()

plt.show()