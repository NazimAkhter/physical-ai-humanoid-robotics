# Chapter 1: Gazebo Simulation

## Overview

This chapter introduces Gazebo as a physics-accurate simulation environment for robotics, enabling safe testing and development of robotics algorithms before deployment on physical robots.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Set up and configure Gazebo simulation environment
2. Create robot models and environments for simulation
3. Implement physics-accurate simulations with realistic parameters
4. Integrate Gazebo with ROS 2 for robot control and testing

## Introduction to Gazebo

Gazebo is a 3D simulation environment that provides:
- High-fidelity physics simulation using ODE, Bullet, and SimBody engines
- Realistic rendering with support for multiple graphics engines
- Sensor simulation including cameras, LIDAR, IMU, and GPS
- Plugin architecture for custom functionality
- Integration with ROS and ROS 2

### Key Features of Gazebo

- **Physics Simulation**: Accurate modeling of rigid body dynamics
- **Sensor Simulation**: Realistic sensor models for perception testing
- **Environment Modeling**: Tools for creating complex environments
- **Robot Modeling**: Support for URDF and SDF robot descriptions
- **Plugin System**: Extensible architecture for custom functionality

## Installing and Setting Up Gazebo

### Installation

Gazebo can be installed separately or as part of a ROS 2 distribution:

```bash
# Install Gazebo Garden (recommended version for ROS 2 Humble)
sudo apt update
sudo apt install ros-humble-gazebo-*
```

### Basic Gazebo Launch

```bash
# Launch Gazebo GUI
gazebo

# Launch Gazebo with a specific world
gazebo /usr/share/gazebo-11/worlds/empty.world
```

## Robot Modeling in Gazebo

### URDF Integration

Gazebo works seamlessly with URDF (Unified Robot Description Format) files:

```xml
<?xml version="1.0"?>
<robot name="simple_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.083" ixy="0.0" ixz="0.0" iyy="0.083" iyz="0.0" izz="0.167"/>
    </inertial>
  </link>

  <!-- Sensor -->
  <link name="hokuyo_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.08"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.08"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="hokuyo_joint" type="fixed">
    <parent link="base_link"/>
    <child link="hokuyo_link"/>
    <origin xyz="0.2 0 0.1" rpy="0 0 0"/>
  </joint>

  <!-- Gazebo plugins -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="hokuyo_link">
    <sensor type="ray" name="head_hokuyo_sensor">
      <pose>0 0 0 0 0 0</pose>
      <visualize>false</visualize>
      <update_rate>40</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <resolution>1</resolution>
            <min_angle>-1.570796</min_angle>
            <max_angle>1.570796</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.10</min>
          <max>30.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <namespace>/simple_robot</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
      </plugin>
    </sensor>
  </gazebo>
</robot>
```

## Gazebo World Files

World files define the simulation environment:

```xml
<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="simple_world">
    <!-- Include a model from Gazebo's model database -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Custom box obstacle -->
    <model name="box_obstacle">
      <pose>2 2 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1667</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.1667</iyy>
            <iyz>0</iyz>
            <izz>0.1667</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Physics parameters -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>
  </world>
</sdf>
```

## ROS 2 Integration

### Launch File for Gazebo + Robot

```xml
<launch>
  <!-- Arguments -->
  <arg name="world" default="empty"/>
  <arg name="model" default="$(find-pkg-share my_robot_description)/urdf/robot.urdf"/>
  <arg name="rviz_config" default="$(find-pkg-share my_robot_description)/rviz/robot.rviz"/>

  <!-- Start Gazebo -->
  <include file="$(find-pkg-share gazebo_ros)/launch/gazebo.launch.py">
    <arg name="world" value="$(find-pkg-share my_robot_gazebo)/worlds/simple_world.world"/>
  </include>

  <!-- Spawn robot in Gazebo -->
  <node name="spawn_urdf" pkg="gazebo_ros" exec="spawn_entity.py"
        args="-entity simple_robot -topic robot_description -x 0 -y 0 -z 1"/>

  <!-- Robot state publisher -->
  <node pkg="robot_state_publisher" exec="robot_state_publisher" name="robot_state_publisher">
    <param name="publish_frequency" value="30"/>
    <param name="use_sim_time" value="true"/>
    <param name="robot_description" value="$(var model)"/>
  </node>

  <!-- Joint state publisher -->
  <node pkg="joint_state_publisher" exec="joint_state_publisher" name="joint_state_publisher">
    <param name="use_sim_time" value="true"/>
  </node>

  <!-- RViz for visualization -->
  <node pkg="rviz2" exec="rviz2" name="rviz2" args="-d $(var rviz_config)"/>
</launch>
```

