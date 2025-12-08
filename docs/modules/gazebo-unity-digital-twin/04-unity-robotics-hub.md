# Chapter 4: Unity Robotics Hub

## Overview

This chapter explores the Unity Robotics Hub, a collection of tools and packages that enable seamless integration between Unity and ROS 2, facilitating the development of robotics applications with high-quality visualization and simulation capabilities.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Install and configure Unity Robotics Hub packages
2. Implement ROS-TCP-Connector for communication
3. Use URDF-Importer to bring robot models into Unity
4. Create custom robotics components using Unity Robotics packages

## Unity Robotics Hub Overview

The Unity Robotics Hub is a collection of packages that facilitate robotics development in Unity:

- **ROS-TCP-Connector**: Enables communication between Unity and ROS 2
- **URDF-Importer**: Imports robot models from URDF files
- **Robotics Examples**: Sample scenes and components for robotics applications
- **Simulation Tools**: Utilities for creating realistic simulation environments

## ROS-TCP-Connector

The ROS-TCP-Connector enables bidirectional communication between Unity and ROS 2 systems.

### Installation and Setup

1. Install the ROS-TCP-Connector package via Unity Package Manager
2. Configure the ROS connection settings
3. Implement publisher and subscriber patterns

### Basic Connection Setup

```csharp
using Unity.Robotics.ROSTCPConnector;

public class RobotConnectionManager : MonoBehaviour
{
    [Header("ROS Connection Settings")]
    public string rosIPAddress = "127.0.0.1";
    public int rosPort = 10000;
    public float connectionTimeout = 10.0f;

    private ROSConnection rosConnection;
    private bool isConnected = false;

    void Start()
    {
        SetupROSConnection();
    }

    void SetupROSConnection()
    {
        // Get or create the ROS connection instance
        rosConnection = ROSConnection.GetOrCreateInstance();

        // Configure connection settings
        rosConnection.Initialize(rosIPAddress, rosPort);

        // Wait for connection
        StartCoroutine(WaitForConnection());
    }

    System.Collections.IEnumerator WaitForConnection()
    {
        float startTime = Time.time;

        while (!rosConnection.IsConnected && (Time.time - startTime) < connectionTimeout)
        {
            yield return new WaitForSeconds(0.1f);
        }

        if (rosConnection.IsConnected)
        {
            isConnected = true;
            Debug.Log("Successfully connected to ROS bridge");
            OnConnected();
        }
        else
        {
            Debug.LogError($"Failed to connect to ROS bridge after {connectionTimeout} seconds");
            OnConnectionFailed();
        }
    }

    void OnConnected()
    {
        // Connection established, register publishers/subscribers
        RegisterROSInterfaces();
    }

    void OnConnectionFailed()
    {
        // Handle connection failure
        Debug.LogWarning("ROS connection failed. Operating in standalone mode.");
    }

    void RegisterROSInterfaces()
    {
        // Register publishers
        rosConnection.RegisterPublisher<geometry_msgs.TwistMsg>("/cmd_vel");
        rosConnection.RegisterPublisher<sensor_msgs.JointStateMsg>("/joint_states");

        // Register subscribers
        rosConnection.Subscribe<sensor_msgs.LaserScanMsg>("/scan", OnLaserScanReceived);
        rosConnection.Subscribe<nav_msgs.OdometryMsg>("/odom", OnOdometryReceived);
    }

    void OnLaserScanReceived(sensor_msgs.LaserScanMsg scan)
    {
        // Process laser scan data
        Debug.Log($"Received laser scan with {scan.ranges.Length} points");
    }

    void OnOdometryReceived(nav_msgs.OdometryMsg odom)
    {
        // Process odometry data
        Debug.Log($"Received odometry: x={odom.pose.pose.position.x}, y={odom.pose.pose.position.y}");
    }
}
```

### Advanced Publisher Implementation

