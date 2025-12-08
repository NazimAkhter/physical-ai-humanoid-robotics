# Chapter 2: Unity Integration

## Overview

This chapter explores Unity as a platform for creating visually rich digital twins and simulation environments for robotics applications, complementing physics-accurate Gazebo simulation.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Set up Unity for robotics simulation and visualization
2. Create visually appealing digital twin environments
3. Integrate Unity with ROS 2 for bidirectional communication
4. Implement custom Unity components for robotics applications

## Introduction to Unity for Robotics

Unity is a powerful game engine that has been adapted for robotics applications through the Unity Robotics Hub, providing:
- High-quality 3D visualization and rendering
- Physics simulation capabilities
- Flexible environment creation tools
- Extensive asset library
- Cross-platform deployment options

### Unity Robotics Hub

The Unity Robotics Hub provides specialized tools for robotics:
- **ROS-TCP-Connector**: Enables communication between Unity and ROS 2
- **URDF-Importer**: Imports robot models from URDF files
- **Robotics Examples**: Sample scenes and components for robotics applications

## Setting Up Unity for Robotics

### Installation Requirements

1. Unity Hub (latest LTS version)
2. Unity Editor (2021.3 LTS or newer recommended)
3. Unity Robotics Hub package
4. ROS 2 environment (for integration)

### Unity Robotics Hub Installation

1. Open Unity Hub and create a new 3D project
2. In the Package Manager, install:
   - ROS-TCP-Connector
   - URDF-Importer
   - Robotics Examples (optional)

### Basic Project Setup

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class RobotController : MonoBehaviour
{
    // ROS connection
    ROSConnection ros;

    // Robot properties
    public string robotName = "my_robot";
    public float linearVelocity = 1.0f;
    public float angularVelocity = 1.0f;

    // ROS topics
    string cmdVelTopic = "/cmd_vel";

    void Start()
    {
        // Initialize ROS connection
        ros = ROSConnection.GetOrCreateInstance();
        ros.RegisterPublisher<TwistMsg>(cmdVelTopic);
    }

    void Update()
    {
        // Process input and send commands to ROS
        ProcessInput();
    }

    void ProcessInput()
    {
        // Example: Use keyboard input for testing
        float linear = 0f;
        float angular = 0f;

        if (Input.GetKey(KeyCode.W))
            linear = linearVelocity;
        else if (Input.GetKey(KeyCode.S))
            linear = -linearVelocity;

        if (Input.GetKey(KeyCode.A))
            angular = angularVelocity;
        else if (Input.GetKey(KeyCode.D))
            angular = -angularVelocity;

        // Send command to ROS
        if (linear != 0 || angular != 0)
        {
            var twist = new TwistMsg();
            twist.linear = new Vector3Msg(linear, 0, 0);
            twist.angular = new Vector3Msg(0, 0, angular);

            ros.Publish(cmdVelTopic, twist);
        }
    }
}
```

## URDF Import and Robot Setup

### Importing URDF Models

Unity's URDF Importer allows direct import of robot models:

```csharp
using Unity.Robotics.URDFImport;
using UnityEngine;

public class RobotImporter : MonoBehaviour
{
    [Header("URDF Settings")]
    public string urdfPath;
    public bool optimizeScene = true;
    public bool useArtificialBounds = true;

    void Start()
    {
        if (!string.IsNullOrEmpty(urdfPath))
        {
            ImportURDF(urdfPath);
        }
    }

