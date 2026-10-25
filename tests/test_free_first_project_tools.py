import unittest
from scripts.free_first_project_tools import simulate_search_scenario

class FreeFirstTests(unittest.TestCase):
    def test_deterministic_coverage_avoids_obstacles(self):
        agents=[{"id":"drone","cell":(0,0)},{"id":"boat","cell":(1,0)},{"id":"ground","cell":(1,1)}]
        result=simulate_search_scenario(2,2,agents,{(1,1)})
        self.assertEqual(result["visited"], [[0,0],[1,0]])
        self.assertEqual(result["coverage"], 2/3)
        self.assertEqual(result,simulate_search_scenario(2,2,agents,{(1,1)}))

    def test_communication_loss_enters_safe_hold(self):
        result=simulate_search_scenario(4,4,[{"cell":(1,1)}],set(),False)
        self.assertEqual(result["status"],"safe_hold")
        self.assertEqual(result["coverage"],0.0)

    def test_invalid_agent_cell_is_ignored(self):
        result=simulate_search_scenario(2,2,[{"cell":("bad",1)},{"cell":(0,0)}],set())
        self.assertEqual(result["accepted_agents"],1)

    def test_invalid_grid_rejected(self):
        with self.assertRaises(ValueError): simulate_search_scenario(0,2,[],set())

if __name__ == "__main__": unittest.main()
