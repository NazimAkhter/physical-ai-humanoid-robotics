# Project Development

## Overview

This chapter covers the development process for integrating all four modules into a complete Physical AI & Humanoid Robotics platform. We'll implement the core integration components and connect them to form a unified system.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Implement the main integration framework connecting all modules
2. Develop communication bridges between different systems
3. Create unified control interfaces
4. Build end-to-end applications combining all technologies

## Integration Architecture

### Main Integration Framework

```python
# main_integration_framework.py
import asyncio
import threading
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class SystemState(Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    ERROR = "error"
    SHUTDOWN = "shutdown"

@dataclass
class IntegrationContext:
    """Context for the integrated system"""
    state: SystemState
    timestamp: float
    components: Dict[str, Any]
    active_processes: Dict[str, Any]
    system_metrics: Dict[str, float]

class PhysicalAIRoboticsPlatform:
    """Main integration class for the Physical AI & Humanoid Robotics platform"""

    def __init__(self):
        self.context = IntegrationContext(
            state=SystemState.IDLE,
            timestamp=time.time(),
            components={},
            active_processes={},
            system_metrics={}
        )

        self.ros_bridge = None
        self.isaac_sim_interface = None
        self.vla_pipeline = None
        self.digital_twin = None

        # Threading and async setup
        self.main_loop = None
        self.system_lock = threading.Lock()

    async def initialize(self):
        """Initialize all system components"""
        self.context.state = SystemState.INITIALIZING
        self.context.timestamp = time.time()

        print("Initializing Physical AI & Humanoid Robotics Platform...")

        # Initialize ROS 2 bridge
        self.ros_bridge = await self._initialize_ros_bridge()

        # Initialize Isaac Sim interface
        self.isaac_sim_interface = await self._initialize_isaac_interface()

        # Initialize VLA pipeline
        self.vla_pipeline = await self._initialize_vla_pipeline()

        # Initialize digital twin
        self.digital_twin = await self._initialize_digital_twin()

        # Register components
        self.context.components = {
            'ros_bridge': self.ros_bridge,
            'isaac_interface': self.isaac_sim_interface,
            'vla_pipeline': self.vla_pipeline,
            'digital_twin': self.digital_twin
        }

        print("All components initialized successfully!")
        self.context.state = SystemState.RUNNING

    async def _initialize_ros_bridge(self):
        """Initialize ROS 2 bridge for robot communication"""
        import rclpy
        from rclpy.node import Node

        # Initialize ROS context
        rclpy.init()

        # Create ROS bridge node
        class ROSBridgeNode(Node):
            def __init__(self):
                super().__init__('physical_ai_bridge')

                # Publishers
                self.cmd_vel_pub = self.create_publisher(
                    'geometry_msgs.msg.Twist',
                    '/cmd_vel',
                    10
                )

                # Subscribers
                self.laser_sub = self.create_subscription(
                    'sensor_msgs.msg.LaserScan',
                    '/scan',
                    self.laser_callback,
                    10
                )

                self.camera_sub = self.create_subscription(
                    'sensor_msgs.msg.Image',
                    '/camera/image_raw',
                    self.camera_callback,
                    10
                )

                # Services
                self.navigation_service = self.create_service(
                    'nav_msgs.srv.GetPlan',
                    'get_navigation_plan',
                    self.handle_navigation_request
                )

                self.context.active_processes['ros_bridge'] = self

            def laser_callback(self, msg):
                # Process laser data
                pass

            def camera_callback(self, msg):
                # Process camera data
                pass

            def handle_navigation_request(self, request, response):
                # Handle navigation requests
                return response

        return ROSBridgeNode()

    async def _initialize_isaac_interface(self):
        """Initialize Isaac Sim interface for AI training and simulation"""
        try:
            from omni.isaac.core import World
            from omni.isaac.core.utils.stage import add_reference_to_stage

            # Initialize Isaac Sim world
            world = World(stage_units_in_meters=1.0)
            world.scene.add_default_ground_plane()

            # Setup robot in simulation
            # This would include robot models, sensors, etc.

            self.context.active_processes['isaac_interface'] = world
            return world

        except ImportError:
            print("Isaac Sim not available, running in simulation-only mode")
            return None

    async def _initialize_vla_pipeline(self):
        """Initialize Vision-Language-Action pipeline"""
        from vla_api.voice import process_voice_command
        from vla_api.planning import generate_action_sequence
        from vla_api.perception import detect_objects, ground_language_to_perception

        class VLAPipeline:
            def __init__(self):
                self.voice_processor = process_voice_command
                self.planning_system = generate_action_sequence
                self.perception_system = {
                    'detect_objects': detect_objects,
                    'ground_language_to_perception': ground_language_to_perception
                }

            async def execute_vla_command(self, voice_command, scene_image):
                """Execute complete VLA pipeline"""
                # Process voice to text and intent
                voice_result = await self.voice_processor(voice_command)

                # Detect objects in scene
                perception_result = await self.perception_system['detect_objects'](scene_image)

                # Generate action plan
                planning_result = await self.planning_system(
                    voice_result['transcription'],
                    {
                        'detected_objects': perception_result['detected_objects'],
                        'robot_state': 'idle'
                    }
                )

                return {
                    'voice_processing': voice_result,
                    'perception': perception_result,
                    'planning': planning_result,
                    'status': 'completed'
                }

        pipeline = VLAPipeline()
        self.context.active_processes['vla_pipeline'] = pipeline
        return pipeline

    async def _initialize_digital_twin(self):
        """Initialize digital twin interface"""
        class DigitalTwinInterface:
            def __init__(self):
                self.simulation_engines = {
                    'gazebo': None,
                    'unity': None,
                    'isaac': None
                }

            def sync_with_real_robot(self, real_data):
                """Synchronize digital twin with real robot data"""
                # Update simulation based on real sensor data
                pass

            def predict_robot_state(self, commands):
                """Predict robot state based on commands"""
                # Run simulation to predict outcomes
                pass

        twin = DigitalTwinInterface()
        self.context.active_processes['digital_twin'] = twin
        return twin

    async def start_main_loop(self):
        """Start the main integration loop"""
        if self.context.state != SystemState.RUNNING:
            raise Exception("System not initialized")

        print("Starting main integration loop...")

        while self.context.state == SystemState.RUNNING:
            try:
                await self._integration_step()
                await asyncio.sleep(0.1)  # 10Hz update rate
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.context.state = SystemState.ERROR
                break

    async def _integration_step(self):
        """Single step of the integration loop"""
        # Update system metrics
        self._update_metrics()

        # Process incoming commands
        await self._process_commands()

        # Synchronize digital twin with real robot
        await self._sync_digital_twin()

        # Update AI models with new data
        await self._update_ai_models()

    def _update_metrics(self):
        """Update system performance metrics"""
        import psutil
        import GPUtil

        # CPU usage
        self.context.system_metrics['cpu_percent'] = psutil.cpu_percent()

        # Memory usage
        memory = psutil.virtual_memory()
        self.context.system_metrics['memory_percent'] = memory.percent
        self.context.system_metrics['memory_available_gb'] = memory.available / (1024**3)

        # GPU usage (if available)
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Primary GPU
            self.context.system_metrics['gpu_percent'] = gpu.load * 100
            self.context.system_metrics['gpu_memory_percent'] = gpu.memoryUtil * 100

    async def _process_commands(self):
        """Process incoming commands from various sources"""
        # This would handle commands from:
        # - VLA pipeline (voice commands)
        # - Web interface
        # - Mobile app
        # - Direct ROS messages
        pass

    async def _sync_digital_twin(self):
        """Synchronize digital twin with real robot state"""
        if self.digital_twin and self.ros_bridge:
            # Get real robot data from ROS
            # Update simulation to match
            pass

    async def _update_ai_models(self):
        """Update AI models with new experience"""
        # This would handle:
        # - Online learning updates
        # - Model retraining
        # - Performance monitoring
        pass

    async def shutdown(self):
        """Gracefully shutdown the system"""
        print("Shutting down Physical AI & Humanoid Robotics Platform...")

        self.context.state = SystemState.SHUTDOWN

        # Stop main loop
        if self.main_loop:
            self.main_loop.cancel()

        # Shutdown ROS bridge
        if self.ros_bridge:
            self.ros_bridge.destroy_node()

        # Shutdown Isaac Sim
        if self.isaac_sim_interface:
            self.isaac_sim_interface.stop()

        # Cleanup other components
        for process_name, process in self.context.active_processes.items():
            if hasattr(process, 'shutdown'):
                process.shutdown()

        print("System shutdown complete")

    def get_system_status(self):
        """Get current system status"""
        return {
            'state': self.context.state.value,
            'timestamp': self.context.timestamp,
            'components': list(self.context.components.keys()),
            'system_metrics': self.context.system_metrics,
            'uptime': time.time() - self.context.timestamp
        }
```

