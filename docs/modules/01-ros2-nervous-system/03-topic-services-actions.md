# Chapter 3: Topics, Services, and Actions Implementation

## Overview

This chapter provides practical implementation details for topics, services, and actions in ROS 2, with complete examples and best practices for robotics applications.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Implement complete publisher-subscriber patterns with proper error handling
2. Create robust service clients and servers with timeout management
3. Develop action clients and servers with feedback and goal management
4. Apply best practices for communication in robotics systems

## Complete Topic Implementation

### Publisher with Error Handling

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import math

class RobustPublisher(Node):
    def __init__(self):
        super().__init__('robust_publisher')

        # Create publisher with custom QoS
        from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher_ = self.create_publisher(String, 'robot_status', qos_profile)
        self.error_publisher_ = self.create_publisher(String, 'errors', qos_profile)

        # Timer for periodic publishing
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.status_counter = 0

    def timer_callback(self):
        try:
            msg = String()
            msg.data = f'Robot status update: {self.status_counter}'
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: {msg.data}')
            self.status_counter += 1

        except Exception as e:
            error_msg = String()
            error_msg.data = f'Error in publisher: {str(e)}'
            self.error_publisher_.publish(error_msg)
            self.get_logger().error(f'Publisher error: {str(e)}')

    def destroy_node(self):
        self.get_logger().info('Shutting down robust publisher...')
        super().destroy_node()
```

### Subscriber with Data Processing

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import numpy as np

class DataProcessingSubscriber(Node):
    def __init__(self):
        super().__init__('data_processing_subscriber')

        # Subscribe to robot status
        self.subscription = self.create_subscription(
            String,
            'robot_status',
            self.status_callback,
            10)

        # Subscribe to sensor data
        self.laser_subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10)

        self.subscription  # prevent unused variable warning
        self.laser_subscription

        # Data storage
        self.status_history = []
        self.obstacle_distances = []

    def status_callback(self, msg):
        self.get_logger().info(f'Received status: {msg.data}')
        self.status_history.append(msg.data)

        # Keep only recent history
        if len(self.status_history) > 100:
            self.status_history.pop(0)

    def laser_callback(self, msg):
        # Process laser scan data
        valid_ranges = [r for r in msg.ranges if not math.isnan(r) and r > 0]

        if valid_ranges:
            min_distance = min(valid_ranges)
            self.obstacle_distances.append(min_distance)

            if min_distance < 0.5:  # Less than 50cm
                self.get_logger().warn(f'Obstacle detected at {min_distance:.2f}m')
```

## Complete Service Implementation

### Service Server with Validation

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

class ValidatedService(Node):
    def __init__(self):
        super().__init__('validated_service')
        self.srv = self.create_service(
            AddTwoInts,
            'validated_add_two_ints',
            self.add_two_ints_callback
        )
        self.request_counter = 0

    def add_two_ints_callback(self, request, response):
        # Validate input
        if request.a < -1000 or request.a > 1000 or request.b < -1000 or request.b > 1000:
            self.get_logger().error('Input values out of range')
            response.sum = 0
            return response

        response.sum = request.a + request.b
        self.request_counter += 1

        self.get_logger().info(
            f'Processed request #{self.request_counter}: {request.a} + {request.b} = {response.sum}'
        )
        return response

### Service Client with Timeout

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import time

class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        self.cli = self.create_client(AddTwoInts, 'validated_add_two_ints')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.request = AddTwoInts.Request()

    def send_request(self, a, b):
        self.request.a = a
        self.request.b = b

        # Make asynchronous call with timeout
        future = self.cli.call_async(self.request)

        # Wait for response with timeout
        start_time = time.time()
        timeout = 5.0  # 5 seconds timeout

        while rclpy.ok():
            if future.done():
                try:
                    response = future.result()
                    return response.sum
                except Exception as e:
                    self.get_logger().error(f'Service call failed: {e}')
                    return None

            if time.time() - start_time > timeout:
                self.get_logger().error('Service call timed out')
                return None

            rclpy.spin_once(self, timeout_sec=0.1)
```

## Complete Action Implementation

### Action Server with Complex Logic

```python
import time
import rclpy
from rclpy.action import ActionServer, CancelResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class ComplexActionServer(Node):
    def __init__(self):
        super().__init__('complex_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'complex_fibonacci',
            self.execute_callback,
            cancel_callback=self.cancel_callback)

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing complex fibonacci goal...')

        # Initialize feedback
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        # Execute with periodic feedback
        for i in range(1, goal_handle.request.order):
            # Check for cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            # Calculate next Fibonacci number
            next_num = feedback_msg.sequence[i] + feedback_msg.sequence[i-1]
            feedback_msg.sequence.append(next_num)

            # Publish feedback
            self.get_logger().info(f'Publishing feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)

            # Simulate work
            time.sleep(0.5)

        # Complete successfully
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Returning result: {result.sequence}')

        return result
```

### Action Client with Full Control

```python
import time
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class ActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'complex_fibonacci')

    def send_goal(self, order):
        # Wait for action server
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        # Create goal
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # Send goal
        self.get_logger().info(f'Sending goal: {order}')
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.sequence}')
```

## Integration Example: Robot Control System

Here's a complete example that integrates all three communication patterns:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from example_interfaces.srv import SetBool
from example_interfaces.action import NavigateToPose
from rclpy.action import ActionServer
from geometry_msgs.msg import PoseStamped

class RobotControlSystem(Node):
    def __init__(self):
        super().__init__('robot_control_system')

        # Publishers
        self.status_pub = self.create_publisher(String, 'robot_status', 10)
        self.emergency_pub = self.create_publisher(Bool, 'emergency_stop', 10)

        # Subscribers
        self.cmd_sub = self.create_subscription(
            String, 'command', self.command_callback, 10)

        # Services
        self.service = self.create_service(
            SetBool, 'enable_robot', self.enable_robot_callback)

        # Actions
        self.nav_server = ActionServer(
            self, NavigateToPose, 'navigate_to_pose', self.navigate_callback)

        # Internal state
        self.robot_enabled = False
        self.current_pose = None

    def command_callback(self, msg):
        if not self.robot_enabled:
            self.get_logger().warn('Robot is disabled, ignoring command')
            return

        # Process command
        command = msg.data.lower()
        if command == 'stop':
            self.emergency_pub.publish(Bool(data=True))
        elif command.startswith('move_to:'):
            # Extract target pose from command
            pass

    def enable_robot_callback(self, request, response):
        self.robot_enabled = request.data
        response.success = True
        response.message = f'Robot {"enabled" if self.robot_enabled else "disabled"}'
        return response

    def navigate_callback(self, goal_handle):
        if not self.robot_enabled:
            goal_handle.abort()
            result = NavigateToPose.Result()
            result.error_code = -1
            return result

        # Navigate to pose logic here
        goal_handle.succeed()
        result = NavigateToPose.Result()
        result.error_code = 0
        return result
```

## Performance Considerations

### Memory Management
- Use appropriate queue sizes to balance memory usage and performance
- Implement data pruning for long-running systems

### Network Efficiency
- Use appropriate QoS settings for your network conditions
- Compress large messages when possible

### Error Handling
- Implement timeouts for all communication patterns
- Handle connection failures gracefully
- Log errors for debugging

## Summary

This chapter provided complete implementations of ROS 2 communication patterns. The next chapter will cover ROS 2 integration with Python and C++.