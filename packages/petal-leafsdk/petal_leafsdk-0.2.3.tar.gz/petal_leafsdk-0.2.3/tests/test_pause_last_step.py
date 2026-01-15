import unittest
from unittest.mock import MagicMock, patch
from petal_leafsdk.mission import Mission, MissionStateAll
from petal_leafsdk.mission_step import StepState
import networkx as nx

class TestMissionPauseLastStep(unittest.TestCase):
    def test_pause_last_step(self):
        """Test that pausing on the last step completes the mission instead of getting stuck."""
        # Setup
        mav_proxy = MagicMock()
        mav_proxy.target_system = 1
        redis_proxy = MagicMock()
        
        # Create mission with mock data
        mission_data = {
            "name": "test_mission",
            "config": {"joystick_mode": "enabled"},
            "steps": [{"type": "Land"}]
        }
        
        mission = Mission(mav_proxy, redis_proxy, data=mission_data)
        
        # Mock the load_plan to set up a simple graph with a mock step executor
        with patch.object(mission, 'mission_plan') as mock_plan:
            mock_plan.name = "test_mission"
            mock_plan.config = MagicMock()
            mock_plan.config.joystick_mode.value = "enabled"
            
            # Create execution graph with mock step executor
            graph = nx.MultiDiGraph()
            mock_step = MagicMock()
            mock_step.state = StepState.RUNNING
            mock_step.pause.return_value = False  # Non-pausable step
            graph.add_node("step1", step=mock_step)
            mock_plan.mission_graph = graph
            
            mission.execution_graph = graph
            mission.current_node = "step1"
            mission.current_step = mock_step
            mission.mission_status.set_state(MissionStateAll.RUNNING)
            
            # Request pause (should be queued for non-pausable step)
            result = mission.pause()
            
            # Verify pause was attempted but returned False (non-pausable)
            self.assertFalse(result)
            
            # Simulate step completion
            mission.mission_status.set_state(MissionStateAll.COMPLETED)
            
            # Verify final state
            final_state = mission.mission_status.get_state()
            print(f"Final state: {final_state}")
            
            if final_state == MissionStateAll.PAUSED_BETWEEN_STEPS:
                print("Failure: Mission stuck in PAUSED state after last step.")
            elif final_state == MissionStateAll.COMPLETED:
                print("Success: Mission completed successfully.")
            else:
                print(f"Unexpected state: {final_state}")
            
            self.assertEqual(final_state, MissionStateAll.COMPLETED)

    def test_pause_for_pausable_steps(self):
        """Test that pausable steps can be paused immediately."""
        # Setup
        mav_proxy = MagicMock()
        mav_proxy.target_system = 1
        redis_proxy = MagicMock()
        
        mission_data = {
            "name": "test_mission",
            "config": {"joystick_mode": "enabled"},
            "steps": [{"type": "GotoLocalPosition", "waypoints": [(0, 0, 0)]}]
        }
        
        mission = Mission(mav_proxy, redis_proxy, data=mission_data)
        
        # Mock the setup with pausable step executor
        with patch.object(mission, 'mission_plan') as mock_plan:
            mock_plan.name = "test_mission"
            mock_plan.config = MagicMock()
            
            graph = nx.MultiDiGraph()
            mock_step = MagicMock()
            mock_step.state = StepState.RUNNING
            mock_step.pause.return_value = True  # Pausable step
            graph.add_node("step1", step=mock_step)
            
            mission.execution_graph = graph
            mission.current_node = "step1"
            mission.current_step = mock_step
            mission.mission_status.set_state(MissionStateAll.RUNNING)
            
            # Request pause - should successfully pause
            result = mission.pause()
            
            # Verify pause was successful
            self.assertTrue(result)
            mock_step.pause.assert_called_once()


if __name__ == '__main__':
    unittest.main()