```csharp
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using RosMessageTypes.Geometry;
using RosMessageTypes.Std;
using UnityEngine;

public class AdvancedRobotPublisher : MonoBehaviour
{
    [Header("Publisher Configuration")]
    public string cmdVelTopic = "/cmd_vel";
    public string jointStateTopic = "/joint_states";
    public string tfTopic = "/tf";

    [Header("Robot Configuration")]
    public Transform robotBase;
    public Transform[] jointTransforms;
    public string[] jointNames;

    private ROSConnection ros;
    private float publishRate = 30.0f; // Hz
    private float publishInterval;
    private float lastPublishTime;

    private geometry_msgs.TwistMsg cmdVelMsg;
    private sensor_msgs.JointStateMsg jointStateMsg;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        // Initialize messages
        InitializeMessages();

        // Register publishers
        ros.RegisterPublisher<geometry_msgs.TwistMsg>(cmdVelTopic);
        ros.RegisterPublisher<sensor_msgs.JointStateMsg>(jointStateTopic);
        ros.RegisterPublisher<geometry_msgs.TransformStampedMsg>(tfTopic);

        publishInterval = 1.0f / publishRate;
        lastPublishTime = 0;
    }

    void InitializeMessages()
    {
        cmdVelMsg = new geometry_msgs.TwistMsg();

        jointStateMsg = new sensor_msgs.JointStateMsg();
        jointStateMsg.name = jointNames;
        jointStateMsg.position = new double[jointNames.Length];
        jointStateMsg.velocity = new double[jointNames.Length];
        jointStateMsg.effort = new double[jointNames.Length];
    }

    void Update()
    {
        if (Time.time - lastPublishTime >= publishInterval)
        {
            PublishRobotState();
            lastPublishTime = Time.time;
        }
    }

    void PublishRobotState()
    {
        // Update joint states
        for (int i = 0; i < jointTransforms.Length && i < jointNames.Length; i++)
        {
            // For revolute joints, use localEulerAngles.z
            // For prismatic joints, use position
            jointStateMsg.position[i] = jointTransforms[i].localEulerAngles.z * Mathf.Deg2Rad;
        }

        // Update timestamps
        var currentTime = new builtin_interfaces.TimeMsg();
        currentTime.sec = (int)Time.time;
        currentTime.nanosec = (uint)((Time.time - Mathf.Floor(Time.time)) * 1e9);

        jointStateMsg.header = new std_msgs.HeaderMsg();
        jointStateMsg.header.stamp = currentTime;
        jointStateMsg.header.frame_id = "base_link";

        // Publish joint states
        ros.Publish(jointStateTopic, jointStateMsg);

        // Publish TF transforms
        PublishTransforms();
    }

    void PublishTransforms()
    {
        // Create TF message for robot base
        var tfMsg = new geometry_msgs.TransformStampedMsg();
        tfMsg.header = new std_msgs.HeaderMsg();
        tfMsg.header.stamp = new builtin_interfaces.TimeMsg();
        tfMsg.header.stamp.sec = (int)Time.time;
        tfMsg.header.stamp.nanosec = (uint)((Time.time - Mathf.Floor(Time.time)) * 1e9);
        tfMsg.header.frame_id = "map";
        tfMsg.child_frame_id = "base_link";

        // Convert Unity coordinates to ROS coordinates
        var position = robotBase.position.To<FLU>();
        tfMsg.transform.translation = new geometry_msgs.Vector3Msg(position.x, position.y, position.z);

        var rotation = robotBase.rotation.To<FLU>();
        tfMsg.transform.rotation = new geometry_msgs.QuaternionMsg(rotation.x, rotation.y, rotation.z, rotation.w);

        ros.Publish(tfTopic, tfMsg);
    }

    public void SendVelocityCommand(float linearX, float angularZ)
    {
        cmdVelMsg.linear = new geometry_msgs.Vector3Msg(linearX, 0, 0);
        cmdVelMsg.angular = new geometry_msgs.Vector3Msg(0, 0, angularZ);

        ros.Publish(cmdVelTopic, cmdVelMsg);
    }
}
```

## URDF-Importer

The URDF-Importer package allows direct import of robot models from URDF files into Unity.

### Basic URDF Import

