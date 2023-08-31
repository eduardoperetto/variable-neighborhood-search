import unittest
from main import ProblemInstance, minimize_k_related_subset

class TestVNSSolution(unittest.TestCase):
    def test_example_instance(self):
        instance = ProblemInstance(nodes=range(1,15), k=3, p=1, edges=[(1, 2), (1, 10), (1, 9), (1, 3), (1, 8), (2, 11), (2, 3), (3, 11), (3, 4), (4, 12), (4, 5), (5, 12), (5, 6), (6, 12), (6, 13), (6, 7), (7, 13), (7, 14), (7, 8), (8, 9), (8, 14), (9, 10), (10, 11), (10, 13), (10, 14), (11, 12), (11, 13), (12, 13), (13, 14)])
        solution, _ = minimize_k_related_subset(instance, num_neighborhoods=10)
        expectedSolution = [6, 7, 10, 11, 12, 13, 14]
        self.assertEqual(solution, expectedSolution)

if __name__ == '__main__':
    unittest.main()
