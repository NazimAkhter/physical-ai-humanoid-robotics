# Chapter 3: Robot Modeling

## Overview

This chapter covers the principles and techniques for creating accurate robot models for both Gazebo and Unity simulation environments, ensuring consistency across different simulation platforms.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Create accurate 3D robot models using CAD tools and mesh formats
2. Define proper physical properties for simulation accuracy
3. Implement collision and visual geometries for different simulation needs
4. Optimize models for performance in both Gazebo and Unity environments

## Robot Modeling Fundamentals

### Coordinate Systems

Understanding coordinate systems is crucial for accurate robot modeling:

- **ROS Coordinate System**: Right-handed (X-forward, Y-left, Z-up)
- **Unity Coordinate System**: Left-handed (X-right, Y-up, Z-forward)
- **Gazebo Coordinate System**: Right-handed (X-forward, Y-left, Z-up)

### Robot Model Structure

A complete robot model typically includes:

```
robot_name/
├── meshes/
│   ├── visual/
│   │   ├── base_link.dae
│   │   ├── wheel_link.stl
│   │   └── sensor_link.obj
│   └── collision/
│       ├── base_link_convex.stl
│       └── wheel_link_simple.stl
├── urdf/
│   └── robot_name.urdf
└── config/
    └── joint_limits.yaml
```

## CAD Modeling for Robotics

### Design Principles

When designing robots for simulation:

1. **Accuracy**: Model dimensions must match the real robot
2. **Simplicity**: Balance detail with performance requirements
3. **Modularity**: Design components that can be easily modified
4. **Assembly**: Consider how parts connect and move relative to each other

### CAD Tools for Robot Modeling

Popular tools for creating robot models:
- **FreeCAD**: Open-source parametric CAD
- **Fusion 360**: Professional CAD with simulation features
- **Blender**: 3D modeling with robotics plugins
- **SolidWorks**: Professional CAD with URDF export

### Example CAD Workflow

1. **Concept Design**: Create basic shapes and dimensions
2. **Detailed Design**: Add features, mounting points, and interfaces
3. **Assembly**: Connect components with proper joints and constraints
4. **Export**: Export to appropriate formats (STL, DAE, OBJ)

## URDF (Unified Robot Description Format)

### URDF Structure

```xml
<?xml version="1.0"?>
<robot name="example_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Base Link Definition -->
  <link name="base_link">
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <inertia ixx="0.4" ixy="0.0" ixz="0.0" iyy="0.4" iyz="0.0" izz="0.2"/>
    </inertial>

    <visual>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://example_robot/meshes/visual/base_link.dae"/>
      </geometry>
      <material name="blue">
        <color rgba="0.0 0.0 1.0 1.0"/>
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0.1" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://example_robot/meshes/collision/base_link_convex.stl"/>
      </geometry>
    </collision>
  </link>

  <!-- Wheel Links -->
  <link name="wheel_left_link">
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.02"/>
    </inertial>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://example_robot/meshes/visual/wheel_left.dae"/>
      </geometry>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
  </link>

  <!-- Joints -->
  <joint name="wheel_left_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_left_link"/>
    <origin xyz="0 0.3 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <dynamics damping="0.1"/>
  </joint>

  <!-- Gazebo-specific elements -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="wheel_left_link">
    <mu1>1.0</mu1>
    <mu2>1.0</mu2>
    <kp>1000000.0</kp>
    <kd>100.0</kd>
  </gazebo>
</robot>
```

### Inertial Properties

Proper inertial properties are critical for realistic simulation:

```xml
<inertial>
  <!-- Mass in kg -->
  <mass value="1.0"/>

  <!-- Origin offset from link frame -->
  <origin xyz="0 0 0.1" rpy="0 0 0"/>

  <!-- Inertia matrix (3x3 symmetric) -->
  <inertia
    ixx="0.4" ixy="0.0" ixz="0.0"
    iyy="0.4" iyz="0.0"
    izz="0.2"/>
</inertial>
```

### Joint Types

Different joint types for various robot mechanisms:

- **Fixed**: Rigid connection (no movement)
- **Revolute**: Rotational joint with limits
- **Continuous**: Rotational joint without limits
- **Prismatic**: Linear sliding joint
- **Floating**: 6-DOF movement
- **Planar**: Movement in a plane

## Mesh Optimization

### Visual vs Collision Meshes

Use different meshes for visual and collision purposes:

#### Visual Meshes
- High detail for rendering
- Textures and materials
- Smooth surfaces
- Higher polygon count acceptable

#### Collision Meshes
- Simplified geometry
- Convex hulls when possible
- Lower polygon count
- Fast collision detection

### Mesh Formats

Supported formats in robotics:

- **STL**: Simple, widely supported, good for collision
- **DAE**: Collada format, supports textures and materials
- **OBJ**: Wavefront format, simple and versatile
- **PLY**: Polygon file format, good for point clouds

### Example Mesh Optimization

```bash
# Simplify mesh using meshlabserver
meshlabserver -i input.obj -o output.obj -s simplify.mlx

# Convert between formats
# Using Python with trimesh
import trimesh
mesh = trimesh.load('input.stl')
mesh.simplify_quadric_decimation(face_count=1000)
mesh.export('output.stl')
```

## Gazebo-Specific Modeling

### Gazebo Tags in URDF

```xml
<gazebo reference="link_name">
  <!-- Material -->
  <material>Gazebo/Blue</material>

  <!-- Physics properties -->
  <mu1>1.0</mu1>          <!-- Friction coefficient 1 -->
  <mu2>1.0</mu2>          <!-- Friction coefficient 2 -->
  <kp>1000000.0</kp>      <!-- Spring stiffness -->
  <kd>100.0</kd>          <!-- Damping coefficient -->
  <fdir1>0 0 1</fdir1>    <!-- Friction direction -->

  <!-- Self-collision -->
  <self_collide>true</self_collide>

  <!-- Gravity -->
  <gravity>true</gravity>

  <!-- Turn off collision -->
  <disable_fixed_joint_lumping>true</disable_fixed_joint_lumping>
</gazebo>
```

### Sensor Integration

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.02 0.08 0.04"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <box size="0.02 0.08 0.04"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
  </inertial>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera_link"/>
  <origin xyz="0.2 0 0.1" rpy="0 0 0"/>
</joint>

<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>camera</namespace>
        <remapping>~/image_raw:=image</remapping>
        <remapping>~/camera_info:=camera_info</remapping>
      </ros>
      <camera_name>camera</camera_name>
      <image_topic_name>image</image_topic_name>
      <camera_info_topic_name>camera_info</camera_info_topic_name>
      <frame_name>camera_link</frame_name>
      <hack_baseline>0.07</hack_baseline>
      <distortion_k1>0.0</distortion_k1>
      <distortion_k2>0.0</distortion_k2>
      <distortion_k3>0.0</distortion_k3>
      <distortion_t1>0.0</distortion_t1>
      <distortion_t2>0.0</distortion_t2>
    </plugin>
  </sensor>
</gazebo>
```

## Unity Robot Modeling

### Unity Robot Components

```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class UnityRobotModel : MonoBehaviour
{
    [Header("Robot Configuration")]
    public RobotJoint[] joints;
    public RobotSensor[] sensors;
    public RobotWheel[] wheels;

    [Header("Physics Settings")]
    public float mass = 10.0f;
    public bool useGravity = true;
    public bool isKinematic = false;

    Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        ConfigurePhysics();
        InitializeComponents();
    }

    void ConfigurePhysics()
    {
        rb.mass = mass;
        rb.useGravity = useGravity;
        rb.isKinematic = isKinematic;
    }

    void InitializeComponents()
    {
        foreach (var joint in joints)
        {
            joint.Initialize();
        }

        foreach (var sensor in sensors)
        {
            sensor.Initialize();
        }

        foreach (var wheel in wheels)
        {
            wheel.Initialize();
        }
    }
}

[System.Serializable]
public class RobotJoint
{
    public string name;
    public Transform jointTransform;
    public JointType jointType;
    public float minLimit;
    public float maxLimit;
    public float velocity;