```csharp
using Unity.Robotics.URDFImport;
using UnityEngine;

public class URDFRobotLoader : MonoBehaviour
{
    [Header("URDF Import Settings")]
    public string urdfFilePath;
    public bool optimizeScene = true;
    public bool useArtificialBounds = true;
    public bool createArtificialInertia = true;

    [Header("Import Options")]
    public bool importVisual = true;
    public bool importCollision = true;
    public bool importInertial = true;

    private GameObject importedRobot;

    void Start()
    {
        if (!string.IsNullOrEmpty(urdfFilePath))
        {
            ImportURDFRobot();
        }
    }

    public void ImportURDFRobot()
    {
        // Clear existing robot if any
        if (importedRobot != null)
        {
            DestroyImmediate(importedRobot);
        }

        try
        {
            // Import the robot from URDF
            importedRobot = URDFRobotExtensions.CreateRobotFromURDF(
                urdfFilePath,
                optimizeScene,
                useArtificialBounds,
                createArtificialInertia,
                importVisual,
                importCollision,
                importInertial
            );

            if (importedRobot != null)
            {
                // Position the robot
                importedRobot.transform.SetParent(transform);
                importedRobot.transform.localPosition = Vector3.zero;
                importedRobot.transform.localRotation = Quaternion.identity;

                Debug.Log($"Successfully imported robot from {urdfFilePath}");

                // Configure the imported robot
                ConfigureImportedRobot(importedRobot);
            }
            else
            {
                Debug.LogError($"Failed to import robot from {urdfFilePath}");
            }
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Error importing URDF: {e.Message}");
        }
    }

    void ConfigureImportedRobot(GameObject robot)
    {
        // Add necessary components for Unity-ROS integration
        var robotController = robot.AddComponent<RobotController>();
        var jointController = robot.AddComponent<JointController>();

        // Configure physics properties
        var rigidbodies = robot.GetComponentsInChildren<Rigidbody>();
        foreach (var rb in rigidbodies)
        {
            rb.interpolation = RigidbodyInterpolation.Interpolate;
            rb.collisionDetectionMode = CollisionDetectionMode.Continuous;
        }
    }
}
```

### Advanced URDF Processing

```csharp
using Unity.Robotics.URDFImport;
using Unity.Robotics.URDFImport.Control;
using UnityEngine;

public class AdvancedURDFProcessor : MonoBehaviour
{
    [Header("Joint Control")]
    public float jointVelocity = 1.0f;
    public float jointAcceleration = 2.0f;

    [Header("Sensor Configuration")]
    public bool addDefaultSensors = true;

    private URDFRobot urdfRobot;
    private ArticulationBody[] articulationBodies;
    private JointControl[] jointControls;

    void Start()
    {
        ProcessURDFRobot();
    }

    void ProcessURDFRobot()
    {
        // Get all ArticulationBodies (Unity's equivalent to URDF joints)
        articulationBodies = GetComponentsInChildren<ArticulationBody>();

        // Create joint controls
        CreateJointControls();

        // Configure joint properties
        ConfigureJointProperties();

        if (addDefaultSensors)
        {
            AddDefaultSensors();
        }
    }

    void CreateJointControls()
    {
        jointControls = new JointControl[articulationBodies.Length];

        for (int i = 0; i < articulationBodies.Length; i++)
        {
            var jointControl = new JointControl(articulationBodies[i]);
            jointControls[i] = jointControl;
        }
    }

    void ConfigureJointProperties()
    {
        foreach (var body in articulationBodies)
        {
            // Configure joint drive for position control
            var drive = body.xDrive;
            drive.forceLimit = 10000f;
            drive.damping = 10f;
            drive.stiffness = 100f;
            body.xDrive = drive;

            // Configure joint limits
            if (body.jointType == ArticulationJointType.RevoluteJoint)
            {
                var limits = body.linearLockX;
                // Set appropriate limits based on URDF specifications
            }
        }
    }

    void AddDefaultSensors()
    {
        // Add camera sensors
        var cameraSensors = GetComponentsInChildren<Camera>();
        foreach (var cam in cameraSensors)
        {
            var cameraSensor = cam.gameObject.AddComponent<CameraSensor>();
            cameraSensor.Initialize();
        }

        // Add IMU sensors
        var imuLinks = FindObjectsOfType<ArticulationBody>();
        foreach (var link in imuLinks)
        {
            if (link.name.ToLower().Contains("imu") || link.name.ToLower().Contains("sensor"))
            {
                var imuSensor = link.gameObject.AddComponent<IMUSensor>();
                imuSensor.Initialize();
            }
        }
    }
}

[System.Serializable]
public class JointControl
{
    public ArticulationBody articulationBody;
    public string jointName;
    public JointControlType controlType = JointControlType.Position;
    public float targetPosition;
    public float targetVelocity;
    public float targetEffort;

    public JointControl(ArticulationBody body)
    {
        articulationBody = body;
        jointName = body.name;
    }

    public void SetTargetPosition(float position)
    {
        targetPosition = position;
        var drive = articulationBody.xDrive;
        drive.target = targetPosition;
        articulationBody.xDrive = drive;
    }

    public void SetTargetVelocity(float velocity)
    {
        targetVelocity = velocity;
        var drive = articulationBody.xDrive;
        drive.targetVelocity = targetVelocity;
        articulationBody.xDrive = drive;
    }
}

public enum JointControlType
{
    Position,
    Velocity,
    Effort,
    Impedance
}
```