    void ImportURDF(string path)
    {
        // Import the URDF file
        GameObject robot = URDFRobotExtensions.CreateRobotFromURDF(
            path,
            optimizeScene,
            useArtificialBounds
        );

        if (robot != null)
        {
            robot.transform.SetParent(transform);
            robot.transform.localPosition = Vector3.zero;
            robot.transform.localRotation = Quaternion.identity;
        }
    }
}
```

### Robot Joint Control

Controlling robot joints in Unity:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using RosMessageTypes.Sensor;

public class JointController : MonoBehaviour
{
    [Header("Joint Configuration")]
    public string[] jointNames;
    public HingeJoint[] joints;
    public float[] jointPositions;

    [Header("ROS Communication")]
    public string jointStateTopic = "/joint_states";

    ROSConnection ros;
    JointStateMsg jointStateMsg;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<JointStateMsg>(jointStateTopic, JointStateCallback);

        InitializeJoints();
    }

    void InitializeJoints()
    {
        jointStateMsg = new JointStateMsg();
        jointStateMsg.name = jointNames;
        jointStateMsg.position = new double[jointNames.Length];
        jointStateMsg.velocity = new double[jointNames.Length];
        jointStateMsg.effort = new double[jointNames.Length];
    }

    void JointStateCallback(JointStateMsg jointState)
    {
        for (int i = 0; i < jointNames.Length && i < jointState.name.Length; i++)
        {
            // Find the joint by name and update its position
            string jointName = jointState.name[i];
            double position = jointState.position[i];

            for (int j = 0; j < joints.Length; j++)
            {
                if (joints[j].name == jointName)
                {
                    // Update joint position
                    JointSpring spring = joints[j].spring;
                    spring.targetPosition = (float)position;
                    joints[j].spring = spring;
                    break;
                }
            }
        }
    }

    void Update()
    {
        // Update joint positions for visualization
        for (int i = 0; i < joints.Length; i++)
        {
            jointStateMsg.position[i] = joints[i].jointAngle;
        }
    }
}
```

## Sensor Simulation in Unity

### Camera Sensor Implementation

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using RosMessageTypes.Sensor;
using System.Collections;

public class UnityCameraSensor : MonoBehaviour
{
    [Header("Camera Settings")]
    public Camera sensorCamera;
    public string imageTopic = "/camera/image_raw";
    public int imageWidth = 640;
    public int imageHeight = 480;
    public int publishFrequency = 30; // Hz

    ROSConnection ros;
    RenderTexture renderTexture;
    Texture2D tempTexture;

    float publishInterval;
    float lastPublishTime;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        // Create render texture for camera
        renderTexture = new RenderTexture(imageWidth, imageHeight, 24);
        sensorCamera.targetTexture = renderTexture;

        // Create temporary texture for reading
        tempTexture = new Texture2D(imageWidth, imageHeight, TextureFormat.RGB24, false);

