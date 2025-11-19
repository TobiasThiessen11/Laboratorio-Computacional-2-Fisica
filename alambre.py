import numpy as np

mu0 = 4 * np.pi * 1e-7

def biot_savart(I, r_puntos, r_prima, dl):
    R = r_puntos - r_prima
    R_norm = np.linalg.norm(R, axis=1).reshape(-1, 1)
    dB = mu0 * I / (4*np.pi) * np.cross(dl, R) / (R_norm**3)
    return dB

def campo_alambre(I, L, N, r_puntos):
    # Alambre centrado en z, desde -L/2 hasta L/2
    zs = np.linspace(-L/2, L/2, N)
    dz = zs[1] - zs[0]
    dl = np.array([0, 0, dz])

    B_total = np.zeros_like(r_puntos)

    for z in zs:
        r_prima = np.array([0, 0, z])
        B_total += biot_savart(I, r_puntos, r_prima, dl)

    return B_total