## Control and Navigation in Gazebo

### Example Navigation Node

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

class GazeboNavigator(Node):
    def __init__(self):
        super().__init__('gazebo_navigator')

        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        # Timer for control loop
        self.timer = self.create_timer(0.1, self.control_loop)

        # State variables
        self.scan_data = None
        self.safe_distance = 0.5

    def scan_callback(self, msg):
        """Process laser scan data from Gazebo"""
        # Convert to numpy array for efficient processing
        ranges = np.array(msg.ranges)
        # Filter out invalid ranges
        valid_ranges = ranges[np.isfinite(ranges) & (ranges > 0)]

        if len(valid_ranges) > 0:
            self.closest_obstacle = np.min(valid_ranges)
        else:
            self.closest_obstacle = float('inf')

        self.scan_data = valid_ranges

    def control_loop(self):
        """Main navigation control loop"""
        if self.scan_data is None:
            return

        cmd = Twist()

        # Simple obstacle avoidance
        if self.closest_obstacle < self.safe_distance:
            # Stop or turn
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5  # Turn right
        else:
            # Move forward
            cmd.linear.x = 0.5
            cmd.angular.z = 0.0

        self.cmd_vel_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    navigator = GazeboNavigator()

    try:
        rclpy.spin(navigator)
    except KeyboardInterrupt:
        navigator.get_logger().info('Navigation stopped by user')
    finally:
        # Stop the robot before exiting
        stop_msg = Twist()
        navigator.cmd_vel_pub.publish(stop_msg)
        navigator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Advanced Gazebo Features

### Custom Plugins

Gazebo plugins extend functionality:

```cpp
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

namespace gazebo
{
  class CustomRobotPlugin : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the model pointer for convenience
      this->model = _parent;

      // Listen to the update event. This event is broadcast every
      // simulation iteration.
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&CustomRobotPlugin::OnUpdate, this));
    }

    // Called by the world update start event
    public: void OnUpdate()
    {
      // Apply a small linear velocity to the model
      this->model->SetLinearVel(ignition::math::Vector3d(0.3, 0, 0));
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(CustomRobotPlugin)
}
```

### Sensor Simulation

Gazebo provides realistic sensor simulation:

- **Camera Sensors**: RGB, depth, and stereo cameras
- **LIDAR**: 2D and 3D LIDAR with configurable parameters
- **IMU**: Inertial measurement units
- **GPS**: Global positioning system
- **Force/Torque**: Force and torque sensors
- **Contact Sensors**: Detect collisions and contacts

## Performance Optimization

### Physics Settings

Optimize physics simulation for your needs:

```xml
<physics type="ode">
  <!-- Smaller step size for accuracy -->
  <max_step_size>0.001</max_step_size>

  <!-- Real-time factor (1.0 = real-time) -->
  <real_time_factor>1.0</real_time_factor>

  <!-- Update rate -->
  <real_time_update_rate>1000</real_time_update_rate>

  <!-- Solver settings -->
  <ode>
    <solver>
      <type>quick</type>
      <iters>10</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Best Practices

1. **Model Simplification**: Use simplified collision geometries for performance
2. **Sensor Optimization**: Configure sensors with appropriate update rates
3. **World Design**: Create realistic but performance-friendly environments
4. **Validation**: Compare simulation results with real-world data
5. **Testing**: Test edge cases and failure scenarios in simulation

## Summary

Gazebo provides a powerful simulation environment for robotics development. The next chapter will cover Unity integration for visually rich environments.