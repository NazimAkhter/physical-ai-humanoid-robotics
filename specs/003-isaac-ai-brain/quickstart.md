# Quickstart Guide: Isaac AI Brain Module

## Overview
This guide provides a quick introduction to setting up and working with the Isaac AI Brain module. This module teaches students how to create photorealistic simulations with Isaac Sim, implement perception systems with Isaac ROS, and configure navigation using Nav2.

## Prerequisites
- Computer with NVIDIA GPU (RTX 2080 or better recommended)
- Ubuntu 22.04 LTS with ROS 2 Humble Hawksbill installed
- NVIDIA Isaac Sim installed and licensed
- Isaac ROS components installed
- Nav2 packages installed via ROS 2
- At least 16GB RAM (32GB recommended)

## Development Environment Setup

### 1. Isaac Sim Installation
```bash
# Install Isaac Sim from NVIDIA Developer website
# Requires NVIDIA GPU with RTX or newer architecture
# Follow NVIDIA's installation guide for your platform
# Verify installation:
isaac-sim --version
```

### 2. Isaac ROS Components
```bash
# Install Isaac ROS packages via apt
sudo apt update
sudo apt install ros-humble-isaac-ros-*

# Or build from source for latest features
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git
# Follow build instructions in repository
```

### 3. Nav2 Installation
```bash
# Install Nav2 packages
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup

# Verify installation
ros2 launch nav2_bringup navigation_launch.py
```

### 4. Docusaurus Documentation Setup
```bash
# Install Node.js 18+
# Clone or navigate to the documentation repository
cd docs

# Install dependencies
npm install

# Start local development server
npm start
```

### 5. Project Structure
```
physical_ai_book/
├── docs/
│   └── modules/
│       └── 03-isaac-ai-brain/
│           ├── index.md
│           ├── chapter-1-isaac-sim-essentials.md
│           ├── chapter-2-isaac-ros-perception.md
│           ├── chapter-3-navigation-with-nav2.md
│           └── chapter-4-integrated-pipeline.md
├── static/
│   ├── img/
│   ├── models/
│   └── datasets/
├── src/
│   └── components/
├── backend/
│   └── src/
│       └── api/
└── specs/
    └── 03-isaac-ai-brain/
```

## Chapter 1: Isaac Sim Essentials

### Creating Your First Scene
```python
# Example Python script to create a basic Isaac Sim scene
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.nucleus import get_assets_root_path

# Initialize world
world = World(stage_units_in_meters=1.0)

# Add ground plane
world.scene.add_default_ground_plane()

# Add a simple object
add_reference_to_stage(
    usd_path="/Isaac/Props/Prims/visual_cube.usd",
    prim_path="/World/Cube"
)

# Play the simulation
world.reset()
for i in range(500):
    world.step(render=True)
```

### Synthetic Dataset Generation
```python
# Example of generating synthetic dataset with annotations
import omni.synthetic_utils as syn_utils

# Configure synthetic data generation
synthetic_config = {
    "rgb": True,
    "depth": True,
    "bounding_box_2d_tight": True,
    "instance_segmentation": True
}

# Generate dataset
dataset_generator = syn_utils.DatasetGenerator(config=synthetic_config)
dataset_generator.generate_dataset(
    scene_path="/path/to/scene.usd",
    output_path="/path/to/output/dataset",
    num_frames=1000
)
```

## Chapter 2: Isaac ROS Perception

### Setting up VSLAM Pipeline
```xml
<!-- Example launch file for Isaac ROS VSLAM -->
<launch>
  <!-- Launch Isaac ROS Visual SLAM node -->
  <node pkg="isaac_ros_visual_slam" exec="visual_slam_node" name="visual_slam">
    <param name="enable_rectification" value="True"/>
    <param name="enable_fisheye_distortion" value="False"/>
    <param name="map_frame" value="map"/>
    <param name="odom_frame" value="odom"/>
    <param name="base_frame" value="base_link"/>
    <param name="publish_odom_tf" value="True"/>
  </node>

  <!-- Launch image rectification -->
  <node pkg="isaac_ros_image_rectifier" exec="image_rectifier_node" name="image_rectifier_left">
    <param name="input_width" value="1920"/>
    <param name="input_height" value="1200"/>
    <param name="camera_model" value="pinhole"/>
  </node>
</launch>
```

### Feature Tracking Node
```cpp
// Example C++ code for Isaac ROS feature tracking
#include <rclcpp/rclcpp.hpp>
#include <isaac_ros_visual_slam/feature_tracker.hpp>

class FeatureTrackerNode : public rclcpp::Node
{
public:
  FeatureTrackerNode()
  : Node("feature_tracker_node")
  {
    // Initialize feature tracking parameters
    this->declare_parameter("max_features", 1000);
    this->declare_parameter("min_distance", 10.0);

    // Create feature tracking pipeline
    feature_tracker_ = std::make_unique<FeatureTracker>();
  }

private:
  std::unique_ptr<FeatureTracker> feature_tracker_;
};
```

## Chapter 3: Navigation with Nav2

