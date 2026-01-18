from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode


class SimulationUI:
    """Handles all UI elements and user controls for the Big Bang Simulator."""

    def __init__(self, simulator):
        self.simulator = simulator  # Reference to the main simulator
        self.ui_text = None

        # Setup UI and controls
        self.setup_ui()
        self.setup_input()

        # Start UI update task
        self.simulator.taskMgr.add(self.update_ui_task, "update_ui_task")

    def setup_ui(self):
        """Initialize UI elements."""
        # OnscreenText to display simulation status
        self.ui_text = OnscreenText(
            text="Time: 0.00s | Speed: 1.0x",
            pos=(-0.8, -0.75), # Adjusted horizontal position closer to left center
            scale=0.07,
            fg=(1, 1, 1, 1), # White color
            align=TextNode.ALeft,
            mayChange=True
        )

    def update_ui_task(self, task):
        """Update UI elements periodically."""
        self.update_ui_text()
        return task.cont

    def update_ui_text(self):
        """Update the UI text with current simulation status."""
        pause_status = "Paused" if self.simulator.paused else "Running"
        self.ui_text.setText(
            f"Time: {self.simulator.simulation_time:.2f}s | Speed: {self.simulator.simulation_speed:.1f}x | Status: {pause_status}\n"
            f"Controls: Up/Down Arrows (Speed), R (Reset), P (Pause)"
        )

    def setup_input(self):
        """Setup keyboard input bindings."""
        self.simulator.accept('arrow_up', self.increase_speed)
        self.simulator.accept('arrow_down', self.decrease_speed)
        self.simulator.accept('r', self.reset_simulation)
        self.simulator.accept('p', self.toggle_pause)

    def increase_speed(self):
        """Increase simulation speed."""
        self.simulator.simulation_speed = min(self.simulator.max_speed,
                                             self.simulator.simulation_speed + self.simulator.speed_increment)
        self.update_ui_text()

    def decrease_speed(self):
        """Decrease simulation speed."""
        self.simulator.simulation_speed = max(self.simulator.min_speed,
                                             self.simulator.simulation_speed - self.simulator.speed_increment)
        self.update_ui_text()

    def reset_simulation(self):
        """Reset the entire simulation."""
        # Remove all existing particles
        for particle in self.simulator.particles:
            particle.removeNode()
        self.simulator.particles = []

        # Reset simulation time and spawn timer
        self.simulator.simulation_time = 0.0
        self.simulator.time_since_last_spawn = 0
        self.simulator.paused = False # Unpause on reset

        # Reset grid
        self.simulator.current_grid_size = self.simulator.initial_grid_size
        self.simulator.create_grid(self.simulator.current_grid_size)

        # Create initial particles again
        self.simulator.create_initial_particles()
        self.update_ui_text()

    def toggle_pause(self):
        """Toggle simulation pause state."""
        self.simulator.paused = not self.simulator.paused
        self.update_ui_text()