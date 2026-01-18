import pytest
from unittest.mock import Mock, patch


@pytest.fixture
def mock_panda3d():
    """Fixture to mock Panda3D components for testing."""
    with patch('panda3d.core.loadPrcFileData'), \
         patch('direct.showbase.ShowBase'), \
         patch('panda3d.core.ClockObject'):
        yield


@pytest.fixture
def mock_simulator():
    """Fixture providing a mock simulator for UI testing."""
    simulator = Mock()
    simulator.taskMgr = Mock()
    simulator.taskMgr.add = Mock()
    simulator.simulation_time = 0.0
    simulator.simulation_speed = 1.0
    simulator.paused = False
    simulator.max_speed = 50.0
    simulator.min_speed = 0.1
    simulator.speed_increment = 1.0
    simulator.particles = []
    simulator.time_since_last_spawn = 0
    simulator.initial_grid_size = 50
    simulator.create_grid = Mock()
    simulator.create_initial_particles = Mock()
    return simulator