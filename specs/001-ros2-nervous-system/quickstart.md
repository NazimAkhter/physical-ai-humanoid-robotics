# Quickstart Guide: ROS 2 Nervous System Module

## Overview
This guide provides a quick introduction to the ROS 2 Nervous System module, covering the essential concepts and code examples to get you started with building the robotic nervous system.

## Prerequisites
- Basic understanding of Python programming
- Familiarity with software development concepts
- Computer with ROS 2 Humble Hawksbill installed (or Docker for containerized development)

## Development Environment Setup

### 1. ROS 2 Installation
```bash
# For Ubuntu 22.04
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/rosInstall.sh | bash
sudo apt install ros-humble-desktop
```

### 2. Python Environment
```bash
# Create virtual environment
python3 -m venv ros2_env
source ros2_env/bin/activate  # On Windows: ros2_env\Scripts\activate

# Install required packages
pip install rclpy
```

### 3. Project Structure
```
physical_ai_book/
├── docs/
│   └── modules/
│       └── 01-ros2-nervous-system/
├── src/
│   └── ros2_examples/
├── tests/
└── specs/
    └── 001-ros2-nervous-system/
```

## Chapter 1: ROS 2 Architecture Basics

### Creating Your First Node
```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Creating a Subscriber
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Chapter 2: Bridging Minds and Machines

### Python Agent with rclpy
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class AIAgent(Node):
    def __init__(self):
        super().__init__('ai_agent')

        # Publisher to send commands to robot
        self.command_publisher = self.create_publisher(String, 'robot_commands', 10)

        # Subscriber to receive sensor data
        self.sensor_subscriber = self.create_subscription(
            String,
            'sensor_data',
            self.sensor_callback,
            10
        )

        # Timer for AI decision making
        self.timer = self.create_timer(1.0, self.ai_decision_loop)

        self.get_logger().info('AI Agent initialized')

    def sensor_callback(self, msg):
        self.get_logger().info(f'Received sensor data: {msg.data}')
        # Process sensor data and make decisions

    def ai_decision_loop(self):
        # Simple AI decision logic
        command_msg = String()
        command_msg.data = f'Move forward - timestamp: {time.time()}'
        self.command_publisher.publish(command_msg)
        self.get_logger().info(f'Sent command: {command_msg.data}')

def main(args=None):
    rclpy.init(args=args)
    ai_agent = AIAgent()

    try:
        rclpy.spin(ai_agent)
    except KeyboardInterrupt:
        pass
    finally:
        ai_agent.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Chapter 3: Defining the Humanoid Body

### Basic URDF Example
```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.2 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.2 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Joint connecting head to base -->
  <joint name="head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.2"/>
  </joint>
</robot>
```

## Chapter 4: The First Reflex

### Complete Example: Publisher with URDF Integration
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import math

class SimpleReflex(Node):
    def __init__(self):
        super().__init__('simple_reflex')

        # Publisher for joint states
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)

        # Timer for reflex action
        self.timer = self.create_timer(0.1, self.reflex_callback)

        # Joint state message template
        self.joint_state = JointState()
        self.joint_state.name = ['head_joint']
        self.joint_state.position = [0.0]
        self.joint_state.velocity = [0.0]
        self.joint_state.effort = [0.0]

        self.get_logger().info('Simple Reflex system initialized')

    def reflex_callback(self):
        # Simple oscillating movement
        current_time = self.get_clock().now().nanoseconds / 1e9
        self.joint_state.position[0] = math.sin(current_time) * 0.5

        self.joint_state.header.stamp = self.get_clock().now().to_msg()
        self.joint_state.header.frame_id = 'base_link'

        self.joint_pub.publish(self.joint_state)

def main(args=None):
    rclpy.init(args=args)
    reflex = SimpleReflex()

    try:
        rclpy.spin(reflex)
    except KeyboardInterrupt:
        pass
    finally:
        reflex.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Running Examples

### 1. Build and Source Workspace
```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Build packages
colcon build

# Source the workspace
source install/setup.bash
```

### 2. Run Publisher and Subscriber
```bash
# Terminal 1: Run publisher
ros2 run your_package_name minimal_publisher

# Terminal 2: Run subscriber
ros2 run your_package_name minimal_subscriber
```

### 3. Visualize with RViz
```bash
# Run RViz to visualize the robot
ros2 run rviz2 rviz2
```

## Documentation Commands

### Generate Documentation
```bash
# Build Docusaurus site
cd docs
npm run build

# Serve locally
npm run start
```

### Validate URDF
```bash
# Use the validation API
curl -X POST http://localhost:8000/api/v1/validation/urdf \
  -H "Content-Type: application/json" \
  -d '{"urdf_content": "<robot>...</robot>"}'
```

## Testing

### Run Unit Tests
```bash
# Python tests
python3 -m pytest tests/

# ROS 2 tests
colcon test
```

## Next Steps
1. Complete all chapters in the ROS 2 Nervous System module
2. Integrate with the RAG chatbot for interactive learning
3. Deploy documentation to GitHub Pages
4. Test with real robotic hardware or simulation