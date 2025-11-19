import numpy as np
import unittest
from alambre import campo_alambre, mu0
from espira import campo_espira

class TestBiotSavart(unittest.TestCase):

    def test_alambre_infinito(self):
        # Caso teórico: Alambre infinito
        # B = mu0 * I / (2 * pi * r)
        # Usamos un alambre muy largo para aproximar
        I = 10.0
        L = 20.0 # Suficientemente largo para r=0.1
        r_dist = 0.1 # Cerca del centro
        
        # Punto de prueba en el eje x a distancia r_dist
        r_puntos = np.array([[r_dist, 0, 0]])
        
        # dz = 20 / 10000 = 0.002, que es << 0.1
        B_calc = campo_alambre(I, L, 10000, r_puntos)
        B_mag_calc = np.linalg.norm(B_calc)
        
        B_teorico = (mu0 * I) / (2 * np.pi * r_dist)
        
        # El campo debe ser en dirección +y (regla mano derecha, corriente en +z)
        # Esperamos B = [0, B_mag, 0]
        
        print(f"\nAlambre Infinito (aprox): Calc={B_mag_calc:.2e}, Teorico={B_teorico:.2e}")
        
        # Tolerancia del 1% debido a la aproximación finita
        self.assertTrue(np.isclose(B_mag_calc, B_teorico, rtol=0.01))
        self.assertTrue(np.isclose(B_calc[0, 0], 0)) # Bx ~ 0
        self.assertTrue(B_calc[0, 1] > 0)            # By > 0

    def test_espira_eje(self):
        # Caso teórico: Eje de la espira
        # B = (mu0 * I * a^2) / (2 * (a^2 + z^2)^(3/2))
        I = 5.0
        a = 0.5
        z = 0.5
        
        r_puntos = np.array([[0, 0, z]])
        
        B_calc = campo_espira(I, a, 1000, r_puntos)
        B_mag_calc = np.linalg.norm(B_calc)
        
        B_teorico = (mu0 * I * a**2) / (2 * (a**2 + z**2)**(1.5))
        
        print(f"Espira Eje: Calc={B_mag_calc:.2e}, Teorico={B_teorico:.2e}")
        
        self.assertTrue(np.isclose(B_mag_calc, B_teorico, rtol=0.01))
        # Campo debe ser en +z
        self.assertTrue(np.isclose(B_calc[0, 0], 0))
        self.assertTrue(np.isclose(B_calc[0, 1], 0))
        self.assertTrue(B_calc[0, 2] > 0)

if __name__ == '__main__':
    unittest.main()