### Nav2 Configuration File
```yaml
# Example Nav2 configuration for humanoid robot
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 10.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: "map"
    robot_base_frame: "base_link"
    odom_topic: "/odom"
    default_bt_xml_filename: "navigate_w_replanning_and_recovery.xml"
    plugin_lib_names:
    - "nav2_compute_path_to_pose_action_bt_node"
    - "nav2_follow_path_action_bt_node"
    - "nav2_back_up_action_bt_node"
    - "nav2_spin_action_bt_node"
    - "nav2_wait_action_bt_node"
    - "nav2_clear_costmap_service_bt_node"
    - "nav2_is_stuck_condition_bt_node"
    - "nav2_goal_reached_condition_bt_node"
    - "nav2_goal_updated_condition_bt_node"
    - "nav2_initial_pose_received_condition_bt_node"
    - "nav2_reinitialize_global_localization_service_bt_node"
    - "nav2_rate_controller_bt_node"
    - "nav2_distance_controller_bt_node"
    - "nav2_speed_controller_bt_node"
    - "nav2_truncate_path_action_bt_node"
    - "nav2_goal_updater_node_bt_node"
    - "nav2_recovery_node_bt_node"
    - "nav2_pipeline_sequence_bt_node"
    - "nav2_round_robin_node_bt_node"
    - "nav2_transform_available_condition_bt_node"
    - "nav2_time_expired_condition_bt_node"
    - "nav2_path_expiring_timer_condition"
    - "nav2_distance_traveled_condition_bt_node"
    - "nav2_single_trigger_bt_node"
    - "nav2_is_battery_low_condition_bt_node"
    - "nav2_navigate_through_poses_action_bt_node"
    - "nav2_navigate_to_pose_action_bt_node"
    - "nav2_remove_passed_goals_action_bt_node"
    - "nav2_planner_selector_bt_node"
    - "nav2_controller_selector_bt_node"
    - "nav2_goal_checker_selector_bt_node"
```

## Chapter 4: Integrated Perception → Navigation Pipeline

### Perception-to-Navigation Integration
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import Float32

class PerceptionNavIntegrator(Node):
    def __init__(self):
        super().__init__('perception_nav_integrator')

        # Subscriptions for perception data
        self.perception_sub = self.create_subscription(
            MarkerArray,
            '/perception/obstacles',
            self.obstacle_callback,
            10
        )

        # Subscriptions for navigation data
        self.nav_goal_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        # Publisher for adapted navigation commands
        self.nav_cmd_pub = self.create_publisher(
            PoseStamped,
            '/adapted_goal_pose',
            10
        )

        # Publisher for integration status
        self.status_pub = self.create_publisher(
            Float32,
            '/integration_status',
            10
        )

        self.latest_obstacles = []
        self.original_goal = None

    def obstacle_callback(self, msg):
        """Process obstacles detected by perception system"""
        self.latest_obstacles = msg.markers
        self.check_navigation_adaptation()

    def goal_callback(self, msg):
        """Receive navigation goal from user/system"""
        self.original_goal = msg
        self.check_navigation_adaptation()

    def check_navigation_adaptation(self):
        """Check if navigation goal needs adaptation based on perception"""
        if self.original_goal is None or not self.latest_obstacles:
            return

        # Check if obstacles block the direct path to goal
        adapted_goal = self.adapt_goal_for_obstacles(
            self.original_goal,
            self.latest_obstacles
        )

        if adapted_goal:
            self.nav_cmd_pub.publish(adapted_goal)
            self.get_logger().info('Published adapted navigation goal')

            # Publish integration status (0.0 to 1.0)
            status_msg = Float32()
            status_msg.data = 0.9  # High integration confidence
            self.status_pub.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    integrator = PerceptionNavIntegrator()

    try:
        rclpy.spin(integrator)
    except KeyboardInterrupt:
        pass
    finally:
        integrator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Running Examples

### 1. Build and Run Documentation
```bash
# Navigate to docs directory
cd docs

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### 2. Test API Endpoints
```bash
# Get Isaac Sim scenes
curl -X GET "http://localhost:3000/api/v1/isaac-sim/scenes" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Request navigation
curl -X POST "http://localhost:3000/api/v1/nav2/navigation/request" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal_position": {"x": 5.0, "y": 3.0, "theta": 0.0},
    "robot_id": "humanoid_robot_1",
    "map_id": "lab_map"
  }'
```

### 3. Validate Simulation Configuration
```bash
# Verify Isaac Sim installation
isaac-sim --version

# Check Isaac ROS nodes
ros2 run isaac_ros_visual_slam visual_slam_node --ros-args --print-parameters
```

## Documentation Commands

### Generate Documentation
```bash
# Build Docusaurus site
cd docs
npm run build

# Serve locally
npm run serve

# Deploy to GitHub Pages
npm run deploy
```

### Validate Content
```bash
# Run content validation scripts
npm test

# Link checker
npx markdown-link-check "**/*.md"

# Build validation
npm run build
```

## Testing

### Run Documentation Tests
```bash
# JavaScript/MDX validation
npm test

# Link checker
npx markdown-link-check "**/*.md"

# Build validation
npm run build
```

## Next Steps
1. Complete all chapters in the Isaac AI Brain module
2. Integrate with the RAG chatbot for interactive learning
3. Deploy documentation to GitHub Pages
4. Test with actual Isaac Sim and Nav2 environments