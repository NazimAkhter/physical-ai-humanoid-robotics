# Data Model: Isaac AI Brain Module

## Key Entities

### Isaac Sim Scene
- **Description**: A photorealistic simulation environment containing objects, lighting, materials, and physics properties that generate synthetic training data
- **Attributes**:
  - scene_id: string (unique identifier)
  - name: string (scene name)
  - description: string (brief description of the scene)
  - lighting_config: object (lighting setup parameters)
  - objects: list of SceneObject
  - physics_properties: object (gravity, friction, etc.)
  - synthetic_data_config: object (annotation and output settings)
  - complexity_level: enum (basic, intermediate, advanced)
  - rendering_quality: enum (low, medium, high, ultra)
- **Relationships**:
  - Contains many SceneObjects
  - Generates many SyntheticDatasets
- **Validation Rules**:
  - Name must be unique within the module
  - Lighting configuration must be valid for Isaac Sim
  - Objects must have proper collision and visual properties

### SceneObject
- **Description**: An object within an Isaac Sim scene
- **Attributes**:
  - object_id: string (unique identifier)
  - name: string (object name)
  - model_type: string (type of model: primitive, USD, OBJ, etc.)
  - position: vector3 (x, y, z coordinates in scene)
  - orientation: quaternion (rotation in scene)
  - visual: VisualProperties (appearance settings)
  - collision: CollisionProperties (collision detection settings)
  - physics: PhysicsProperties (mass, friction, etc.)
  - material: MaterialProperties (textures, shaders, etc.)
- **Relationships**:
  - Belongs to one IsaacSimScene
- **Validation Rules**:
  - Position must be within scene boundaries
  - Must have valid visual and collision properties

### VSLAM Pipeline
- **Description**: A system that processes visual input to simultaneously localize the camera and map the environment in real-time
- **Attributes**:
  - pipeline_id: string (unique identifier)
  - name: string (pipeline name)
  - algorithm_type: string (ORB-SLAM, LSD-SLAM, etc.)
  - camera_config: object (camera intrinsic/extrinsic parameters)
  - feature_detector: string (type of feature detector used)
  - matcher: string (type of descriptor matcher)
  - optimizer: string (type of pose optimizer)
  - tracking_accuracy: float (accuracy metric)
  - computational_requirements: object (CPU/GPU requirements)
  - parameters: map of string to value (algorithm-specific parameters)
- **Relationships**:
  - Processes many VisualInputs
  - Produces many PoseEstimates and Maps
- **Validation Rules**:
  - Camera configuration must match input data format
  - Parameters must be valid for the chosen algorithm type

### Isaac ROS Perception Node
- **Description**: A ROS 2 node that implements hardware-accelerated computer vision algorithms for robot perception
- **Attributes**:
  - node_id: string (unique identifier)
  - name: string (node name)
  - node_type: string (feature_tracker, object_detector, depth_processor, etc.)
  - input_topics: list of string (ROS topics the node subscribes to)
  - output_topics: list of string (ROS topics the node publishes to)
  - computational_requirements: object (GPU acceleration requirements)
  - processing_rate: float (frames per second)
  - parameters: map of string to value (node-specific parameters)
  - hardware_acceleration: string (CUDA, TensorRT, etc.)
- **Relationships**:
  - Connects to many other ROS nodes
  - Processes many PerceptionMessages
- **Validation Rules**:
  - Input/output topics must follow ROS 2 conventions
  - Hardware acceleration settings must be available on target systems

### Nav2 Navigation System
- **Description**: A navigation stack that includes mapping, path planning, and motion control for autonomous robot navigation
- **Attributes**:
  - system_id: string (unique identifier)
  - name: string (system name)
  - map_config: object (map settings and parameters)
  - planner_config: object (path planning algorithm settings)
  - controller_config: object (motion controller settings)
  - recovery_config: object (recovery behavior settings)
  - costmap_config: object (costmap parameters)
  - robot_config: object (robot-specific parameters)
  - safety_limits: object (velocity, acceleration, etc.)
- **Relationships**:
  - Contains many Nav2Modules (mapper, planner, controller)
  - Processes many NavigationRequests
- **Validation Rules**:
  - All configurations must be valid Nav2 parameters
  - Safety limits must be within robot capabilities