## Communication Bridges

### ROS Bridge Implementation

```python
# ros_bridge.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import asyncio
import websockets
import json

class ROSBridge(Node):
    """Bridge between ROS 2 and other system components"""

    def __init__(self):
        super().__init__('physical_ai_ros_bridge')

        # ROS publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/system_status', 10)

        self.laser_sub = self.create_subscription(LaserScan, '/scan', self.laser_callback, 10)
        self.camera_sub = self.create_subscription(Image, '/camera/image_raw', self.camera_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # WebSocket server for external communication
        self.websocket_server = None
        self.connected_clients = set()

        # Data buffers
        self.sensor_data = {
            'laser': None,
            'camera': None,
            'odometry': None
        }

        # Start WebSocket server
        self.start_websocket_server()

    def laser_callback(self, msg):
        """Handle laser scan data"""
        self.sensor_data['laser'] = {
            'ranges': list(msg.ranges),
            'intensities': list(msg.intensities),
            'angle_min': msg.angle_min,
            'angle_max': msg.angle_max,
            'angle_increment': msg.angle_increment,
            'time_increment': msg.time_increment,
            'scan_time': msg.scan_time,
            'range_min': msg.range_min,
            'range_max': msg.range_max
        }

        # Broadcast to connected clients
        self.broadcast_to_clients({
            'type': 'sensor_data',
            'sensor': 'laser',
            'data': self.sensor_data['laser']
        })

    def camera_callback(self, msg):
        """Handle camera image data"""
        # Convert ROS image to format suitable for AI processing
        self.sensor_data['camera'] = {
            'height': msg.height,
            'width': msg.width,
            'encoding': msg.encoding,
            'is_bigendian': msg.is_bigendian,
            'step': msg.step,
            # Note: Raw data would be processed separately
        }

        # Broadcast to connected clients
        self.broadcast_to_clients({
            'type': 'sensor_data',
            'sensor': 'camera',
            'data': {
                'height': msg.height,
                'width': msg.width,
                'encoding': msg.encoding
            }
        })

    def odom_callback(self, msg):
        """Handle odometry data"""
        self.sensor_data['odometry'] = {
            'pose': {
                'position': {
                    'x': msg.pose.pose.position.x,
                    'y': msg.pose.pose.position.y,
                    'z': msg.pose.pose.position.z
                },
                'orientation': {
                    'x': msg.pose.pose.orientation.x,
                    'y': msg.pose.pose.orientation.y,
                    'z': msg.pose.pose.orientation.z,
                    'w': msg.pose.pose.orientation.w
                }
            },
            'twist': {
                'linear': {
                    'x': msg.twist.twist.linear.x,
                    'y': msg.twist.twist.linear.y,
                    'z': msg.twist.twist.linear.z
                },
                'angular': {
                    'x': msg.twist.twist.angular.x,
                    'y': msg.twist.twist.angular.y,
                    'z': msg.twist.twist.angular.z
                }
            }
        }

        # Broadcast to connected clients
        self.broadcast_to_clients({
            'type': 'sensor_data',
            'sensor': 'odometry',
            'data': self.sensor_data['odometry']
        })

    def start_websocket_server(self):
        """Start WebSocket server for external communication"""
        import threading

        async def register_client(websocket, path):
            self.connected_clients.add(websocket)
            try:
                async for message in websocket:
                    await self.handle_websocket_message(message)
            finally:
                self.connected_clients.remove(websocket)

        def run_websocket_server():
            start_server = websockets.serve(register_client, "localhost", 8765)
            asyncio.run(start_server)

        # Run WebSocket server in separate thread
        ws_thread = threading.Thread(target=run_websocket_server, daemon=True)
        ws_thread.start()

    async def handle_websocket_message(self, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)

            if data['type'] == 'robot_command':
                await self.execute_robot_command(data['command'])
            elif data['type'] == 'request_data':
                await self.send_sensor_data(data['sensor_type'])
        except json.JSONDecodeError:
            self.get_logger().error(f"Invalid JSON message: {message}")

    def broadcast_to_clients(self, message):
        """Broadcast message to all connected WebSocket clients"""
        if not self.connected_clients:
            return

        async def send_to_client(client):
            try:
                await client.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                pass  # Client disconnected

        # Send to all clients concurrently
        for client in self.connected_clients.copy():
            asyncio.create_task(send_to_client(client))

    async def execute_robot_command(self, command):
        """Execute robot command received via WebSocket"""
        if command['action'] == 'move':
            twist_msg = Twist()
            twist_msg.linear.x = command['linear_velocity']
            twist_msg.angular.z = command['angular_velocity']
            self.cmd_vel_pub.publish(twist_msg)
        elif command['action'] == 'stop':
            stop_msg = Twist()
            self.cmd_vel_pub.publish(stop_msg)

    async def send_sensor_data(self, sensor_type):
        """Send sensor data to requesting client"""
        if sensor_type in self.sensor_data and self.sensor_data[sensor_type]:
            response = {
                'type': 'sensor_response',
                'sensor': sensor_type,
                'data': self.sensor_data[sensor_type]
            }
            # This would be sent back to the requesting client
```

