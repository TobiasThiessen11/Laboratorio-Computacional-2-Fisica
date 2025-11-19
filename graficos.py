import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def graficar_2d(x, y, Bx, By, titulo="Campo Magnético", geometria=None):
    """
    Grafica campo magnético en 2D con vectores.
    
    Args:
        x, y: Mallas de coordenadas
        Bx, By: Componentes del campo
        titulo: Título del gráfico
        geometria: dict con 'tipo' ('alambre', 'espira', 'ambos') y parámetros
    """
    plt.figure(figsize=(8, 8))
    
    # Normalizar vectores para mejor visualización
    B_mag = np.sqrt(Bx**2 + By**2)
    B_mag_max = np.max(B_mag)
    if B_mag_max > 0:
        Bx_norm = Bx / B_mag_max
        By_norm = By / B_mag_max
    else:
        Bx_norm = Bx
        By_norm = By
    
    # Colorear por magnitud
    colors = B_mag
    plt.quiver(x, y, Bx_norm, By_norm, colors, cmap='viridis', scale=30)
    plt.colorbar(label='|B| (T)')
    
    # Dibujar geometría de la fuente
    if geometria:
        if geometria['tipo'] == 'alambre' or geometria['tipo'] == 'ambos':
            L = geometria.get('L', 2)
            plt.plot([0, 0], [-L/2, L/2], 'r-', linewidth=3, label='Alambre')
            plt.plot([0, 0], [-L/2, L/2], 'ro', markersize=8)
        
        if geometria['tipo'] == 'espira' or geometria['tipo'] == 'ambos':
            a = geometria.get('a', 0.5)
            theta = np.linspace(0, 2*np.pi, 100)
            plt.plot(a*np.cos(theta), a*np.sin(theta), 'b-', linewidth=3, label='Espira')
    
    plt.title(titulo)
    plt.axis('equal')
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.grid(True, alpha=0.3)
    if geometria:
        plt.legend()
    plt.show()

def graficar_3d(x, y, z, Bx, By, Bz, titulo="Campo Magnético 3D", geometria=None):
    """
    Grafica campo magnético en 3D con vectores.
    
    Args:
        x, y, z: Coordenadas de los puntos
        Bx, By, Bz: Componentes del campo
        titulo: Título del gráfico
        geometria: dict con 'tipo' ('alambre', 'espira', 'ambos') y parámetros
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Normalizar vectores
    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
    B_mag_max = np.max(B_mag)
    if B_mag_max > 0:
        Bx_norm = Bx / B_mag_max
        By_norm = By / B_mag_max
        Bz_norm = Bz / B_mag_max
    else:
        Bx_norm = Bx
        By_norm = By
        Bz_norm = Bz
    
    # Quiver plot con colores
    colors = B_mag.flatten()
    q = ax.quiver(x, y, z, Bx_norm, By_norm, Bz_norm, 
                  length=0.15, normalize=False, 
                  cmap='viridis', linewidth=1.5)
    
    # Dibujar geometría
    if geometria:
        if geometria['tipo'] == 'alambre' or geometria['tipo'] == 'ambos':
            L = geometria.get('L', 2)
            zs = np.linspace(-L/2, L/2, 50)
            ax.plot([0]*len(zs), [0]*len(zs), zs, 'r-', linewidth=3, label='Alambre')
        
        if geometria['tipo'] == 'espira' or geometria['tipo'] == 'ambos':
            a = geometria.get('a', 0.5)
            theta = np.linspace(0, 2*np.pi, 100)
            ax.plot(a*np.cos(theta), a*np.sin(theta), [0]*len(theta), 
                   'b-', linewidth=3, label='Espira')
    
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    ax.set_title(titulo)
    if geometria:
        ax.legend()
    plt.show()