## Sensor Simulation Integration

### Camera Sensor with ROS Integration

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;
using RosMessageTypes.Std;
using UnityEngine;

public class ROSSensorCamera : MonoBehaviour
{
    [Header("Camera Configuration")]
    public Camera sensorCamera;
    public int imageWidth = 640;
    public int imageHeight = 480;
    public int cameraFps = 30;
    public string imageTopic = "/camera/image_raw";
    public string cameraInfoTopic = "/camera/camera_info";

    [Header("Camera Parameters")]
    public float fov = 60f;
    public float nearClip = 0.1f;
    public float farClip = 100f;

    private ROSConnection ros;
    private RenderTexture renderTexture;
    private Texture2D readTexture;
    private float publishInterval;
    private float lastPublishTime;

    // Camera info message
    private sensor_msgs.CameraInfoMsg cameraInfoMsg;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        // Setup camera
        if (sensorCamera == null)
            sensorCamera = GetComponent<Camera>();

        SetupRenderTexture();
        SetupCameraInfo();

        publishInterval = 1.0f / cameraFps;
        lastPublishTime = 0;

        // Register publishers
        ros.RegisterPublisher<sensor_msgs.ImageMsg>(imageTopic);
        ros.RegisterPublisher<sensor_msgs.CameraInfoMsg>(cameraInfoTopic);
    }

    void SetupRenderTexture()
    {
        renderTexture = new RenderTexture(imageWidth, imageHeight, 24, RenderTextureFormat.ARGB32);
        sensorCamera.targetTexture = renderTexture;
        readTexture = new Texture2D(imageWidth, imageHeight, TextureFormat.RGB24, false);
    }

    void SetupCameraInfo()
    {
        cameraInfoMsg = new sensor_msgs.CameraInfoMsg();
        cameraInfoMsg.header = new std_msgs.HeaderMsg();
        cameraInfoMsg.width = (uint)imageWidth;
        cameraInfoMsg.height = (uint)imageHeight;
        cameraInfoMsg.distortion_model = "plumb_bob";

        // Calculate camera matrix based on FOV
        float fx = (imageWidth / 2.0f) / Mathf.Tan(Mathf.Deg2Rad * fov / 2.0f);
        float fy = (imageHeight / 2.0f) / Mathf.Tan(Mathf.Deg2Rad * fov / 2.0f);

        cameraInfoMsg.K = new double[] { fx, 0, imageWidth / 2.0, 0, fy, imageHeight / 2.0, 0, 0, 1 };
        cameraInfoMsg.P = new double[] { fx, 0, imageWidth / 2.0, 0, 0, fy, imageHeight / 2.0, 0, 0, 0, 1, 0 };
    }

    void Update()
    {
        if (Time.time - lastPublishTime >= publishInterval)
        {
            PublishCameraData();
            lastPublishTime = Time.time;
        }
    }

    void PublishCameraData()
    {
        // Capture image from render texture
        RenderTexture.active = renderTexture;
        readTexture.ReadPixels(new Rect(0, 0, imageWidth, imageHeight), 0, 0);
        readTexture.Apply();

        // Create and publish image message
        var imageMsg = new sensor_msgs.ImageMsg();
        imageMsg.header = new std_msgs.HeaderMsg();
        imageMsg.header.stamp = new builtin_interfaces.TimeMsg();
        imageMsg.header.stamp.sec = (int)Time.time;
        imageMsg.header.stamp.nanosec = (uint)((Time.time - Mathf.Floor(Time.time)) * 1e9);
        imageMsg.header.frame_id = transform.name + "_optical_frame";

        imageMsg.height = (uint)imageHeight;
        imageMsg.width = (uint)imageWidth;
        imageMsg.encoding = "rgb8";
        imageMsg.is_bigendian = 0;
        imageMsg.step = (uint)(imageWidth * 3); // 3 bytes per pixel

        // Convert texture to byte array
        imageMsg.data = readTexture.GetRawTextureData<byte>();

        ros.Publish(imageTopic, imageMsg);

        // Update and publish camera info
        cameraInfoMsg.header.stamp = imageMsg.header.stamp;
        ros.Publish(cameraInfoTopic, cameraInfoMsg);
    }

    void OnDestroy()
    {
        if (renderTexture != null)
            RenderTexture.ReleaseTemporary(renderTexture);
    }
}
```

## Custom Robotics Components

### Robot State Publisher

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Nav;
using RosMessageTypes.Std;
using UnityEngine;

public class RobotStatePublisher : MonoBehaviour
{
    [Header("Topics")]
    public string jointStatesTopic = "/joint_states";
    public string tfTopic = "/tf";

    [Header("Robot Configuration")]
    public Transform robotRoot;
    public Transform[] jointTransforms;
    public string[] jointNames;
    public Transform[] linkTransforms;
    public string[] linkNames;

    private ROSConnection ros;
    private sensor_msgs.JointStateMsg jointStateMsg;
    private float publishRate = 50.0f;
    private float publishInterval;
    private float lastPublishTime;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();

        InitializeMessages();
        ros.RegisterPublisher<sensor_msgs.JointStateMsg>(jointStatesTopic);
        ros.RegisterPublisher<geometry_msgs.TransformStampedMsg>(tfTopic);

        publishInterval = 1.0f / publishRate;
        lastPublishTime = 0;
    }

    void InitializeMessages()
    {
        jointStateMsg = new sensor_msgs.JointStateMsg();
        jointStateMsg.name = jointNames;
        jointStateMsg.position = new double[jointNames.Length];
        jointStateMsg.velocity = new double[jointNames.Length];
        jointStateMsg.effort = new double[jointNames.Length];
    }

    void Update()
    {
        if (Time.time - lastPublishTime >= publishInterval)
        {
            PublishRobotState();
            lastPublishTime = Time.time;
        }
    }

    void PublishRobotState()
    {
        // Update joint states
        for (int i = 0; i < jointTransforms.Length && i < jointNames.Length; i++)
        {
            jointStateMsg.position[i] = jointTransforms[i].localEulerAngles.z * Mathf.Deg2Rad;
        }

        // Update timestamp
        var currentTime = new builtin_interfaces.TimeMsg();
        currentTime.sec = (int)Time.time;
        currentTime.nanosec = (uint)((Time.time - Mathf.Floor(Time.time)) * 1e9);

        jointStateMsg.header = new std_msgs.HeaderMsg();
        jointStateMsg.header.stamp = currentTime;
        jointStateMsg.header.frame_id = "base_link";

        ros.Publish(jointStatesTopic, jointStateMsg);

        // Publish transforms for all links
        PublishTransforms();
    }

    void PublishTransforms()
    {
        var currentTime = new builtin_interfaces.TimeMsg();
        currentTime.sec = (int)Time.time;
        currentTime.nanosec = (uint)((Time.time - Mathf.Floor(Time.time)) * 1e9);

        for (int i = 0; i < linkTransforms.Length && i < linkNames.Length; i++)
        {
            var tfMsg = new geometry_msgs.TransformStampedMsg();
            tfMsg.header = new std_msgs.HeaderMsg();
            tfMsg.header.stamp = currentTime;
            tfMsg.header.frame_id = "base_link";
            tfMsg.child_frame_id = linkNames[i];

            var position = linkTransforms[i].position.To<FLU>();
            tfMsg.transform.translation = new geometry_msgs.Vector3Msg(position.x, position.y, position.z);

            var rotation = linkTransforms[i].rotation.To<FLU>();
            tfMsg.transform.rotation = new geometry_msgs.QuaternionMsg(rotation.x, rotation.y, rotation.z, rotation.w);

            ros.Publish(tfTopic, tfMsg);
        }
    }
}
```