## Unified Control Interface

### Web Interface Implementation

```python
# web_interface.py
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any, List
import asyncio
import json

app = FastAPI(title="Physical AI & Humanoid Robotics Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

class RobotCommand(BaseModel):
    """Model for robot commands"""
    linear_velocity: float = 0.0
    angular_velocity: float = 0.0
    action: str = "move"

class VoiceCommand(BaseModel):
    """Model for voice commands"""
    audio_data: str  # Base64 encoded audio
    sample_rate: int = 16000

@app.get("/")
async def root():
    """Main dashboard"""
    return {"message": "Physical AI & Humanoid Robotics Platform API"}

@app.post("/api/robot/command")
async def send_robot_command(command: RobotCommand):
    """Send command to robot"""
    # This would interface with the ROS bridge
    print(f"Sending command: {command}")

    # In real implementation, this would send to ROS bridge
    # await ros_bridge.execute_command(command)

    return {"status": "command_sent", "command": command.dict()}

@app.post("/api/vla/process")
async def process_voice_command(voice_cmd: VoiceCommand):
    """Process voice command through VLA pipeline"""
    # This would interface with the VLA pipeline
    print(f"Processing voice command with {len(voice_cmd.audio_data)} bytes of audio")

    # In real implementation, this would process through VLA pipeline
    # result = await vla_pipeline.execute_voice_command(voice_cmd.audio_data)

    return {
        "status": "processing",
        "message": "Voice command received and being processed"
    }

@app.get("/api/system/status")
async def get_system_status():
    """Get overall system status"""
    # This would interface with the main platform
    # status = await main_platform.get_system_status()

    return {
        "system_status": "running",
        "components": {
            "ros_bridge": "connected",
            "isaac_sim": "running",
            "vla_pipeline": "ready",
            "digital_twin": "synced"
        },
        "metrics": {
            "cpu_usage": 45.2,
            "memory_usage": 62.1,
            "gpu_usage": 23.5
        }
    }

@app.get("/api/sensors/data")
async def get_sensor_data():
    """Get current sensor data"""
    # This would interface with ROS bridge
    return {
        "laser_scan": {
            "ranges": [1.0, 1.1, 1.2, 1.3, 1.4],
            "min_range": 0.1,
            "max_range": 30.0
        },
        "camera": {
            "resolution": [640, 480],
            "encoding": "rgb8"
        },
        "odometry": {
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
        }
    }

@app.websocket("/ws/robot")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time robot control"""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "robot_command":
                command = RobotCommand(**message["data"])
                # Execute command
                result = await send_robot_command(command)
                await websocket.send_text(json.dumps(result))

            elif message["type"] == "request_status":
                status = await get_system_status()
                await websocket.send_text(json.dumps(status))

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Additional API endpoints for specific functionality
@app.get("/api/navigation/plan")
async def get_navigation_plan(start: str, goal: str):
    """Get navigation plan between start and goal positions"""
    # This would interface with navigation stack
    return {
        "plan": [
            {"x": 0.0, "y": 0.0, "theta": 0.0},
            {"x": 1.0, "y": 0.0, "theta": 0.0},
            {"x": 1.0, "y": 1.0, "theta": 1.57}
        ],
        "status": "success"
    }

@app.post("/api/manipulation/grasp")
async def plan_grasp_object(object_id: str):
    """Plan grasp for specified object"""
    # This would interface with manipulation stack
    return {
        "grasp_poses": [
            {"position": {"x": 0.5, "y": 0.3, "z": 0.2}, "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}}
        ],
        "approach_poses": [
            {"position": {"x": 0.5, "y": 0.3, "z": 0.3}, "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}}
        ],
        "status": "success"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## End-to-End Application Examples

### Navigation with VLA Integration

```python
# end_to_end_examples.py
import asyncio
from typing import Dict, Any

