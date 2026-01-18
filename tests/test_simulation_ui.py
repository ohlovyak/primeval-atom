import pytest
from unittest.mock import Mock, patch, MagicMock


class TestSimulationUI:
    """Test cases for the SimulationUI class."""

    def test_initialization(self):
        """Test that SimulationUI initializes correctly."""
        from simulation_ui import SimulationUI

        # Mock simulator
        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.taskMgr.add = Mock()

        # Create UI
        ui = SimulationUI(mock_simulator)

        # Verify UI was set up
        assert ui.simulator == mock_simulator
        assert ui.ui_text is not None

        # Verify input was set up
        mock_simulator.accept.assert_any_call('arrow_up', ui.increase_speed)
        mock_simulator.accept.assert_any_call('arrow_down', ui.decrease_speed)
        mock_simulator.accept.assert_any_call('r', ui.reset_simulation)
        mock_simulator.accept.assert_any_call('p', ui.toggle_pause)

        # Verify UI update task was added
        mock_simulator.taskMgr.add.assert_called_once()

    def test_setup_ui(self):
        """Test UI element setup."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()

        with patch('simulation_ui.OnscreenText') as mock_text:
            ui = SimulationUI(mock_simulator)

            # Verify OnscreenText was created with correct parameters
            mock_text.assert_called_once()
            call_args = mock_text.call_args
            assert call_args[1]['text'] == "Time: 0.00s | Speed: 1.0x"
            assert call_args[1]['pos'] == (-0.8, -0.75)
            assert call_args[1]['scale'] == 0.07
            assert call_args[1]['fg'] == (1, 1, 1, 1)
            assert call_args[1]['mayChange'] == True

    def test_update_ui_task(self):
        """Test UI update task."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()

        ui = SimulationUI(mock_simulator)
        mock_task = Mock()
        mock_task.cont = "cont"

        with patch.object(ui, 'update_ui_text') as mock_update:
            result = ui.update_ui_task(mock_task)

            mock_update.assert_called_once()
            assert result == "cont"

    def test_update_ui_text_running(self):
        """Test UI text update when simulation is running."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.simulation_time = 123.456
        mock_simulator.simulation_speed = 2.5
        mock_simulator.paused = False

        ui = SimulationUI(mock_simulator)

        # Mock the setText method
        ui.ui_text.setText = Mock()

        ui.update_ui_text()

        # Verify correct text was set
        ui.ui_text.setText.assert_called_once_with(
            "Time: 123.46s | Speed: 2.5x | Status: Running\n"
            "Controls: Up/Down Arrows (Speed), R (Reset), P (Pause)"
        )

    def test_update_ui_text_paused(self):
        """Test UI text update when simulation is paused."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.simulation_time = 0.0
        mock_simulator.simulation_speed = 1.0
        mock_simulator.paused = True

        ui = SimulationUI(mock_simulator)
        ui.ui_text.setText = Mock()

        ui.update_ui_text()

        ui.ui_text.setText.assert_called_once_with(
            "Time: 0.00s | Speed: 1.0x | Status: Paused\n"
            "Controls: Up/Down Arrows (Speed), R (Reset), P (Pause)"
        )

    def test_increase_speed_within_limits(self):
        """Test speed increase within limits."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.simulation_speed = 5.0
        mock_simulator.max_speed = 10.0
        mock_simulator.speed_increment = 2.0

        ui = SimulationUI(mock_simulator)

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.increase_speed()

            assert mock_simulator.simulation_speed == 7.0
            mock_update_text.assert_called_once()

    def test_increase_speed_at_max(self):
        """Test speed increase when already at max."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.simulation_speed = 10.0
        mock_simulator.max_speed = 10.0
        mock_simulator.speed_increment = 2.0

        ui = SimulationUI(mock_simulator)

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.increase_speed()

            assert mock_simulator.simulation_speed == 10.0  # Should not exceed max
            mock_update_text.assert_called_once()

    def test_decrease_speed_within_limits(self):
        """Test speed decrease within limits."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.simulation_speed = 5.0
        mock_simulator.min_speed = 0.1
        mock_simulator.speed_increment = 2.0

        ui = SimulationUI(mock_simulator)

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.decrease_speed()

            assert mock_simulator.simulation_speed == 3.0
            mock_update_text.assert_called_once()

    def test_decrease_speed_at_min(self):
        """Test speed decrease when already at min."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.simulation_speed = 0.1
        mock_simulator.min_speed = 0.1
        mock_simulator.speed_increment = 2.0

        ui = SimulationUI(mock_simulator)

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.decrease_speed()

            assert mock_simulator.simulation_speed == 0.1  # Should not go below min
            mock_update_text.assert_called_once()

    def test_reset_simulation(self):
        """Test simulation reset functionality."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.particles = [Mock(), Mock(), Mock()]  # 3 mock particles
        mock_simulator.simulation_time = 100.0
        mock_simulator.time_since_last_spawn = 50.0
        mock_simulator.paused = True
        mock_simulator.initial_grid_size = 25

        ui = SimulationUI(mock_simulator)

        # Mock the methods that should be called
        mock_simulator.particles[0].removeNode = Mock()
        mock_simulator.particles[1].removeNode = Mock()
        mock_simulator.particles[2].removeNode = Mock()
        mock_simulator.create_grid = Mock()
        mock_simulator.create_initial_particles = Mock()

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.reset_simulation()

            # Verify particles were removed
            for particle in mock_simulator.particles:
                particle.removeNode.assert_called_once()

            # Verify simulation state was reset
            assert mock_simulator.particles == []
            assert mock_simulator.simulation_time == 0.0
            assert mock_simulator.time_since_last_spawn == 0
            assert mock_simulator.paused == False

            # Verify grid and particles were recreated
            mock_simulator.create_grid.assert_called_once_with(25)
            mock_simulator.create_initial_particles.assert_called_once()
            mock_update_text.assert_called_once()

    def test_toggle_pause_from_running(self):
        """Test pause toggle from running state."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.paused = False

        ui = SimulationUI(mock_simulator)

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.toggle_pause()

            assert mock_simulator.paused == True
            mock_update_text.assert_called_once()

    def test_toggle_pause_from_paused(self):
        """Test pause toggle from paused state."""
        from simulation_ui import SimulationUI

        mock_simulator = Mock()
        mock_simulator.taskMgr = Mock()
        mock_simulator.paused = True

        ui = SimulationUI(mock_simulator)

        with patch.object(ui, 'update_ui_text') as mock_update_text:
            ui.toggle_pause()

            assert mock_simulator.paused == False
            mock_update_text.assert_called_once()