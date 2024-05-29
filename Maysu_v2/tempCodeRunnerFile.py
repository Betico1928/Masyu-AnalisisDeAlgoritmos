from masyu import verificar_perla_negra


def test_verificar_perla_negra(self):
    # Caso de prueba con línea que hace un giro de 90 grados en perla negra
    linea_correcta = [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
    fila_perla = 2
    columna_perla = 2
    self.assertTrue(verificar_perla_negra(linea_correcta, fila_perla, columna_perla))

    # Caso de prueba con línea que no hace un giro de 90 grados en perla negra
    linea_incorrecta = [(1, 1), (1, 2), (1, 3)]
    self.assertFalse(verificar_perla_negra(linea_incorrecta, fila_perla, columna_perla))

    # Caso de prueba con línea que no ocupa los espacios anterior y posterior en el camino del ciclo
    linea_incorrecta2 = [(1, 1), (1, 2), (2, 2), (3, 3)]
    self.assertFalse(verificar_perla_negra(linea_incorrecta2, fila_perla, columna_perla))