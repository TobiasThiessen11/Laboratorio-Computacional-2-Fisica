import numpy as np
from alambre import campo_alambre
from espira import campo_espira
from graficos import graficar_2d

# Malla de puntos
x = np.linspace(-1, 1, 20)
y = np.linspace(-1, 1, 20)
xx, yy = np.meshgrid(x, y)

# Convertir a puntos (x,y,z)
r = np.c_[xx.ravel(), yy.ravel(), np.zeros_like(xx).ravel()]

# ---- Campo del alambre ----
B_alambre = campo_alambre(I=1, L=2, N=600, r_puntos=r)

# ---- Campo de la espira ----
B_espira = campo_espira(I=1, a=0.5, N=800, r_puntos=r)

# ---- Campo total ----
B = B_alambre + B_espira

# Para graficar 2D
Bx = B[:,0].reshape(xx.shape)
By = B[:,1].reshape(yy.shape)

graficar_2d(xx, yy, Bx, By, titulo="Campo Magnético Total (Alambre + Espira)")