    public void Initialize()
    {
        // Configure joint based on type
        switch (jointType)
        {
            case JointType.Revolute:
                ConfigureRevoluteJoint();
                break;
            case JointType.Prismatic:
                ConfigurePrismaticJoint();
                break;
        }
    }

    void ConfigureRevoluteJoint()
    {
        var hingeJoint = jointTransform.GetComponent<HingeJoint>();
        if (hingeJoint != null)
        {
            var limits = hingeJoint.limits;
            limits.min = minLimit;
            limits.max = maxLimit;
            hingeJoint.limits = limits;
            hingeJoint.useLimits = true;
        }
    }

    void ConfigurePrismaticJoint()
    {
        // Configure for prismatic movement
        var joint = jointTransform.GetComponent<ConfigurableJoint>();
        if (joint != null)
        {
            joint.xMotion = ConfigurableJointMotion.Limited;
            joint.linearLimit = new SoftJointLimit { limit = maxLimit };
        }
    }
}

public enum JointType
{
    Fixed,
    Revolute,
    Continuous,
    Prismatic,
    Floating,
    Planar
}
```

### Collision Optimization in Unity

```csharp
using UnityEngine;

public class RobotCollisionOptimizer : MonoBehaviour
{
    [Header("Collision Settings")]
    public CollisionType collisionType = CollisionType.Mesh;
    public int maxTriangleCount = 1000;
    public bool useConvexHull = true;

    void Start()
    {
        OptimizeColliders();
    }

    void OptimizeColliders()
    {
        var meshFilters = GetComponentsInChildren<MeshFilter>();

        foreach (var meshFilter in meshFilters)
        {
            var meshCollider = meshFilter.gameObject.GetComponent<MeshCollider>();

            if (meshCollider != null)
            {
                var mesh = meshFilter.sharedMesh;

                if (mesh.triangles.Length > maxTriangleCount)
                {
                    // Use convex hull for performance
                    meshCollider.convex = useConvexHull;

                    if (useConvexHull)
                    {
                        // For complex meshes, use primitive colliders when possible
                        ReplaceWithPrimitiveCollider(meshFilter.gameObject, mesh);
                    }
                }
            }
        }
    }

    void ReplaceWithPrimitiveCollider(GameObject obj, Mesh mesh)
    {
        // Remove mesh collider
        var meshCollider = obj.GetComponent<MeshCollider>();
        if (meshCollider != null)
            DestroyImmediate(meshCollider);

        // Add appropriate primitive collider
        if (IsBoxShaped(mesh))
        {
            obj.AddComponent<BoxCollider>();
        }
        else if (IsCylinderShaped(mesh))
        {
            obj.AddComponent<CapsuleCollider>();
        }
        else
        {
            // Keep mesh collider but make it convex if possible
            var newMeshCollider = obj.AddComponent<MeshCollider>();
            newMeshCollider.convex = useConvexHull && IsConvexCapable(mesh);
        }
    }

    bool IsBoxShaped(Mesh mesh)
    {
        // Simplified check - in practice, you'd do more sophisticated geometry analysis
        return mesh.vertices.Length <= 8;
    }

    bool IsCylinderShaped(Mesh mesh)
    {
        // Simplified check
        return mesh.vertices.Length > 8 && mesh.vertices.Length <= 24;
    }

    bool IsConvexCapable(Mesh mesh)
    {
        // Check if mesh can be made convex
        return mesh.vertices.Length <= 255; // Unity limit for convex meshes
    }
}
```

## Model Validation and Testing

### Validation Checklist

```python
import xml.etree.ElementTree as ET
import os

