import numpy as np
from alambre import campo_alambre
from espira import campo_espira
from graficos import graficar_2d, graficar_3d

# ============================================================================
# PARÁMETROS DE LA SIMULACIÓN
# ============================================================================
I_alambre = 10.0  # Corriente en el alambre (A)
L_alambre = 2.0   # Longitud del alambre (m)
I_espira = 5.0    # Corriente en la espira (A)
a_espira = 0.5    # Radio de la espira (m)

# Punto específico para cálculo algebraico
punto_test = np.array([[0.3, 0.0, 0.2]])

print("="*70)
print("LABORATORIO COMPUTACIONAL 3: LEY DE BIOT-SAVART")
print("="*70)
print(f"\nParámetros:")
print(f"  Alambre: I = {I_alambre} A, L = {L_alambre} m")
print(f"  Espira:  I = {I_espira} A, a = {a_espira} m")
print(f"  Punto de prueba: ({punto_test[0,0]}, {punto_test[0,1]}, {punto_test[0,2]}) m")

# ============================================================================
# 1. CAMPO MAGNÉTICO DEL ALAMBRE RECTO
# ============================================================================
print("\n" + "-"*70)
print("1. CAMPO MAGNÉTICO DEL ALAMBRE RECTO")
print("-"*70)

# --- Malla 2D en el plano XY (z=0) ---
x_2d = np.linspace(-1, 1, 20)
y_2d = np.linspace(-1, 1, 20)
xx_2d, yy_2d = np.meshgrid(x_2d, y_2d)
r_2d = np.c_[xx_2d.ravel(), yy_2d.ravel(), np.zeros_like(xx_2d).ravel()]

B_alambre_2d = campo_alambre(I_alambre, L_alambre, 1000, r_2d)
Bx_2d = B_alambre_2d[:, 0].reshape(xx_2d.shape)
By_2d = B_alambre_2d[:, 1].reshape(yy_2d.shape)

# --- Malla 3D ---
x_3d = np.linspace(-1, 1, 8)
y_3d = np.linspace(-1, 1, 8)
z_3d = np.linspace(-1, 1, 8)
xx_3d, yy_3d, zz_3d = np.meshgrid(x_3d, y_3d, z_3d)
r_3d = np.c_[xx_3d.ravel(), yy_3d.ravel(), zz_3d.ravel()]

B_alambre_3d = campo_alambre(I_alambre, L_alambre, 1000, r_3d)
Bx_3d = B_alambre_3d[:, 0]
By_3d = B_alambre_3d[:, 1]
Bz_3d = B_alambre_3d[:, 2]

# --- Cálculo en punto específico ---
B_alambre_punto = campo_alambre(I_alambre, L_alambre, 2000, punto_test)
print(f"\nCampo magnético en {punto_test[0]}:")
print(f"  B_alambre = ({B_alambre_punto[0,0]:.6e}, {B_alambre_punto[0,1]:.6e}, {B_alambre_punto[0,2]:.6e}) T")
print(f"  |B_alambre| = {np.linalg.norm(B_alambre_punto):.6e} T")

# --- Gráficos ---
print("\nGenerando gráficos 2D y 3D del alambre...")
graficar_2d(xx_2d, yy_2d, Bx_2d, By_2d, 
            titulo="Campo Magnético - Alambre Recto (Plano XY, z=0)",
            geometria={'tipo': 'alambre', 'L': L_alambre})

graficar_3d(xx_3d.ravel(), yy_3d.ravel(), zz_3d.ravel(), 
            Bx_3d, By_3d, Bz_3d,
            titulo="Campo Magnético 3D - Alambre Recto",
            geometria={'tipo': 'alambre', 'L': L_alambre})

# ============================================================================
# 2. CAMPO MAGNÉTICO DE LA ESPIRA CIRCULAR
# ============================================================================
print("\n" + "-"*70)
print("2. CAMPO MAGNÉTICO DE LA ESPIRA CIRCULAR")
print("-"*70)

# --- 2D ---
B_espira_2d = campo_espira(I_espira, a_espira, 1000, r_2d)
Bx_espira_2d = B_espira_2d[:, 0].reshape(xx_2d.shape)
By_espira_2d = B_espira_2d[:, 1].reshape(yy_2d.shape)

# --- 3D ---
B_espira_3d = campo_espira(I_espira, a_espira, 1000, r_3d)
Bx_espira_3d = B_espira_3d[:, 0]
By_espira_3d = B_espira_3d[:, 1]
Bz_espira_3d = B_espira_3d[:, 2]

# --- Punto específico ---
B_espira_punto = campo_espira(I_espira, a_espira, 2000, punto_test)
print(f"\nCampo magnético en {punto_test[0]}:")
print(f"  B_espira = ({B_espira_punto[0,0]:.6e}, {B_espira_punto[0,1]:.6e}, {B_espira_punto[0,2]:.6e}) T")
print(f"  |B_espira| = {np.linalg.norm(B_espira_punto):.6e} T")

# --- Gráficos ---
print("\nGenerando gráficos 2D y 3D de la espira...")
graficar_2d(xx_2d, yy_2d, Bx_espira_2d, By_espira_2d, 
            titulo="Campo Magnético - Espira Circular (Plano XY, z=0)",
            geometria={'tipo': 'espira', 'a': a_espira})

graficar_3d(xx_3d.ravel(), yy_3d.ravel(), zz_3d.ravel(), 
            Bx_espira_3d, By_espira_3d, Bz_espira_3d,
            titulo="Campo Magnético 3D - Espira Circular",
            geometria={'tipo': 'espira', 'a': a_espira})

# ============================================================================
# 3. SUPERPOSICIÓN: ALAMBRE + ESPIRA
# ============================================================================
print("\n" + "-"*70)
print("3. SUPERPOSICIÓN: ALAMBRE + ESPIRA")
print("-"*70)
print("(El alambre está ubicado en el eje de la espira)")

# --- 2D ---
B_total_2d = B_alambre_2d + B_espira_2d
Bx_total_2d = B_total_2d[:, 0].reshape(xx_2d.shape)
By_total_2d = B_total_2d[:, 1].reshape(yy_2d.shape)

# --- 3D ---
B_total_3d = B_alambre_3d + B_espira_3d
Bx_total_3d = B_total_3d[:, 0]
By_total_3d = B_total_3d[:, 1]
Bz_total_3d = B_total_3d[:, 2]

# --- Punto específico ---
B_total_punto = B_alambre_punto + B_espira_punto
print(f"\nCampo magnético total en {punto_test[0]}:")
print(f"  B_total = ({B_total_punto[0,0]:.6e}, {B_total_punto[0,1]:.6e}, {B_total_punto[0,2]:.6e}) T")
print(f"  |B_total| = {np.linalg.norm(B_total_punto):.6e} T")

# --- Gráficos ---
print("\nGenerando gráficos 2D y 3D de la superposición...")
graficar_2d(xx_2d, yy_2d, Bx_total_2d, By_total_2d, 
            titulo="Campo Magnético - Superposición (Alambre + Espira)",
            geometria={'tipo': 'ambos', 'L': L_alambre, 'a': a_espira})

graficar_3d(xx_3d.ravel(), yy_3d.ravel(), zz_3d.ravel(), 
            Bx_total_3d, By_total_3d, Bz_total_3d,
            titulo="Campo Magnético 3D - Superposición (Alambre + Espira)",
            geometria={'tipo': 'ambos', 'L': L_alambre, 'a': a_espira})

print("\n" + "="*70)
print("¡Simulación completada!")
print("="*70)