        publishInterval = 1.0f / publishFrequency;
        lastPublishTime = 0;
    }

    void Update()
    {
        if (Time.time - lastPublishTime >= publishInterval)
        {
            PublishCameraImage();
            lastPublishTime = Time.time;
        }
    }

    void PublishCameraImage()
    {
        // Set the active render texture
        RenderTexture.active = renderTexture;

        // Read pixels from render texture
        tempTexture.ReadPixels(new Rect(0, 0, imageWidth, imageHeight), 0, 0);
        tempTexture.Apply();

        // Convert to ROS image message
        var imageMsg = new ImageMsg();
        imageMsg.header = new std_msgs.HeaderMsg();
        imageMsg.header.stamp = new builtin_interfaces.TimeMsg();
        imageMsg.header.frame_id = "camera_frame";

        imageMsg.height = (uint)imageHeight;
        imageMsg.width = (uint)imageWidth;
        imageMsg.encoding = "rgb8";
        imageMsg.is_bigendian = 0;
        imageMsg.step = (uint)(imageWidth * 3); // 3 bytes per pixel for RGB

        // Convert texture to byte array
        byte[] imageData = tempTexture.GetRawTextureData<byte>();
        imageMsg.data = imageData;

        // Publish the image
        ros.Publish(imageTopic, imageMsg);
    }

    void OnDestroy()
    {
        if (renderTexture != null)
            RenderTexture.ReleaseTemporary(renderTexture);
    }
}
```

### LIDAR Sensor Simulation

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using RosMessageTypes.Sensor;

public class UnityLidarSensor : MonoBehaviour
{
    [Header("LIDAR Settings")]
    public float rangeMin = 0.1f;
    public float rangeMax = 30.0f;
    public int rayCount = 720;
    public float angleMin = -Mathf.PI / 2;
    public float angleMax = Mathf.PI / 2;
    public float updateRate = 10.0f; // Hz

    [Header("Raycast Settings")]
    public LayerMask detectionLayers = -1;
    public string scanTopic = "/scan";

    ROSConnection ros;
    float updateInterval;
    float lastUpdateTime;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        updateInterval = 1.0f / updateRate;
        lastUpdateTime = 0;
    }

    void Update()
    {
        if (Time.time - lastUpdateTime >= updateInterval)
        {
            PublishLidarScan();
            lastUpdateTime = Time.time;
        }
    }

    void PublishLidarScan()
    {
        // Create ray directions
        float angleIncrement = (angleMax - angleMin) / rayCount;

        var ranges = new float[rayCount];

        for (int i = 0; i < rayCount; i++)
        {
            float angle = angleMin + i * angleIncrement;

            // Create ray in local space and transform to world space
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
            direction = transform.TransformDirection(direction);

            // Perform raycast
            RaycastHit hit;
            if (Physics.Raycast(transform.position, direction, out hit, rangeMax, detectionLayers))
            {
                float distance = hit.distance;
                ranges[i] = distance >= rangeMin ? distance : rangeMin;
            }
            else
            {
                ranges[i] = float.PositiveInfinity; // No obstacle detected
            }
        }

        // Create LaserScan message
        var scanMsg = new LaserScanMsg();
        scanMsg.header = new std_msgs.HeaderMsg();
        scanMsg.header.stamp = new builtin_interfaces.TimeMsg();
        scanMsg.header.frame_id = "lidar_frame";

        scanMsg.angle_min = angleMin;
        scanMsg.angle_max = angleMax;
        scanMsg.angle_increment = angleIncrement;
        scanMsg.time_increment = 0;
        scanMsg.scan_time = 1.0f / updateRate;
        scanMsg.range_min = rangeMin;
        scanMsg.range_max = rangeMax;

        scanMsg.ranges = ranges;
        scanMsg.intensities = new float[rayCount]; // Optional intensity data

        // Publish the scan
        ros.Publish(scanTopic, scanMsg);
    }
}
```

## ROS 2 Integration Patterns

### Publisher Component

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class UnityPublisher : MonoBehaviour
{
    [Header("Publisher Settings")]
    public string topicName = "/unity_status";
    public float publishRate = 1.0f; // Hz

    ROSConnection ros;
    float publishInterval;
    float lastPublishTime;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.RegisterPublisher<StringMsg>(topicName);

        publishInterval = 1.0f / publishRate;
        lastPublishTime = 0;
    }

    void Update()
    {
        if (Time.time - lastPublishTime >= publishInterval)
        {
            PublishStatus();
            lastPublishTime = Time.time;
        }
    }

    void PublishStatus()
    {
        var statusMsg = new StringMsg();
        statusMsg.data = $"Unity simulation time: {Time.time:F2}, position: {transform.position}";

        ros.Publish(topicName, statusMsg);
    }
}
```

### Subscriber Component

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class UnitySubscriber : MonoBehaviour
{
    [Header("Subscriber Settings")]
    public string topicName = "/robot_command";

    ROSConnection ros;
    string lastCommand = "idle";

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<StringMsg>(topicName, CommandCallback);
    }

    void CommandCallback(StringMsg commandMsg)
    {
        lastCommand = commandMsg.data;
        ProcessCommand(lastCommand);
    }

    void ProcessCommand(string command)
    {
        switch (command.ToLower())
        {
            case "forward":
                transform.Translate(Vector3.forward * Time.deltaTime);
                break;
            case "backward":
                transform.Translate(Vector3.forward * -Time.deltaTime);
                break;
            case "rotate_left":
                transform.Rotate(Vector3.up, -90 * Time.deltaTime);
                break;
            case "rotate_right":
                transform.Rotate(Vector3.up, 90 * Time.deltaTime);
                break;
            case "stop":
                // Stop movement
                break;
        }
    }

    void OnGUI()
    {
        // Display last received command
        GUI.Label(new Rect(10, 10, 300, 20), $"Last Command: {lastCommand}");
    }
}
```

