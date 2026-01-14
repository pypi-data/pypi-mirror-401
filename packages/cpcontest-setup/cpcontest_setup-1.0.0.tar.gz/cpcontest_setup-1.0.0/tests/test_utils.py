import unittest
import os
import tempfile
from cpcontest.utils.template import crear_datos_reemplazo_standard


class TestUtils(unittest.TestCase):
    
    def test_crear_datos_reemplazo(self):
        """Test creación de datos de reemplazo"""
        datos = crear_datos_reemplazo_standard("A")
        self.assertIn("$%U%$", datos)
        self.assertIn("$%file%$", datos)
        self.assertEqual(datos["$%file%$"], "A")


if __name__ == "__main__":
    unittest.main()