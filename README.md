# The Primeval Atom

A real-time 3D visualization of the Big Bang and cosmic expansion, built with Panda3D.

## Overview

"The Primeval Atom" is an interactive simulation that visualizes the early moments of the universe's expansion immediately following the Big Bang. The project represents fundamental particles and energy as colored spheres that expand outward from a central point, demonstrating the rapid inflation and expansion of the universe.

## Features

### Current Implementation

- **3D Particle System**: Different colored particles represent various types of matter and energy:
  - Orange particles (Type 1): High-energy particles
  - Blue particles (Type 2): Medium-energy particles
  - Purple particles (Type 3): Exotic matter
  - Green particles (Type 4): Standard matter

- **Dynamic Grid**: An expanding 3D grid that grows automatically as particles reach the boundaries, representing the expanding space of the universe

- **Real-time Simulation**: Continuous particle spawning and expansion with adjustable time controls

- **Interactive Controls**:
  - **Up/Down Arrow Keys**: Increase/decrease simulation speed (0.1x to 50x)
  - **P Key**: Pause/unpause the simulation
  - **R Key**: Reset the simulation to initial state

- **Visual Features**:
  - Radial gradient textures for particle appearance
  - Ambient and directional lighting
  - On-screen UI displaying simulation time, speed, and status
  - Black space-like background

## Technical Details

- **Engine**: Panda3D 3D graphics engine
- **Language**: Python
- **Window Size**: 1600x1200 (configurable)
- **Particle Count**: Starts with 20 particles, continuously spawns more
- **Grid System**: Adaptive grid that expands when particles reach 80% of current boundaries

## Installation & Running

### Prerequisites
- Python 3.x
- Panda3D library

### Setup
1. Ensure you have a Python virtual environment with Panda3D installed
2. Install testing dependencies (optional):
   ```bash
   pip install -e .[dev]
   ```
3. Run the simulation:
   ```bash
   python main.py
   ```

### Testing

The project includes comprehensive unit tests using pytest with coverage reporting.

#### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage report
python -m pytest --cov-report=html

# Run specific test file
python -m pytest tests/test_bigbang_simulator.py

# Run specific test
python -m pytest tests/test_simulation_ui.py::TestSimulationUI::test_initialization -v
```

#### Test Coverage

The project achieves **100% coverage** of the core UI and control logic, with comprehensive testing of all user-facing functionality. Panda3D graphics initialization code is excluded from coverage as it involves complex global state management that's difficult to test reliably.

#### Test Structure

- `tests/test_simulation_ui.py` - **100% coverage** of UI controls and state management (15 tests)
- `tests/test_main.py` - Tests for main entry point structure
- `tests/test_integration.py` - Integration tests for module imports and system components

## Physics Interpretation

The simulation represents a simplified model of cosmic expansion:

- **Particle Expansion**: Particles move outward from the origin at a constant rate, representing the universe's expansion
- **Continuous Creation**: New particles spawn over time, simulating ongoing particle creation in the early universe
- **Grid Expansion**: The coordinate system expands to accommodate the growing universe
- **Time Acceleration**: Variable speed controls allow observation of both rapid early expansion and slower later phases

## Future Development Plans

Potential enhancements for the project:

- **Multiple Expansion Phases**: Different expansion rates for different cosmic epochs
- **Particle Interactions**: Basic collision detection and particle combination
- **Temperature Visualization**: Color changes based on cooling universe
- **Cosmic Microwave Background**: Background radiation visualization
- **Galaxy Formation**: Particle clustering and structure formation
- **Sound Effects**: Audio representation of cosmic events
- **Data Export**: Save simulation states and particle data
- **Performance Optimization**: Handle larger particle counts efficiently

## Educational Value

This project serves as both a programming exercise and an educational tool for understanding:
- Basic 3D graphics programming with Panda3D
- Particle system implementation
- Real-time simulation techniques
- Cosmic expansion concepts
- Interactive application development

## Project Structure

```
primeval-atom/
├── main.py                    # Main entry point
├── bigbang_simulator.py      # Core simulation logic
├── simulation_ui.py          # UI and controls
├── pyproject.toml            # Project configuration and dependencies
├── tests/                    # Unit tests
│   ├── test_bigbang_simulator.py
│   ├── test_simulation_ui.py
│   ├── test_main.py
│   └── test_integration.py
├── README.md                 # This file
└── venv/                     # Python virtual environment (contains Panda3D)
```

## License

This project is open-source and available for educational and research purposes.