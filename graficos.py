import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graficar_2d(x, y, Bx, By, titulo="Campo Magnético"):
    plt.figure(figsize=(6,6))
    plt.quiver(x, y, Bx, By)
    plt.title(titulo)
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

def graficar_3d(x, y, z, Bx, By, Bz, titulo="Campo Magnético 3D"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(x, y, z, Bx, By, Bz, length=0.1)
    ax.set_title(titulo)
    plt.show()
