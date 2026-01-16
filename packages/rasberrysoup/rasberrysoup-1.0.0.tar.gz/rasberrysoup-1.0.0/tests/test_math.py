import unittest
from rasberrysoup import quad, gold, dist, fourier, interest

class TestRasberrysoup(unittest.TestCase):

    def test_quad(self):
        # x^2 - 5x + 6 = 0 -> x=2, 3
        roots = quad(1, -5, 6)
        self.assertIn(complex(3, 0), roots)
        self.assertIn(complex(2, 0), roots)
        
        # x^2 + 1 = 0 -> x=i, -i
        roots2 = quad(1, 0, 1)
        self.assertIn(complex(0, 1), roots2)
        self.assertIn(complex(0, -1), roots2)

    def test_gold(self):
        self.assertAlmostEqual(gold(), 1.618033988749895)

    def test_dist(self):
        # 3-4-5 triangle
        self.assertEqual(dist([0, 0], [3, 4]), 5.0)
        # 3D distance
        self.assertAlmostEqual(dist([0, 0, 0], [1, 1, 1]), math.sqrt(3))

    def test_interest(self):
        # 1000 at 5% for 2 periods
        self.assertAlmostEqual(interest(1000, 0.05, 2), 1102.5)

    def test_fourier(self):
        # Simple test with [1, 0, 0, 0]
        data = [1, 0, 0, 0]
        result = fourier(data)
        # DFT of [1, 0, 0, 0] is [1, 1, 1, 1]
        for val in result:
            self.assertAlmostEqual(val.real, 1.0)
            self.assertAlmostEqual(val.imag, 0.0)

if __name__ == '__main__':
    import math
    unittest.main()
