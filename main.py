import random
import math
from panda3d.core import loadPrcFileData
loadPrcFileData("", "win-size 1600 1200")
loadPrcFileData("", "window-title The Primeval Atom")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, VBase4, Vec3, LColor, TextNode, Texture, PNMImage, LineSegs
from direct.gui.OnscreenText import OnscreenText
import direct.gui.DirectGuiGlobals as DGG # For text positioning

class BigBangSimulator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0)  # Black background
        self.disableMouse()  # Disable default camera control

        # Basic camera setup
        self.camera.setPos(0, -40, 0)  # Move camera back
        self.camera.lookAt(0, 0, 0)  # Look at the origin

        # Basic lighting
        self.setup_lighting()

        # Grid parameters
        self.grid_node = None
        self.initial_grid_size = 50
        self.current_grid_size = self.initial_grid_size
        self.grid_spacing = 2 # User modified to 2
        self.grid_growth_threshold = 0.8 # Grow grid when particles reach 80% of current grid_size
        self.grid_growth_increment = 20 # How much the grid grows each time

        # Create 3D grid
        self.create_grid(self.current_grid_size) # <--- NEW: Pass initial grid size

        # Particle system parameters
        self.num_initial_particles = 20
        self.expansion_rate = 0.1
        self.particles = []
        self.particle_types = {
            "type1": {"color": LColor(1, 0.5, 0, 1), "scale": 0.5}, # Orange
            "type2": {"color": LColor(0, 0.5, 1, 1), "scale": 0.7}, # Blue
            "type3": {"color": LColor(0.8, 0, 0.8, 1), "scale": 0.6}, # Purple
            "type4": {"color": LColor(0.2, 0.8, 0.2, 1), "scale": 0.4}, # Green
        }
        self.spawn_interval = 0.5 # Seconds between new particle spawns
        self.time_since_last_spawn = 0

        # Simulation time parameters
        self.simulation_time = 0.0
        self.simulation_speed = 5.0 # 1.0 is normal speed, 2.0 is double speed, etc.
        self.min_speed = 0.1
        self.max_speed = 50.0
        self.speed_increment = 1.0
        self.paused = False

        # Create initial particles
        self.create_initial_particles()

        # Generate particle texture once
        self.particle_texture = self.create_radial_texture()

        # Start the expansion task
        self.taskMgr.add(self.update_simulation_time, "update_simulation_time_task")
        self.taskMgr.add(self.expand_universe, "expand_universe_task")
        self.taskMgr.add(self.spawn_particles_task, "spawn_particles_task")
        self.taskMgr.add(self.update_grid_size_task, "update_grid_size_task") # <--- NEW: Grid update task

        # Setup user input
        self.setup_input()

        # Setup UI
        self.setup_ui()
        self.taskMgr.add(self.update_ui_task, "update_ui_task")

    def setup_lighting(self):
        # ... (lighting code remains the same as before) ...
        from panda3d.core import AmbientLight, DirectionalLight, VBase4

        # Ambient light
        alight = AmbientLight('ambientLight')
        alight.setColor(VBase4(0.3, 0.3, 0.3, 1))
        ambientLight = self.render.attachNewNode(alight)
        self.render.setLight(ambientLight)

        # Directional light
        dlight = DirectionalLight('directionalLight')
        dlight.setColor(VBase4(0.8, 0.8, 0.8, 1))
        directionalLight = self.render.attachNewNode(dlight)
        directionalLight.setHpr(0, -60, 0)  # Angle the light
        self.render.setLight(directionalLight)

    def create_radial_texture(self):
        # ... (unchanged radial texture creation code) ...
        tex_size = 64
        image = PNMImage(tex_size, tex_size, 1) # 1 for grayscale
        
        for y in range(tex_size):
            for x in range(tex_size):
                # Calculate distance from center (normalized to 0.0 to 1.0)
                dist_x = (x / (tex_size - 1)) - 0.5
                dist_y = (y / (tex_size - 1)) - 0.5
                distance = math.sqrt(dist_x**2 + dist_y**2)

                # Create a radial gradient (brighter in center, darker outwards)
                # Clamp value between 0 and 1, invert it so center is brightest
                color_val = max(0.0, 1.0 - (distance * 2.0))
                image.setXelA(x, y, color_val) # Set alpha for transparency
                # image.setXel(x, y, color_val) # For RGB

        texture = Texture("radial_gradient")
        texture.load(image)
        texture.setFormat(Texture.FAlpha) # Use FAlpha for transparency if needed
        return texture

    def create_grid(self, grid_size): # <--- MODIFIED: Accepts grid_size
        if self.grid_node:
            self.grid_node.removeNode() # Remove old grid if it exists

        grid_spacing = self.grid_spacing # Use class member for spacing
        grid_color = VBase4(0.2, 0.2, 0.2, 1) # Dark grey color for grid lines

        # Create a LineSegs object
        ls = LineSegs()
        ls.setThickness(1)
        ls.setColor(grid_color)

        # Draw lines along the XZ plane (like a floor grid)
        for i in range(-grid_size, grid_size + 1, grid_spacing):
            # X lines
            ls.moveTo(i, 0, -grid_size)
            ls.drawTo(i, 0, grid_size)
            # Z lines
            ls.moveTo(-grid_size, 0, i)
            ls.drawTo(grid_size, 0, i)
        
        # Add some lines along the Y axis for depth
        ls.moveTo(0, -grid_size, 0)
        ls.drawTo(0, grid_size, 0)

        # Generate the geometry and attach it to render
        self.grid_node = self.render.attachNewNode(ls.create()) # Store reference
        self.grid_node.setPos(0, 0, 0) # Position the grid at the origin

    def update_grid_size_task(self, task): # <--- NEW: Task to dynamically update grid size
        if not self.paused and self.particles: # Only update if not paused and particles exist
            max_extent = 0.0
            for particle in self.particles:
                pos = particle.getPos()
                # Get the maximum absolute coordinate value
                extent = max(abs(pos.x), abs(pos.y), abs(pos.z))
                if extent > max_extent:
                    max_extent = extent
            
            # Check if particles are approaching the edge of the current grid
            if max_extent > (self.current_grid_size * self.grid_growth_threshold):
                new_grid_size = self.current_grid_size + self.grid_growth_increment
                print(f"Expanding grid to size: {new_grid_size}")
                self.create_grid(new_grid_size)
                self.current_grid_size = new_grid_size
        return task.cont

    def create_initial_particles(self):
        for _ in range(self.num_initial_particles):
            self.spawn_new_particle()

    def spawn_new_particle(self):
        # Create a sphere instead of loading "models/smiley"
        sphere = self.loader.loadModel("misc/sphere") # Panda3D's default sphere model
        sphere.reparentTo(self.render)
        
        # Choose a random particle type
        particle_type_name = random.choice(list(self.particle_types.keys()))
        particle_props = self.particle_types[particle_type_name]

        # Set color and scale
        sphere.setColor(particle_props["color"])
        sphere.setScale(particle_props["scale"])

        particle = sphere # 'particle' refers to the sphere

        # Initial random position close to the origin
        x = random.uniform(-0.1, 0.1)
        y = random.uniform(-0.1, 0.1)
        z = random.uniform(-0.1, 0.1)
        particle.setPos(x, y, z)
        
        # Store initial direction for expansion as individual components
        direction_vec = Vec3(x, y, z).normalized()
        particle.setTag("dir_x", str(direction_vec.x))
        particle.setTag("dir_y", str(direction_vec.y))
        particle.setTag("dir_z", str(direction_vec.z))
        
        self.particles.append(particle)

    def update_simulation_time(self, task):
        if not self.paused: # Only update if not paused
            dt = globalClock.getDt()
            self.simulation_time += dt * self.simulation_speed
        return task.cont

    def spawn_particles_task(self, task):
        if not self.paused: # Only spawn if not paused
            dt = globalClock.getDt()
            self.time_since_last_spawn += dt * self.simulation_speed # Use simulation speed
            if self.time_since_last_spawn > self.spawn_interval:
                self.spawn_new_particle()
                self.time_since_last_spawn = 0
        return task.cont

    def expand_universe(self, task):
        if not self.paused: # Only expand if not paused
            dt = globalClock.getDt() # Time elapsed since last frame
            for particle in self.particles:
                # Retrieve individual direction components and convert to float
                dir_x = float(particle.getTag("dir_x"))
                dir_y = float(particle.getTag("dir_y"))
                dir_z = float(particle.getTag("dir_z"))
                direction = Vec3(dir_x, dir_y, dir_z)

                current_pos = particle.getPos()
                new_pos = current_pos + direction * self.expansion_rate * dt * self.simulation_speed # Use simulation speed
                particle.setPos(new_pos)
        return task.cont

    def setup_input(self):
        self.accept('arrow_up', self.increase_speed)
        self.accept('arrow_down', self.decrease_speed)
        self.accept('r', self.reset_simulation)
        self.accept('p', self.toggle_pause) # New key binding for pause

    def increase_speed(self):
        self.simulation_speed = min(self.max_speed, self.simulation_speed + self.speed_increment)
        # print(f"Simulation speed: {self.simulation_speed:.1f}") # No longer need to print to console
        self.update_ui_text()

    def decrease_speed(self):
        self.simulation_speed = max(self.min_speed, self.simulation_speed - self.speed_increment)
        # print(f"Simulation speed: {self.simulation_speed:.1f}") # No longer need to print to console
        self.update_ui_text()

    def reset_simulation(self):
        # Remove all existing particles
        for particle in self.particles:
            particle.removeNode()
        self.particles = []

        # Reset simulation time and spawn timer
        self.simulation_time = 0.0
        self.time_since_last_spawn = 0
        self.paused = False # Unpause on reset

        # Reset grid
        self.current_grid_size = self.initial_grid_size # Reset grid size
        self.create_grid(self.current_grid_size) # Recreate initial grid

        # Create initial particles again
        self.create_initial_particles()
        self.update_ui_text()


    def toggle_pause(self):
        self.paused = not self.paused
        # print(f"Simulation paused: {self.paused}") # No longer need to print to console
        self.update_ui_text()

    def setup_ui(self):
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
        self.update_ui_text()
        return task.cont

    def update_ui_text(self):
        pause_status = "Paused" if self.paused else "Running"
        self.ui_text.setText(
            f"Time: {self.simulation_time:.2f}s | Speed: {self.simulation_speed:.1f}x | Status: {pause_status}\n"
            f"Controls: Up/Down Arrows (Speed), R (Reset), P (Pause)"
        )


if __name__ == "__main__":
    app = BigBangSimulator()
    app.run()
