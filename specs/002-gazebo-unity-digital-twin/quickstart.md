# Quickstart Guide: Gazebo Unity Digital Twin Module

## Overview
This guide provides a quick introduction to setting up and working with the Gazebo Unity Digital Twin module. This module teaches students how to create physics simulations in Gazebo and visualize them with Unity for digital twin applications.

## Prerequisites
- Basic understanding of robotics concepts
- Computer with Ubuntu 22.04 or Windows 10/11 for Unity
- At least 8GB RAM (16GB recommended for Unity)
- Graphics card supporting OpenGL 3.3+ for Gazebo, DirectX 11+ for Unity

## Development Environment Setup

### 1. Gazebo Installation
```bash
# For Ubuntu 22.04
sudo apt update
sudo apt install gazebo libgazebo-dev

# Or install ROS 2 Humble with Gazebo integration
sudo apt install ros-humble-gazebo-*
```

### 2. Unity Installation
```bash
# Download Unity Hub from unity.com
# Install Unity 2022.3 LTS or newer
# Add the Robotics package through Unity Package Manager
```

### 3. Docusaurus Documentation Setup
```bash
# Install Node.js 18+
# Clone or navigate to the documentation repository
cd docs

# Install dependencies
npm install

# Start local development server
npm start
```

### 4. Project Structure
```
physical_ai_book/
├── docs/
│   └── modules/
│       └── 02-gazebo-unity-digital-twin/
│           ├── index.md
│           ├── chapter-1-gazebo-fundamentals.md
│           ├── chapter-2-building-environments.md
│           ├── chapter-3-sensor-simulation.md
│           └── chapter-4-unity-integration.md
├── static/
│   ├── img/
│   ├── models/
│   └── worlds/
├── src/
│   └── components/
├── backend/
│   └── src/
│       └── api/
└── specs/
    └── 02-gazebo-unity-digital-twin/
```

## Chapter 1: Gazebo Fundamentals

### Creating Your First World
```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="simple_world">
    <!-- Define physics engine -->
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Add a ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Add a simple box -->
    <model name="box">
      <pose>0 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box><size>1 1 1</size></box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box><size>1 1 1</size></box>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

### Running the Simulation
```bash
# Launch Gazebo with your world file
gz sim -r simple_world.sdf

# Or using legacy command
gazebo --verbose simple_world.sdf
```

## Chapter 2: Building Environments

### Creating a Complex Environment
```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="robot_environment">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Outdoor environment with lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Terrain model -->
    <model name="terrain">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <heightmap>
              <uri>model://terrain/heightmap.png</uri>
            </heightmap>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <heightmap>
              <uri>model://terrain/heightmap.png</uri>
            </heightmap>
          </geometry>
        </visual>
      </link>
    </model>

    <!-- Objects for robot interaction -->
    <model name="table">
      <pose>2 0 0 0 0 0</pose>
      <!-- ... table definition ... -->
    </model>
  </world>
</sdf>
```

## Chapter 3: Sensor Simulation

### Adding a LiDAR Sensor
```xml
<model name="lidar_robot">
  <link name="chassis">
    <!-- Chassis definition -->
  </link>

  <link name="lidar_link">
    <sensor name="lidar" type="ray">
      <ray>
        <scan>
          <horizontal>
            <samples>360</samples>
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>10.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin filename="libgazebo_ros_ray_sensor.so" name="gazebo_ros_lidar">
        <ros>
          <namespace>lidar_robot</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
      </plugin>
    </sensor>
  </link>
</model>
```

### Customizable Noise Model
```xml
<sensor name="noisy_camera" type="camera">
  <camera>
    <!-- Camera parameters -->
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </camera>
</sensor>
```

## Chapter 4: Unity Integration

### Basic Unity Visualization Setup
```csharp
using UnityEngine;
using System.Collections.Generic;

public class GazeboUnityBridge : MonoBehaviour
{
    [Header("Gazebo Connection")]
    public string gazeboSimulationId;
    public float updateRateHz = 30.0f;

    [Header("Object Mapping")]
    public Dictionary<string, GameObject> objectMap = new Dictionary<string, GameObject>();

    private float lastUpdateTime;

    void Start()
    {
        lastUpdateTime = Time.time;
        ConnectToGazebo();
    }

    void Update()
    {
        if (Time.time - lastUpdateTime >= 1.0f / updateRateHz)
        {
            UpdateFromGazebo();
            lastUpdateTime = Time.time;
        }
    }

    private void ConnectToGazebo()
    {
        // Implementation to connect to Gazebo simulation
        Debug.Log($"Connecting to Gazebo simulation: {gazeboSimulationId}");
    }

    private void UpdateFromGazebo()
    {
        // Fetch simulation state from API and update Unity objects
        // This would call the API endpoint: /api/v1/simulations/{id}/state
    }
}
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
# Get simulation state
curl -X GET "http://localhost:3000/api/v1/simulations/test-sim/state" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Unity assets
curl -X GET "http://localhost:3000/api/v1/unity/assets?category=models" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Validate Simulation Configuration
```bash
# Validate SDF files
gz sdf -k world_file.sdf

# Check model files
gz model --info model_name
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
npm run validate:links
npm run validate:mdx
npm run validate:images
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
1. Complete all chapters in the Gazebo Unity Digital Twin module
2. Integrate with the RAG chatbot for interactive learning
3. Deploy documentation to GitHub Pages
4. Test with actual Gazebo and Unity environments