# Data Model: ROS 2 Nervous System Module

## Key Entities

### ROS 2 Node
- **Description**: A process that performs computation, implementing the communication primitives of ROS 2
- **Attributes**:
  - node_id: string (unique identifier)
  - name: string (node name)
  - namespace: string (optional namespace)
  - publishers: list of Publisher
  - subscribers: list of Subscriber
  - services: list of Service
  - parameters: map of string to value
- **Relationships**:
  - Contains many Publishers
  - Contains many Subscribers
  - Contains many Services
- **Validation Rules**:
  - Name must be unique within namespace
  - Node must have at least one communication primitive (publisher, subscriber, or service)

### ROS 2 Topic
- **Description**: A named bus over which nodes exchange messages in a publish/subscribe pattern
- **Attributes**:
  - topic_name: string (unique name)
  - message_type: string (type of messages)
  - publishers_count: integer (number of publishers)
  - subscribers_count: integer (number of subscribers)
  - qos_profile: QoSProfile (quality of service settings)
- **Relationships**:
  - Connected to many Publishers
  - Connected to many Subscribers

### ROS 2 Service
- **Description**: A request/reply communication pattern between nodes for remote procedure calls
- **Attributes**:
  - service_name: string (unique name)
  - request_type: string (type of request message)
  - response_type: string (type of response message)
  - server: Node (the node providing the service)
  - clients: list of Node (nodes using the service)
- **Relationships**:
  - Belongs to one Server Node
  - Connected to many Client Nodes

### URDF Definition
- **Description**: An XML-based format that describes robot geometry, kinematics, and dynamics
- **Attributes**:
  - urdf_id: string (unique identifier)
  - name: string (robot name)
  - links: list of Link
  - joints: list of Joint
  - materials: list of Material
  - content: string (raw XML content)
  - validation_status: enum (valid, invalid, unvalidated)
- **Relationships**:
  - Contains many Links
  - Contains many Joints
  - Contains many Materials

### Link
- **Description**: A rigid component of a robot in URDF
- **Attributes**:
  - link_id: string (unique identifier)
  - name: string (link name)
  - visual: Visual (visual representation)
  - collision: Collision (collision representation)
  - inertial: Inertial (inertial properties)
- **Relationships**:
  - Belongs to one URDF Definition
  - Connected to many Joints (as parent or child)

### Joint
- **Description**: Connection between two links in URDF
- **Attributes**:
  - joint_id: string (unique identifier)
  - name: string (joint name)
  - type: enum (revolute, continuous, prismatic, fixed, floating, planar)
  - parent_link: Link (parent link)
  - child_link: Link (child link)
  - origin: Pose (position and orientation)
  - axis: Vector3 (joint axis)
- **Relationships**:
  - Belongs to one URDF Definition
  - Connected to two Links (parent and child)

### rclpy
- **Description**: Python client library for ROS 2 that enables Python programs to interact with ROS 2
- **Attributes**:
  - version: string (library version)
  - supported_python_versions: list of string
  - supported_ros2_distributions: list of string
  - functionality: list of string (publishers, subscribers, services, etc.)
- **Relationships**:
  - Used by Python Nodes
  - Interfaces with ROS 2 middleware

## State Transitions

### Node State Transitions
- CREATED → ACTIVE (when node is initialized and ready)
- ACTIVE → INACTIVE (when node is paused)
- INACTIVE → ACTIVE (when node resumes)
- ACTIVE → FINALIZED (when node is destroyed)

### URDF Validation State Transitions
- UNVALIDATED → VALID (when URDF passes validation)
- UNVALIDATED → INVALID (when URDF fails validation)
- INVALID → VALID (when invalid URDF is corrected)
- VALID → INVALID (when valid URDF is modified incorrectly)

## Entity Relationships

```
[Node] 1---* [Publisher] ---* [Topic]
[Node] 1---* [Subscriber] ---* [Topic]
[Node] 1---* [Service] ---1 [Node] (server-client relationship)
[URDF Definition] 1---* [Link]
[URDF Definition] 1---* [Joint]
[Link] *---* [Joint] (each joint connects two links)
```

## Validation Rules

### Node Validation
- Node name must follow ROS naming conventions
- Node must initialize successfully with ROS 2 middleware
- Node must properly handle lifecycle transitions

### Topic Validation
- Topic name must follow ROS naming conventions
- Message types must be compatible between publishers and subscribers
- QoS profiles must be compatible between publishers and subscribers

### URDF Validation
- All XML must be well-formed
- All referenced links in joints must exist
- No circular dependencies in joint connections
- Valid geometry specifications
- Valid material references