# Chapter 1: Isaac Sim Overview

## Overview

This chapter introduces NVIDIA Isaac Sim as a comprehensive simulation environment for AI-powered robotics, focusing on computer vision, perception, and intelligent decision-making systems for humanoid robotics applications.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Understand the architecture and capabilities of NVIDIA Isaac Sim
2. Set up Isaac Sim for robotics simulation and AI training
3. Configure physics and rendering settings for realistic simulation
4. Integrate Isaac Sim with ROS 2 for robotics applications

## Introduction to NVIDIA Isaac Sim

NVIDIA Isaac Sim is a robotics simulator built on NVIDIA Omniverse, providing:
- **Photorealistic rendering**: RTX-accelerated rendering for computer vision training
- **Accurate physics simulation**: PhysX-based physics engine for realistic interactions
- **AI training environment**: Integrated tools for reinforcement learning and computer vision
- **ROS 2 integration**: Seamless integration with ROS 2 for robotics development
- **Digital twin capabilities**: High-fidelity simulation for testing and validation

### Key Features of Isaac Sim

- **Synthetic Data Generation**: Create labeled training data for computer vision
- **Reinforcement Learning**: Integrated RL training environments
- **Multi-robot Simulation**: Support for complex multi-robot scenarios
- **Hardware-in-the-loop**: Integration with real hardware for testing
- **Extensible Framework**: Python API for custom simulation scenarios

## Installing and Setting Up Isaac Sim

### System Requirements

- **GPU**: NVIDIA GPU with RTX or newer architecture (8GB+ VRAM recommended)
- **OS**: Ubuntu 20.04/22.04 or Windows 10/11
- **RAM**: 32GB+ recommended
- **Storage**: 50GB+ available space

### Installation Methods

#### Docker Installation (Recommended)

```bash
# Pull Isaac Sim Docker image
docker pull nvcr.io/nvidia/isaac-sim:latest

# Run Isaac Sim with GPU support
docker run --gpus all -it --rm \
  --network=host \
  --env "ACCEPT_EULA=Y" \
  --env "USING_HEADLESS_MODE=0" \
  nvcr.io/nvidia/isaac-sim:latest
```

#### Local Installation

```bash
# Download Isaac Sim from NVIDIA Developer website
# Follow installation instructions for your platform
# Ensure CUDA and other dependencies are properly installed
```

### Basic Launch

```bash
# Using Docker
./docker/isaac-sim.sh

# Using local installation
./isaac-sim/python.sh
```

## Isaac Sim Architecture

### Core Components

1. **Omniverse Kit**: The underlying platform providing USD scene management
2. **PhysX**: NVIDIA's physics simulation engine
3. **RTX Renderer**: Real-time ray tracing renderer
4. **ROS Bridge**: Integration layer for ROS 2 communication
5. **AI Framework**: Tools for computer vision and reinforcement learning

### USD (Universal Scene Description)

Isaac Sim uses USD for scene representation:

```python
import omni
from pxr import Usd, UsdGeom, Gf, Sdf

# Create a new USD stage
stage = Usd.Stage.CreateNew("my_robot.usda")

# Create a robot prim
robot_prim = UsdGeom.Xform.Define(stage, "/World/Robot")
robot_prim.AddTranslateOp().Set(Gf.Vec3d(0, 0, 1.0))

# Create a base link
base_link = UsdGeom.Cube.Define(stage, "/World/Robot/BaseLink")
base_link.GetSizeAttr().Set(1.0)

# Save the stage
stage.GetRootLayer().Save()
```

## Robot Modeling in Isaac Sim

### URDF Import

Isaac Sim provides tools for importing URDF models:

```python
import omni
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import get_prim_at_path

# Import URDF robot
def import_urdf_robot(urdf_path, prim_path):
    # Add URDF reference to stage
    add_reference_to_stage(
        usd_path=urdf_path,
        prim_path=prim_path
    )

# Example usage
robot_path = "/Isaac/Robots/Franka/franka.usd"
add_reference_to_stage(robot_path, "/World/Robot")
```

### Custom Robot Creation

```python
import omni
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.nucleus import get_assets_root_path
import numpy as np

class CustomRobot(Robot):
    def __init__(
        self,
        prim_path: str,
        name: str = "custom_robot",
        usd_path: str = None,
        position: np.ndarray = np.array([0, 0, 0]),
        orientation: np.ndarray = np.array([0, 0, 0, 1])
    ) -> None:
        self._usd_path = usd_path
        self._position = position
        self._orientation = orientation

        super().__init__(
            prim_path=prim_path,
            name=name,
            usd_path=usd_path,
            position=position,
            orientation=orientation
        )

# Create robot in world
world = World()
robot = world.scene.add(
    CustomRobot(
        prim_path="/World/Robot",
        name="my_robot",
        usd_path="path/to/robot.usd",
        position=np.array([0, 0, 1.0])
    )
)
```

