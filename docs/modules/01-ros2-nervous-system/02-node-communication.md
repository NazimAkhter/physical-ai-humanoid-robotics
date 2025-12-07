# Chapter 2: Node Communication Patterns

## Overview

This chapter explores the communication patterns in ROS 2: topics, services, and actions, which form the nervous system for robotics applications.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Implement topic-based communication for streaming data
2. Create service-based communication for request-response patterns
3. Use action-based communication for goal-oriented tasks
4. Understand Quality of Service (QoS) settings for different communication needs

## Topic-Based Communication

Topics enable unidirectional, streaming communication between nodes using a publish/subscribe pattern.

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')
```

## Service-Based Communication

Services provide bidirectional request-response communication for synchronous operations.

### Service Server Example

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning: {response.sum}')
        return response
```

## Action-Based Communication

Actions are used for long-running tasks that provide feedback and can be canceled.

### Action Server Example

```python
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])

            self.get_logger().info(f'Publishing feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Returning result: {result.sequence}')

        return result
```

## Quality of Service (QoS) Settings

QoS settings allow fine-tuning communication behavior:

### Reliability Policy

- **Reliable**: All messages are delivered (like TCP)
- **Best Effort**: Messages may be lost (like UDP)

### Durability Policy

- **Transient Local**: Publishers get messages sent before they started
- **Volatile**: No message persistence

### History Policy

- **Keep Last**: Keep N most recent messages
- **Keep All**: Keep all messages

### Example QoS Configuration

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

# For critical data (e.g., safety commands)
critical_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=10
)

# For high-frequency sensor data
sensor_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=5
)
```

## Communication Patterns Comparison

| Pattern | Use Case | Characteristics |
|---------|----------|-----------------|
| Topics | Sensor data, status updates | Unidirectional, asynchronous |
| Services | Simple queries, configuration | Bidirectional, synchronous |
| Actions | Long-running tasks | Bidirectional, with feedback |

## Best Practices

1. **Topic naming**: Use descriptive, consistent names
2. **Message design**: Keep messages efficient and well-structured
3. **QoS selection**: Match QoS settings to your application requirements
4. **Error handling**: Implement proper error handling for all communication patterns

## Summary

This chapter covered the three main communication patterns in ROS 2. The next chapter will explore implementing these patterns in Python and C++.