def validate_urdf_model(urdf_path):
    """Validate URDF model for common issues"""
    try:
        tree = ET.parse(urdf_path)
        root = tree.getroot()

        issues = []

        # Check for proper robot tag
        if root.tag != 'robot':
            issues.append("URDF must have 'robot' as root element")

        # Check for robot name
        if 'name' not in root.attrib:
            issues.append("Robot must have a name attribute")

        # Check links and joints
        links = root.findall('link')
        joints = root.findall('joint')

        if len(links) == 0:
            issues.append("Robot must have at least one link")

        # Validate joint-parent relationships
        link_names = [link.get('name') for link in links]
        for joint in joints:
            parent = joint.find('parent')
            child = joint.find('child')

            if parent is not None and parent.get('link') not in link_names:
                issues.append(f"Joint {joint.get('name')} has invalid parent link")

            if child is not None and child.get('link') not in link_names:
                issues.append(f"Joint {joint.get('name')} has invalid child link")

        return len(issues) == 0, issues

    except ET.ParseError as e:
        return False, [f"XML Parse Error: {str(e)}"]
    except Exception as e:
        return False, [f"Validation Error: {str(e)}"]

def check_mesh_files(urdf_path):
    """Check if all referenced mesh files exist"""
    import re

    with open(urdf_path, 'r') as f:
        content = f.read()

    # Find all mesh references
    mesh_pattern = r'filename="([^"]*\.(dae|stl|obj|ply))"'
    mesh_refs = re.findall(mesh_pattern, content)

    missing_files = []
    for mesh_ref, ext in mesh_refs:
        # Handle package:// references
        if mesh_ref.startswith('package://'):
            # Convert to actual file path
            actual_path = mesh_ref.replace('package://', './')
            if not os.path.exists(actual_path):
                missing_files.append(actual_path)

    return len(missing_files) == 0, missing_files
```

## Performance Optimization

### Level of Detail (LOD) for Robot Models

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "RobotLODSettings", menuName = "Robotics/LOD Settings")]
public class RobotLODSettings : ScriptableObject
{
    [Header("LOD Configuration")]
    public float[] distances = { 5f, 15f, 30f };
    public GameObject[] lodMeshes;
    public Material[] lodMaterials;

    [Header("Performance Settings")]
    public bool enableLOD = true;
    public float lodFadeTime = 0.5f;
}

public class RobotLODController : MonoBehaviour
{
    public RobotLODSettings lodSettings;
    private LODGroup lodGroup;
    private LOD[] lods;

    void Start()
    {
        SetupLOD();
    }

    void SetupLOD()
    {
        if (lodSettings == null || !lodSettings.enableLOD) return;

        lodGroup = GetComponent<LODGroup>();
        if (lodGroup == null)
            lodGroup = gameObject.AddComponent<LODGroup>();

        // Create LOD array
        lods = new LOD[lodSettings.lodMeshes.Length];

        for (int i = 0; i < lodSettings.lodMeshes.Length; i++)
        {
            var renderers = GetComponentsInChildren<Renderer>();

            // Create combined renderer for this LOD level
            var lodRenderer = new Renderer[renderers.Length];
            for (int j = 0; j < renderers.Length; j++)
            {
                var lodMesh = Instantiate(lodSettings.lodMeshes[i]);
                lodMesh.transform.SetParent(transform);
                lodRenderer[j] = lodMesh.GetComponent<Renderer>();
            }

            lods[i] = new LOD(lodSettings.distances[i], lodRenderer);
        }

        lodGroup.SetLODs(lods);
        lodGroup.RecalculateBounds();
    }
}
```

## Best Practices

1. **Consistency**: Maintain consistent coordinate systems across all models
2. **Validation**: Always validate URDF files before simulation
3. **Optimization**: Balance visual quality with simulation performance
4. **Documentation**: Document model parameters and assumptions
5. **Versioning**: Use version control for model files
6. **Testing**: Test models in both simulation environments
7. **Standards**: Follow ROS conventions for naming and structure

## Tools and Resources

### Model Creation Tools
- **Blender**: 3D modeling with robotics plugins
- **FreeCAD**: Parametric CAD design
- **MeshLab**: Mesh processing and optimization
- **Open3D**: 3D data processing library

### Validation Tools
- **check_urdf**: ROS tool for URDF validation
- **xacro**: XML macro language for URDF
- **URDF Viewer**: Visual URDF inspection tools

## Summary

Accurate robot modeling is fundamental to successful simulation. The next chapter will cover Unity Robotics Hub integration in more detail.