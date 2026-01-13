import unittest
from messages.greeting.Greetings import generar_array

from messages.greeting.Greetings import *# greeting, Greeting
from messages.farewell.Farewell import *# farewell, Farewell

class PruebasHola(unittest.TestCase):

    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0, 1, 2, 3, 4, 5]),
            generar_array(6)
        )

greeting()
Greeting()

farewell()
Farewell()