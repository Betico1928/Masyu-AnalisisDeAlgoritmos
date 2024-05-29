import unittest
import tkinter as tk
from unittest.mock import patch
from io import StringIO
from masyu import Masyu, leer_archivo_entrada, verificar_solucion, verificar_linea_continua, verificar_perla_blanca, \
    verificar_perla_negra
from io import StringIO


class TestMasyu(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.update()
        self.root.destroy()

    def test_leer_archivo_entrada(self):
        # Simulamos un archivo de prueba con datos ficticios
        input_data = "5\n2,2,1\n4,4,2\n"
        with patch('builtins.open', return_value=StringIO(input_data)) as mock_file:
            n_filas, n_columnas, perlas = leer_archivo_entrada('test_input.txt')
            mock_file.assert_called_once_with('test_input.txt', 'r')
            self.assertEqual(n_filas, 5)
            self.assertEqual(n_columnas, 5)
            self.assertEqual(perlas, [(2, 2, 1), (4, 4, 2)])

    @patch('sys.stdout', new_callable=StringIO)
    def test_imprimir_ruta(self, mock_stdout):
        juego = Masyu(self.root, 5, 5, [(2, 2, 1), (4, 4, 2)])
        juego.linea_actual = [(1, 1), (1, 2), (1, 3)]
        juego.imprimir_ruta()
        self.assertEqual(mock_stdout.getvalue().strip(), "Ruta actual: [(1, 1), (1, 2), (1, 3)]")

    def test_verificar_solucion_incorrecta(self):
        linea = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 2)]
        perlas = [(2, 2, 1), (4, 4, 2)]
        es_correcto, errores = verificar_solucion(linea, perlas)
        self.assertFalse(es_correcto)

    def test_verificar_linea_continua(self):
        # Caso de prueba con línea continua
        linea_continua = [(1, 1), (1, 2), (1, 3)]
        self.assertTrue(verificar_linea_continua(linea_continua))

        # Caso de prueba con línea no continua
        linea_no_continua = [(1, 1), (2, 2), (3, 3)]
        self.assertFalse(verificar_linea_continua(linea_no_continua))

    def test_verificar_perla_blanca(self):
        # Caso de prueba con línea que pasa por perla blanca de forma recta con giros
        linea_correcta = [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
        fila_perla = 2
        columna_perla = 2
        self.assertTrue(verificar_perla_blanca(linea_correcta, fila_perla, columna_perla))

        # Caso de prueba con línea que no pasa por perla blanca de forma correcta
        linea_incorrecta = [(1, 1), (1, 2), (1, 3)]
        self.assertFalse(verificar_perla_blanca(linea_incorrecta, fila_perla, columna_perla))

    def test_verificar_perla_negra(self):
        # Caso de prueba con línea que hace un giro de 90 grados en perla negra
        linea_correcta = [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
        fila_perla = 2
        columna_perla = 2
        self.assertTrue(verificar_perla_negra(linea_correcta, fila_perla, columna_perla))

        # Caso de prueba con línea que no hace un giro de 90 grados en perla negra
        linea_incorrecta = [(1, 1), (1, 2), (1, 3)]
        self.assertFalse(verificar_perla_negra(linea_incorrecta, fila_perla, columna_perla))


if __name__ == '__main__':
    unittest.main()