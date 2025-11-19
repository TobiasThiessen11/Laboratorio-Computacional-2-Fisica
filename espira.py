import numpy as np
from alambre import biot_savart, mu0

def campo_espira(I, a, N, r_puntos):
    thetas = np.linspace(0, 2*np.pi, N)
    dtheta = thetas[1] - thetas[0]

    B_total = np.zeros_like(r_puntos)

    for th in thetas:
        r_prima = np.array([a*np.cos(th), a*np.sin(th), 0])
        dl = np.array([-a*np.sin(th)*dtheta, a*np.cos(th)*dtheta, 0])
        B_total += biot_savart(I, r_puntos, r_prima, dl)

    return B_total