## Physics Configuration

### Physics Scene Setup

```python
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_ground_plane
from omni.isaac.core.utils.prims import set_targets
import omni.physx as ophysx

# Create physics world
world = World(stage_units_in_meters=1.0)

# Set physics parameters
world.scene.add_default_ground_plane()

# Configure physics settings
physics_settings = world.get_physics_context().get_physics_sim_params()
physics_settings.dt = 1.0 / 60.0  # Time step
physics_settings.substeps = 1
physics_settings.gravity = [0.0, 0.0, -9.81]
```

### Material Properties

```python
from omni.isaac.core.materials import VisualMaterial
from omni.isaac.core.utils.prims import get_prim_at_path

# Create custom material
material = world.scene.add(
    VisualMaterial(
        prim_path="/World/Looks/RobotMaterial",
        name="robot_material",
        color=np.array([0.1, 0.1, 0.8])
    )
)

# Apply material to robot parts
robot_prim = get_prim_at_path("/World/Robot/BaseLink")
material.apply(robot_prim)
```

## Sensor Integration

### Camera Sensors

```python
from omni.isaac.sensor import Camera
import numpy as np

# Add RGB camera to robot
camera = world.scene.add(
    Camera(
        prim_path="/World/Robot/Camera",
        frequency=30,  # Hz
        resolution=(640, 480)
    )
)

# Configure camera parameters
camera.set_focal_length(24.0)
camera.set_horizontal_aperture(20.955)
camera.set_vertical_aperture(15.29)
```

### LIDAR Sensors

```python
from omni.isaac.range_sensor import _range_sensor
import omni
import numpy as np

# Get range sensor interface
range_sensor_interface = _range_sensor.acquire_range_sensor_interface()

# Create LIDAR sensor
lidar_config = {
    "rotation_frequency": 10,
    "samples_per_scan": 720,
    "max_range": 25.0,
    "min_range": 0.1,
    "angle_range": (-np.pi/2, np.pi/2),
    "angles": np.linspace(-np.pi/2, np.pi/2, 720)
}

# Add LIDAR to robot
lidar_prim_path = "/World/Robot/Lidar"
lidar = world.scene.add(
    LIDAR(
        prim_path=lidar_prim_path,
        name="front_lidar",
        translation=np.array([0.3, 0, 0.2]),
        orientation=np.array([0, 0, 0, 1])
    )
)
```

## ROS 2 Integration

### ROS Bridge Setup

```python
from omni.isaac.ros_bridge import RosBridge
import rclpy
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist

# Initialize ROS bridge
ros_bridge = RosBridge()

# Initialize ROS node
rclpy.init()
ros_node = rclpy.create_node('isaac_sim_controller')

# Create ROS publishers and subscribers
cmd_vel_pub = ros_node.create_publisher(Twist, '/cmd_vel', 10)
scan_sub = ros_node.create_subscription(LaserScan, '/scan', scan_callback, 10)
```

### ROS Message Synchronization

```python
import asyncio
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.core import SimulationWorld

class ROSSyncController:
    def __init__(self):
        self.sim_world = SimulationWorld.instance()
        self.ros_node = None
        self.latest_cmd = None

    def sync_with_ros(self):
        """Synchronize simulation with ROS messages"""
        # Process ROS callbacks
        if self.ros_node:
            rclpy.spin_once(self.ros_node, timeout_sec=0)

        # Apply latest commands
        if self.latest_cmd:
            self.execute_robot_command(self.latest_cmd)

    def execute_robot_command(self, cmd):
        """Execute robot command from ROS"""
        # Convert ROS command to Isaac Sim action
        linear_vel = cmd.linear.x
        angular_vel = cmd.angular.z

        # Apply to robot
        self.robot.apply_velocity_commands([linear_vel, angular_vel])
```

## Computer Vision in Isaac Sim

### Synthetic Data Generation

```python
import omni
from omni.isaac.synthetic_utils import SyntheticDataHelper
from omni.isaac.core.utils.prims import get_prim_at_path
import numpy as np

class SyntheticDataGenerator:
    def __init__(self):
        self.sd_helper = SyntheticDataHelper()

    def generate_training_data(self, robot_path, num_samples=1000):
        """Generate synthetic training data for computer vision"""

        for i in range(num_samples):
            # Randomize scene
            self.randomize_scene()

            # Capture RGB image
            rgb_data = self.sd_helper.get_rgb_data(robot_path + "/Camera")

            # Capture segmentation mask
            seg_data = self.sd_helper.get_semantic_segmentation(robot_path + "/Camera")

            # Capture depth data
            depth_data = self.sd_helper.get_depth_data(robot_path + "/Camera")

            # Save data with annotations
            self.save_training_sample(rgb_data, seg_data, depth_data, i)

    def randomize_scene(self):
        """Randomize lighting, objects, and camera position"""
        # Randomize lighting
        light_prim = get_prim_at_path("/World/Light")
        # Set random position, intensity, color

        # Randomize object positions
        # Move objects to random locations within bounds
        pass

    def save_training_sample(self, rgb, seg, depth, sample_id):
        """Save training sample with annotations"""
        # Save RGB image
        rgb.save(f"rgb_{sample_id:06d}.png")

        # Save segmentation mask
        seg.save(f"seg_{sample_id:06d}.png")

        # Save depth map
        depth.save(f"depth_{sample_id:06d}.png")
```