## Environment Creation

### Creating Complex Environments

Unity's visual editor allows creation of complex environments:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class EnvironmentManager : MonoBehaviour
{
    [Header("Environment Settings")]
    public GameObject[] obstaclePrefabs;
    public Transform environmentBounds;

    [Header("Procedural Generation")]
    public int obstacleCount = 10;
    public float minObstacleSize = 0.5f;
    public float maxObstacleSize = 2.0f;

    List<GameObject> spawnedObstacles = new List<GameObject>();

    void Start()
    {
        GenerateEnvironment();
    }

    void GenerateEnvironment()
    {
        ClearEnvironment();

        for (int i = 0; i < obstacleCount; i++)
        {
            SpawnRandomObstacle();
        }
    }

    void SpawnRandomObstacle()
    {
        if (obstaclePrefabs.Length == 0) return;

        // Select random prefab
        GameObject prefab = obstaclePrefabs[Random.Range(0, obstaclePrefabs.Length)];

        // Random position within bounds
        Vector3 position = new Vector3(
            Random.Range(-environmentBounds.localScale.x / 2, environmentBounds.localScale.x / 2),
            0,
            Random.Range(-environmentBounds.localScale.z / 2, environmentBounds.localScale.z / 2)
        );

        // Random rotation
        Quaternion rotation = Quaternion.Euler(0, Random.Range(0, 360), 0);

        // Random scale
        float scale = Random.Range(minObstacleSize, maxObstacleSize);
        Vector3 scaleVector = Vector3.one * scale;

        GameObject obstacle = Instantiate(prefab, position, rotation);
        obstacle.transform.localScale = scaleVector;

        spawnedObstacles.Add(obstacle);
    }

    void ClearEnvironment()
    {
        foreach (GameObject obstacle in spawnedObstacles)
        {
            if (obstacle != null)
                DestroyImmediate(obstacle);
        }
        spawnedObstacles.Clear();
    }
}
```

## Performance Optimization

### Rendering Optimization

```csharp
using UnityEngine;

public class RenderingOptimizer : MonoBehaviour
{
    [Header("LOD Settings")]
    public float lodDistance = 10.0f;
    public Renderer[] detailedRenderers;
    public Renderer[] simplifiedRenderers;

    [Header("Quality Settings")]
    public bool useOcclusionCulling = true;
    public bool useLOD = true;

    void Start()
    {
        SetupOptimization();
    }

    void SetupOptimization()
    {
        if (useOcclusionCulling)
        {
            // Enable occlusion culling in the camera
            Camera.main.occlusionCulling = true;
        }
    }

    void Update()
    {
        if (useLOD)
        {
            UpdateLOD();
        }
    }

    void UpdateLOD()
    {
        float distance = Vector3.Distance(Camera.main.transform.position, transform.position);

        bool useDetailed = distance < lodDistance;

        foreach (Renderer renderer in detailedRenderers)
        {
            renderer.enabled = useDetailed;
        }

        foreach (Renderer renderer in simplifiedRenderers)
        {
            renderer.enabled = !useDetailed;
        }
    }
}
```

## Best Practices

1. **Performance**: Optimize scenes for real-time performance
2. **Scale**: Maintain proper scale between Unity and ROS coordinates
3. **Coordinate Systems**: Handle coordinate system differences (Unity uses left-handed, ROS uses right-handed)
4. **Network**: Optimize network communication frequency
5. **Synchronization**: Maintain synchronization between Unity and ROS states
6. **Testing**: Validate Unity simulation against real-world data

## Integration with Gazebo

Unity can complement Gazebo by providing:
- Visually rich environments for human-robot interaction
- Advanced rendering for perception system training
- Game-like interfaces for teleoperation
- Prototyping tools for rapid environment creation

## Summary

Unity provides a powerful platform for creating visually rich digital twin environments for robotics. The next chapter will cover robot modeling techniques for both Gazebo and Unity.