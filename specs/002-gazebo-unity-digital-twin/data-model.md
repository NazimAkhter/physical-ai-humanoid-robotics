# Data Model: Gazebo Unity Digital Twin Module

## Key Entities

### Gazebo World
- **Description**: A simulation environment containing physics properties, objects, and settings that define a robot testing space
- **Attributes**:
  - world_id: string (unique identifier)
  - name: string (world name)
  - physics_engine: string (type of physics engine used)
  - gravity: vector3 (gravity vector in x, y, z directions)
  - objects: list of GazeboObject
  - lighting: list of LightSource
  - terrain: TerrainModel (if applicable)
  - settings: map of string to value (physics and rendering settings)
- **Relationships**:
  - Contains many GazeboObjects
  - Contains many LightSources
  - May have one TerrainModel
- **Validation Rules**:
  - Name must be unique within the module
  - Gravity vector must have realistic values for simulation
  - Objects must have valid collision and visual properties

### GazeboObject
- **Description**: An object within a Gazebo simulation environment
- **Attributes**:
  - object_id: string (unique identifier)
  - name: string (object name)
  - model_type: string (type of model: primitive, SDF, URDF)
  - position: vector3 (x, y, z coordinates in world)
  - orientation: quaternion (rotation in world)
  - visual: VisualProperties (appearance settings)
  - collision: CollisionProperties (collision detection settings)
  - physics: PhysicsProperties (mass, friction, etc.)
- **Relationships**:
  - Belongs to one GazeboWorld
- **Validation Rules**:
  - Position must be within world boundaries
  - Must have valid visual and collision properties

### Sensor Model
- **Description**: A representation of physical sensors (LiDAR, Depth Cameras, IMUs) with noise models and data output characteristics
- **Attributes**:
  - sensor_id: string (unique identifier)
  - name: string (sensor name)
  - type: enum (LiDAR, DepthCamera, IMU, etc.)
  - parent_object: GazeboObject (the object the sensor is attached to)
  - position: vector3 (position relative to parent)
  - orientation: quaternion (orientation relative to parent)
  - noise_model: NoiseModel (noise characteristics)
  - output_format: string (format of sensor data)
  - parameters: map of string to value (sensor-specific parameters)
- **Relationships**:
  - Belongs to one GazeboObject (as attachment)
  - Has one NoiseModel
- **Validation Rules**:
  - Must be properly attached to a valid GazeboObject
  - Noise model must be appropriate for sensor type
  - Parameters must be valid for the sensor type

### NoiseModel
- **Description**: Configuration for simulating real-world sensor noise and inaccuracies
- **Attributes**:
  - noise_id: string (unique identifier)
  - type: enum (gaussian, uniform, custom)
  - mean: float (mean value for noise distribution)
  - std_dev: float (standard deviation for noise)
  - parameters: map of string to value (noise-specific parameters)
  - customizable: boolean (whether parameters can be adjusted by user)
- **Relationships**:
  - Used by many SensorModels
- **Validation Rules**:
  - Parameters must be valid for the specified noise type
  - Values must result in realistic sensor behavior

### Simulation Environment
- **Description**: A complete setup including terrain, objects, lighting, and physics parameters for robot testing
- **Attributes**:
  - env_id: string (unique identifier)
  - name: string (environment name)
  - world: GazeboWorld (the underlying world model)
  - complexity_level: enum (basic, intermediate, advanced, customizable)
  - terrain_type: string (flat, rough, urban, etc.)
  - objects_count: integer (number of objects in environment)
  - lighting_conditions: string (day, night, variable)
  - physics_parameters: map of string to value (custom physics settings)
- **Relationships**:
  - Contains one GazeboWorld
  - Contains many GazeboObjects (through the world)
- **Validation Rules**:
  - Complexity level must match the specified constraints
  - Must have valid physics parameters for stable simulation

### Unity Visualization
- **Description**: A high-fidelity visual representation that complements Gazebo simulation for enhanced user interaction
- **Attributes**:
  - viz_id: string (unique identifier)
  - name: string (visualization name)
  - gazebo_link: string (reference to linked Gazebo simulation)
  - rendering_quality: enum (low, medium, high, ultra)
  - interaction_modes: list of string (available interaction methods)
  - assets: list of UnityAsset
  - update_rate: float (how frequently it updates from Gazebo)
  - ros_integration: boolean (whether it connects to ROS)
- **Relationships**:
  - Links to one GazeboWorld
  - Contains many UnityAssets
- **Validation Rules**:
  - Must have valid link to a Gazebo simulation
  - Update rate must be reasonable for performance

### UnityAsset
- **Description**: A 3D model, material, or other asset used in Unity visualization
- **Attributes**:
  - asset_id: string (unique identifier)
  - name: string (asset name)
  - type: enum (model, material, texture, animation, prefab)
  - file_path: string (path to asset file)
  - size: float (file size in MB)
  - quality_settings: map of string to value (LOD, texture resolution, etc.)
- **Relationships**:
  - Belongs to many UnityVisualizations
- **Validation Rules**:
  - File path must exist and be accessible
  - Size must be reasonable for web/download constraints

### Digital Twin
- **Description**: An integrated system combining Gazebo physics simulation and Unity visualization for comprehensive robot testing
- **Attributes**:
  - twin_id: string (unique identifier)
  - name: string (digital twin name)
  - gazebo_component: GazeboWorld (physics simulation component)
  - unity_component: UnityVisualization (visualization component)
  - synchronization_mode: enum (real-time, batch, manual)
  - data_flow_direction: enum (gazebo-to-unity, bidirectional, unity-to-gazebo)
  - performance_metrics: map of string to value (FPS, update rates, etc.)
- **Relationships**:
  - Contains one GazeboWorld
  - Contains one UnityVisualization
- **Validation Rules**:
  - Both components must be properly configured
  - Synchronization must be technically feasible

## State Transitions

### Simulation Environment State Transitions
- CREATED → CONFIGURED (when all objects and settings are defined)
- CONFIGURED → RUNNING (when simulation is started)
- RUNNING → PAUSED (when simulation is paused)
- PAUSED → RUNNING (when simulation is resumed)
- RUNNING/PAUSED → STOPPED (when simulation ends)

### Digital Twin State Transitions
- DEFINED → SYNCHRONIZED (when Gazebo and Unity components are linked)
- SYNCHRONIZED → ACTIVE (when real-time data flow is established)
- ACTIVE → INACTIVE (when synchronization is paused)
- INACTIVE → ACTIVE (when synchronization is resumed)

## Entity Relationships

```
[GazeboWorld] 1---* [GazeboObject]
[GazeboWorld] 1---* [LightSource]
[GazeboWorld] 1---1 [TerrainModel]
[GazeboObject] *---1 [SensorModel]
[SensorModel] 1---1 [NoiseModel]
[SimulationEnvironment] 1---1 [GazeboWorld]
[UnityVisualization] *---* [UnityAsset]
[Digital Twin] 1---1 [GazeboWorld] + 1---1 [UnityVisualization]
```

## Validation Rules

### Gazebo World Validation
- World file must be valid SDF/XML
- All referenced models must exist
- Physics parameters must result in stable simulation
- Object positions must not result in initial collisions

### Sensor Model Validation
- Sensor must be properly mounted on a valid object
- Sensor parameters must be within realistic ranges
- Noise model must be appropriate for sensor type
- Output format must be compatible with expected consumers

### Unity Visualization Validation
- All referenced assets must exist and be properly formatted
- Rendering quality settings must be achievable on target hardware
- Update rate must be reasonable for performance
- ROS integration settings must be consistent with clarification decisions