## Reinforcement Learning Integration

### RL Environment Setup

```python
from omni.isaac.gym import IsaacEnv
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
import numpy as np
import torch

class IsaacRobotEnv(IsaacEnv):
    def __init__(self):
        # Initialize environment parameters
        self.robot_position = np.array([0, 0, 1.0])
        self.target_position = np.array([5, 5, 0])

        # Call parent constructor
        super().__init__()

    def set_up_scene(self, scene):
        # Add robot to scene
        world = self._world
        world.scene.add_default_ground_plane()

        # Add robot
        robot = world.scene.add(
            Robot(
                prim_path="/World/Robot",
                name="robot",
                usd_path="path/to/robot.usd",
                position=self.robot_position
            )
        )

        # Add target
        target = world.scene.add(
            FixedCuboid(
                prim_path="/World/Target",
                name="target",
                position=self.target_position,
                size=0.2,
                color=np.array([1, 0, 0])
            )
        )

    def get_observations(self):
        # Get robot state
        robot_position, robot_orientation = self._world.scene.get_object("robot").get_world_pose()
        robot_linear_vel = self._world.scene.get_object("robot").get_linear_velocity()
        robot_angular_vel = self._world.scene.get_object("robot").get_angular_velocity()

        # Get target relative position
        relative_pos = self.target_position - robot_position

        # Combine observations
        obs = np.concatenate([
            robot_position[:2],  # x, y
            robot_linear_vel[:2],  # linear vel x, y
            robot_angular_vel[2:3],  # angular vel z
            relative_pos[:2]  # relative target position
        ])

        return {"obs": obs}

    def get_rewards(self):
        # Calculate reward based on distance to target
        robot_pos = self._world.scene.get_object("robot").get_world_pose()[0]
        distance = np.linalg.norm(robot_pos[:2] - self.target_position[:2])

        # Reward based on proximity to target
        reward = -distance * 0.1  # Negative distance penalty

        # Bonus for getting close
        if distance < 0.5:
            reward += 10.0

        return reward

    def get_extras(self):
        return {}

    def reset(self):
        # Reset robot to initial position
        self._world.scene.get_object("robot").set_world_pose(
            self.robot_position,
            orientation=[0, 0, 0, 1]
        )

        # Randomize target position
        self.target_position = np.random.uniform(low=[-5, -5], high=[5, 5], size=(2,))
        self.target_position = np.append(self.target_position, [0])

        return self.get_observations()

    def set_actions(self, actions):
        # Convert actions to robot commands
        linear_vel = actions[0]  # Forward/backward
        angular_vel = actions[1]  # Turn left/right

        # Apply to robot
        self._world.scene.get_object("robot").apply_velocity_commands(
            [linear_vel, 0, 0],  # Linear velocity
            [0, 0, angular_vel]   # Angular velocity
        )
```

## Performance Optimization

### Simulation Settings

```python
# Optimize for performance vs quality
def configure_performance_settings():
    # Set rendering quality
    import omni.kit.app
    app = omni.kit.app.get_app()

    # For training: higher quality
    settings = {
        "rtx-defaults": {
            "pathtracing": False,  # Disable for performance
            "denoising": False,    # Disable for performance
            "maxBounces": 1        # Reduce for performance
        }
    }

    # Apply settings
    for section, params in settings.items():
        for param, value in params.items():
            app.get_rendering_context().set_setting(f"/{section}/{param}", value)

# Level of detail settings
def configure_lod_settings():
    # Set primitive complexity for collision
    # Use simpler shapes for collision detection
    # Use detailed shapes for visual rendering
    pass
```

## Best Practices

1. **Scene Complexity**: Balance visual quality with simulation performance
2. **Physics Tuning**: Adjust time steps and solver parameters for stability
3. **Sensor Configuration**: Match sensor parameters to real hardware
4. **Lighting**: Use consistent lighting for synthetic data generation
5. **Validation**: Compare simulation results with real-world data

## Troubleshooting

### Common Issues

- **GPU Memory**: Reduce scene complexity or rendering resolution
- **Physics Instability**: Decrease time step or adjust solver parameters
- **ROS Connection**: Ensure ROS bridge is properly configured
- **Performance**: Close unnecessary applications and processes

## Summary

Isaac Sim provides a comprehensive platform for AI-powered robotics simulation with photorealistic rendering and accurate physics. The next chapter will cover AI and robot training in Isaac Sim.