class EndToEndApplications:
    """Implementation of end-to-end applications combining all modules"""

    def __init__(self, platform):
        self.platform = platform

    async def voice_navigation_task(self, voice_command: str):
        """Complete task: navigate to location based on voice command"""

        print(f"Processing voice navigation command: {voice_command}")

        # Step 1: Voice processing through VLA pipeline
        voice_result = await self.platform.vla_pipeline.voice_processor(voice_command)
        print(f"Voice processing result: {voice_result}")

        # Step 2: Extract destination from processed voice
        destination = self._extract_destination(voice_result['transcription'])

        # Step 3: Get current robot position from ROS
        current_pos = await self._get_robot_position()

        # Step 4: Plan navigation path using ROS navigation stack
        nav_plan = await self._plan_navigation(current_pos, destination)

        # Step 5: Execute navigation with Isaac Sim monitoring
        execution_result = await self._execute_navigation(nav_plan)

        # Step 6: Update digital twin
        await self._update_digital_twin(execution_result)

        return {
            "status": "completed",
            "voice_processing": voice_result,
            "navigation_plan": nav_plan,
            "execution_result": execution_result,
            "destination": destination
        }

    async def object_interaction_task(self, voice_command: str, scene_image: Any):
        """Complete task: interact with object based on voice command"""

        print(f"Processing object interaction command: {voice_command}")

        # Step 1: Voice processing
        voice_result = await self.platform.vla_pipeline.voice_processor(voice_command)

        # Step 2: Object detection in scene
        detection_result = await self.platform.vla_pipeline.perception_system['detect_objects'](scene_image)

        # Step 3: Ground language to visual entities
        grounding_result = await self.platform.vla_pipeline.perception_system['ground_language_to_perception'](
            voice_result['transcription'],
            scene_image
        )

        # Step 4: Generate manipulation plan
        manipulation_plan = await self.platform.vla_pipeline.planning_system(
            voice_result['transcription'],
            {
                'detected_objects': detection_result['detected_objects'],
                'grounding_result': grounding_result,
                'robot_state': 'idle'
            }
        )

        # Step 5: Execute manipulation with safety checks
        execution_result = await self._execute_manipulation(manipulation_plan)

        # Step 6: Update digital twin and log results
        await self._update_digital_twin(execution_result)
        await self._log_interaction(voice_command, execution_result)

        return {
            "status": "completed",
            "voice_processing": voice_result,
            "perception": detection_result,
            "grounding": grounding_result,
            "manipulation_plan": manipulation_plan,
            "execution_result": execution_result
        }

    def _extract_destination(self, transcription: str) -> Dict[str, float]:
        """Extract destination coordinates from voice transcription"""
        # This would use NLP to extract location information
        # For example: "Go to the kitchen" -> kitchen coordinates
        destinations = {
            "kitchen": {"x": 5.0, "y": 3.0},
            "living room": {"x": 2.0, "y": 1.0},
            "bedroom": {"x": 8.0, "y": 2.0},
            "office": {"x": 1.0, "y": 5.0}
        }

        transcription_lower = transcription.lower()
        for location, coords in destinations.items():
            if location in transcription_lower:
                return coords

        # Default: return current position + offset
        return {"x": 1.0, "y": 1.0}

    async def _get_robot_position(self) -> Dict[str, float]:
        """Get current robot position from ROS odometry"""
        # This would interface with ROS odometry topic
        return {"x": 0.0, "y": 0.0, "theta": 0.0}

    async def _plan_navigation(self, start: Dict[str, float], goal: Dict[str, float]) -> List[Dict[str, float]]:
        """Plan navigation path using ROS navigation stack"""
        # This would call ROS navigation service
        # For example, using nav_msgs/GetPlan service
        return [
            {"x": start["x"], "y": start["y"], "theta": start["theta"]},
            {"x": goal["x"], "y": goal["y"], "theta": goal["theta"]}
        ]

    async def _execute_navigation(self, nav_plan: List[Dict[str, float]]) -> Dict[str, Any]:
        """Execute navigation plan"""
        # This would send commands to robot through ROS
        # Monitor progress and handle obstacles
        result = {
            "status": "success",
            "completed_waypoints": len(nav_plan),
            "execution_time": 30.0,  # seconds
            "distance_traveled": 5.0  # meters
        }
        return result

    async def _execute_manipulation(self, manipulation_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute manipulation plan"""
        # This would interface with robot manipulator
        # Execute each action in the plan
        result = {
            "status": "success",
            "completed_actions": len(manipulation_plan.get("action_sequence", [])),
            "execution_time": 45.0,  # seconds
            "success_rate": 0.95
        }
        return result

    async def _update_digital_twin(self, execution_result: Dict[str, Any]):
        """Update digital twin with execution results"""
        # This would update Isaac Sim or other simulation
        # with real robot state and results
        pass

    async def _log_interaction(self, voice_command: str, execution_result: Dict[str, Any]):
        """Log the interaction for learning and analysis"""
        # This would log to database for future learning
        log_entry = {
            "timestamp": asyncio.get_event_loop().time(),
            "voice_command": voice_command,
            "result": execution_result,
            "success": execution_result.get("status") == "success"
        }
        # In real implementation, this would save to database
        pass

# Example usage
async def run_end_to_end_examples():
    """Run example end-to-end applications"""
    # This would be called from the main platform
    pass
```

## Testing and Validation

### Integration Tests

```python
# integration_tests.py
import unittest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

class TestIntegrationFramework(unittest.TestCase):
    """Integration tests for the Physical AI platform"""

    def setUp(self):
        """Set up test environment"""
        self.platform = Mock()  # This would be the real platform in actual tests
        self.apps = EndToEndApplications(self.platform)

    @patch('end_to_end_examples.EndToEndApplications._get_robot_position')
    @patch('end_to_end_examples.EndToEndApplications._plan_navigation')
    @patch('end_to_end_examples.EndToEndApplications._execute_navigation')
    @patch('end_to_end_examples.EndToEndApplications._update_digital_twin')
    def test_voice_navigation_task(self, mock_update_twin, mock_execute, mock_plan, mock_get_pos):
        """Test voice navigation task"""
        # Set up mocks
        mock_get_pos.return_value = {"x": 0.0, "y": 0.0}
        mock_plan.return_value = [{"x": 1.0, "y": 1.0}]
        mock_execute.return_value = {"status": "success"}

        # Test the function
        result = asyncio.run(self.apps.voice_navigation_task("Go to the kitchen"))

        # Verify results
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["destination"], {"x": 5.0, "y": 3.0})  # Kitchen coordinates

    @patch('end_to_end_examples.EndToEndApplications._execute_manipulation')
    @patch('end_to_end_examples.EndToEndApplications._update_digital_twin')
    @patch('end_to_end_examples.EndToEndApplications._log_interaction')
    def test_object_interaction_task(self, mock_log, mock_update_twin, mock_execute):
        """Test object interaction task"""
        # Mock the VLA pipeline components
        with patch.object(self.apps.platform, 'vla_pipeline') as mock_vla:
            mock_vla.voice_processor = AsyncMock(return_value={
                'transcription': 'Pick up the red cube'
            })
            mock_vla.perception_system = {
                'detect_objects': AsyncMock(return_value={
                    'detected_objects': [{'class': 'cube', 'color': 'red'}]
                }),
                'ground_language_to_perception': AsyncMock(return_value={
                    'target_entities': [{'entity': 'red cube'}]
                })
            }
            mock_vla.planning_system = AsyncMock(return_value={
                'action_sequence': [{'action': 'pick', 'object': 'red cube'}]
            })

            mock_execute.return_value = {"status": "success"}

            # Test the function
            result = asyncio.run(
                self.apps.object_interaction_task("Pick up the red cube", "mock_image")
            )

            # Verify results
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["execution_result"]["status"], "success")

class TestROSBridge(unittest.TestCase):
    """Tests for ROS bridge functionality"""

    def test_laser_callback(self):
        """Test laser scan callback"""
        from ros_bridge import ROSBridge

        bridge = ROSBridge.__new__(ROSBridge)  # Create without calling __init__
        bridge.sensor_data = {'laser': None}
        bridge.connected_clients = set()

        # Create mock LaserScan message
        class MockLaserScan:
            def __init__(self):
                self.ranges = [1.0, 2.0, 3.0]
                self.intensities = [0.5, 0.6, 0.7]
                self.angle_min = -1.57
                self.angle_max = 1.57
                self.angle_increment = 0.1
                self.time_increment = 0.0
                self.scan_time = 0.0
                self.range_min = 0.1
                self.range_max = 30.0

        msg = MockLaserScan()
        bridge.laser_callback(msg)

        # Verify data was stored
        self.assertIsNotNone(bridge.sensor_data['laser'])
        self.assertEqual(bridge.sensor_data['laser']['ranges'], [1.0, 2.0, 3.0])

def run_integration_tests():
    """Run all integration tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == '__main__':
    run_integration_tests()
```

## Performance Optimization

### Async Optimization Techniques

```python
# performance_optimization.py
import asyncio
import concurrent.futures
from functools import partial
import time
from typing import Callable, Any
import threading

class PerformanceOptimizer:
    """Performance optimization for the integrated system"""

    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.processing_queue = asyncio.Queue()
        self.result_cache = {}
        self.cache_lock = threading.Lock()

    async def optimized_process_sensor_data(self, sensor_type: str, data: Any) -> Any:
        """Optimized sensor data processing with caching and parallel execution"""

        # Create cache key
        cache_key = f"{sensor_type}_{hash(str(data)) % 10000}"

        # Check cache first
        with self.cache_lock:
            if cache_key in self.result_cache:
                return self.result_cache[cache_key]

        # Process data using appropriate method
        if sensor_type == 'camera':
            result = await self._process_camera_data_optimized(data)
        elif sensor_type == 'laser':
            result = await self._process_laser_data_optimized(data)
        elif sensor_type == 'imu':
            result = await self._process_imu_data_optimized(data)
        else:
            result = data  # Default: return as-is

        # Cache result
        with self.cache_lock:
            self.result_cache[cache_key] = result
            # Limit cache size
            if len(self.result_cache) > 1000:
                # Remove oldest entries
                oldest_key = next(iter(self.result_cache))
                del self.result_cache[oldest_key]

        return result

    async def _process_camera_data_optimized(self, data: Any) -> Any:
        """Optimized camera data processing"""
        # Use thread pool for CPU-intensive image processing
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            partial(self._cpu_intensive_image_processing, data)
        )
        return result

    async def _process_laser_data_optimized(self, data: Any) -> Any:
        """Optimized laser data processing"""
        # Use asyncio for I/O-bound operations
        return await self._async_laser_processing(data)

    def _cpu_intensive_image_processing(self, image_data):
        """CPU-intensive image processing (runs in thread pool)"""
        # This would contain actual image processing code
        # For example: object detection, feature extraction, etc.
        time.sleep(0.01)  # Simulate processing time
        return {"processed": True, "features": []}

    async def _async_laser_processing(self, laser_data):
        """Async laser processing"""
        # This would contain laser processing code
        # For example: obstacle detection, mapping, etc.
        await asyncio.sleep(0.001)  # Simulate async processing
        return {"processed": True, "obstacles": []}

    def batch_process_requests(self, requests: list) -> list:
        """Batch process multiple requests for efficiency"""
        # Process requests in batches to improve throughput
        results = []

        # Group similar requests
        camera_requests = [r for r in requests if r['type'] == 'camera']
        laser_requests = [r for r in requests if r['type'] == 'laser']

        # Process in parallel using thread pool
        with concurrent.futures.ThreadPoolExecutor() as executor:
            camera_future = executor.submit(self._process_camera_batch, camera_requests)
            laser_future = executor.submit(self._process_laser_batch, laser_requests)

            camera_results = camera_future.result()
            laser_results = laser_future.result()

        results.extend(camera_results)
        results.extend(laser_results)

        return results

    def _process_camera_batch(self, requests):
        """Process camera requests in batch"""
        return [{"id": r['id'], "result": "processed"} for r in requests]

    def _process_laser_batch(self, requests):
        """Process laser requests in batch"""
        return [{"id": r['id'], "result": "processed"} for r in requests]

# Global performance optimizer instance
perf_optimizer = PerformanceOptimizer()
```

## Best Practices for Development

### Code Organization

1. **Modular Design**: Keep components loosely coupled
2. **Async First**: Use async/await for I/O operations
3. **Error Handling**: Implement comprehensive error handling
4. **Logging**: Use structured logging for debugging
5. **Testing**: Write comprehensive unit and integration tests

### Performance Guidelines

1. **Resource Management**: Properly manage GPU and memory resources
2. **Concurrency**: Use appropriate concurrency models (async vs threading)
3. **Caching**: Implement caching for expensive operations
4. **Monitoring**: Monitor system performance and resource usage
5. **Scalability**: Design for horizontal scaling when possible

## Summary

This chapter covered the implementation of the integrated Physical AI & Humanoid Robotics platform, including the main integration framework, communication bridges, unified control interfaces, and end-to-end applications. The next section will cover deployment and production considerations.