### Synthetic Dataset
- **Description**: A collection of artificially generated data that mimics real-world sensor inputs for training AI models
- **Attributes**:
  - dataset_id: string (unique identifier)
  - name: string (dataset name)
  - scene: IsaacSimScene (source scene)
  - data_type: enum (images, depth_maps, point_clouds, annotations)
  - size: float (size in GB)
  - annotation_format: string (format of annotations)
  - image_resolution: object (width and height of images)
  - frame_count: integer (number of frames in dataset)
  - generation_date: string (date of dataset creation)
  - quality_metrics: object (sharpness, noise levels, etc.)
- **Relationships**:
  - Generated from one IsaacSimScene
  - Used by many TrainingModels
- **Validation Rules**:
  - Must have valid source scene reference
  - Size must be reasonable for storage and transfer

### Pose Estimate
- **Description**: An estimation of camera/robot position and orientation in the environment
- **Attributes**:
  - estimate_id: string (unique identifier)
  - timestamp: number (time of estimation)
  - position: vector3 (x, y, z coordinates)
  - orientation: quaternion (rotation as quaternion)
  - covariance: matrix (uncertainty in the estimate)
  - tracking_confidence: float (confidence level of the estimate)
  - source_pipeline: VSLAMPipeline (pipeline that generated the estimate)
  - frame_id: string (coordinate frame identifier)
- **Relationships**:
  - Generated by one VSLAMPipeline
  - Part of one Map
- **Validation Rules**:
  - Position and orientation must be mathematically valid
  - Covariance matrix must be positive semi-definite

### Navigation Request
- **Description**: A request for the Nav2 system to navigate to a specific goal location
- **Attributes**:
  - request_id: string (unique identifier)
  - goal_position: vector3 (x, y, theta coordinates of goal)
  - start_position: vector3 (x, y, theta coordinates of start)
  - timestamp: string (time of request)
  - status: enum (pending, active, succeeded, failed, cancelled)
  - path: list of vector2 (planned path waypoints)
  - completion_percentage: float (percentage of path completed)
  - navigation_system: Nav2NavigationSystem (system handling the request)
- **Relationships**:
  - Handled by one Nav2NavigationSystem
  - May generate many PathUpdates
- **Validation Rules**:
  - Goal and start positions must be within map boundaries
  - Status transitions must follow valid state machine rules

## State Transitions

### Navigation Request State Transitions
- PENDING → ACTIVE (when navigation begins)
- ACTIVE → SUCCEEDED (when goal reached successfully)
- ACTIVE → FAILED (when navigation fails)
- ACTIVE → CANCELLED (when request cancelled by user)
- FAILED → PENDING (when retry is initiated)

### VSLAM Pipeline State Transitions
- INITIALIZED → TRACKING (when visual input starts)
- TRACKING → LOST (when tracking fails)
- LOST → TRACKING (when tracking recovers)
- TRACKING → PAUSED (when tracking is paused)
- PAUSED → TRACKING (when tracking resumes)

## Entity Relationships

```
[IsaacSimScene] 1---* [SceneObject]
[IsaacSimScene] *---* [SyntheticDataset]
[VSLAMPipeline] *---* [PoseEstimate]
[VSLAMPipeline] *---* [Map]
[IsaacROSPerceptionNode] *---* [PerceptionMessage]
[Nav2NavigationSystem] 1---* [Nav2Module]
[Nav2NavigationSystem] *---* [NavigationRequest]
[SyntheticDataset] *---* [TrainingModel]
[PoseEstimate] 1---* [Map]
[NavigationRequest] 1---* [PathUpdate]
```

## Validation Rules

### Isaac Sim Scene Validation
- Scene must have valid USD or compatible format
- All referenced assets must exist and be accessible
- Physics parameters must result in stable simulation
- Object positions must not result in initial collisions
- Rendering quality settings must be achievable on target hardware

### VSLAM Pipeline Validation
- Camera configuration must match input data format
- Algorithm parameters must be within valid ranges
- Computational requirements must be available on target system
- Tracking accuracy must meet minimum thresholds

### Isaac ROS Perception Node Validation
- All ROS topic names must follow ROS 2 naming conventions
- Input/output message types must be compatible
- Hardware acceleration settings must be available
- Processing rate must be achievable with available resources

### Nav2 Navigation System Validation
- All configuration files must be valid YAML
- Map must be properly formatted and accessible
- Robot parameters must be within physical limits
- Safety limits must be appropriate for robot hardware