## Best Practices for Unity Robotics Hub

### Performance Optimization

1. **Network Efficiency**: Batch messages when possible to reduce network overhead
2. **Update Rates**: Use appropriate update rates for different types of data
3. **Message Size**: Optimize message contents to reduce bandwidth usage
4. **Threading**: Use async operations for network communication

### Error Handling

```csharp
public class RobustROSConnection : MonoBehaviour
{
    private ROSConnection ros;
    private bool connectionActive = false;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.OnConnected += OnROSConnected;
        ros.OnDisconnected += OnROSDisconnected;
        ros.OnConnectionFailed += OnROSConnectionFailed;
    }

    void OnROSConnected()
    {
        connectionActive = true;
        Debug.Log("ROS connection established");
        InitializeROSInterfaces();
    }

    void OnROSDisconnected()
    {
        connectionActive = false;
        Debug.LogWarning("ROS connection lost");
        HandleDisconnection();
    }

    void OnROSConnectionFailed(string errorMessage)
    {
        connectionActive = false;
        Debug.LogError($"ROS connection failed: {errorMessage}");
        AttemptReconnection();
    }

    void InitializeROSInterfaces()
    {
        try
        {
            ros.RegisterPublisher<geometry_msgs.TwistMsg>("/cmd_vel");
            ros.Subscribe<sensor_msgs.LaserScanMsg>("/scan", OnLaserScanReceived);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to initialize ROS interfaces: {e.Message}");
        }
    }

    void HandleDisconnection()
    {
        // Switch to safe mode or emergency procedures
        StopRobotMotion();
    }

    async void AttemptReconnection()
    {
        // Wait before attempting reconnection
        await System.Threading.Tasks.Task.Delay(5000);

        if (!connectionActive)
        {
            ros.Initialize();
        }
    }

    void StopRobotMotion()
    {
        if (connectionActive)
        {
            var stopCmd = new geometry_msgs.TwistMsg();
            ros.Publish("/cmd_vel", stopCmd);
        }
    }

    void OnLaserScanReceived(sensor_msgs.LaserScanMsg scan)
    {
        // Validate message before processing
        if (scan.ranges != null && scan.ranges.Length > 0)
        {
            // Process valid scan data
        }
    }
}
```

## Troubleshooting Common Issues

### Connection Issues

- **Port Conflicts**: Ensure ROS bridge is running on the correct port
- **Network Configuration**: Check firewall settings and network connectivity
- **Message Type Mismatches**: Verify message types match between Unity and ROS

### Performance Issues

- **High Latency**: Reduce message frequency or optimize message size
- **Frame Drops**: Optimize Unity scene complexity and rendering settings
- **Memory Usage**: Monitor and optimize object instantiation and destruction

## Summary

The Unity Robotics Hub provides powerful tools for integrating Unity with ROS 2, enabling the creation of visually rich simulation environments for robotics applications. Proper configuration and implementation of these tools is essential for successful robotics development in Unity.