# Chapter 4: ROS 2 with Python and C++

## Overview

This chapter covers implementing ROS 2 applications in both Python and C++, highlighting the advantages of each language for different robotics applications.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Create ROS 2 packages in both Python and C++
2. Implement nodes, publishers, and subscribers in both languages
3. Choose appropriate languages for different robotics components
4. Integrate Python and C++ nodes in the same system

## Python in ROS 2

Python is ideal for rapid prototyping, AI integration, and high-level control in robotics applications.

### Python Package Structure

```
my_robot_py/
├── CMakeLists.txt
├── package.xml
├── setup.py
├── setup.cfg
└── my_robot_py/
    ├── __init__.py
    ├── publisher_member_function.py
    └── subscriber_member_function.py
```

### Python Node Implementation

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import numpy as np

class PythonRobotController(Node):
    def __init__(self):
        super().__init__('python_robot_controller')

        # Publishers
        self.cmd_publisher = self.create_publisher(String, 'robot_command', 10)

        # Subscribers
        self.laser_sub = self.create_subscription(
            LaserScan, 'scan', self.laser_callback, 10)

        # Timers
        self.control_timer = self.create_timer(0.1, self.control_loop)

        # Internal state
        self.laser_data = None
        self.robot_state = 'idle'

    def laser_callback(self, msg):
        """Process laser scan data"""
        # Convert to numpy array for efficient processing
        ranges = np.array(msg.ranges)
        # Filter out invalid ranges
        valid_ranges = ranges[np.isfinite(ranges) & (ranges > 0)]

        if len(valid_ranges) > 0:
            self.closest_obstacle = np.min(valid_ranges)
        else:
            self.closest_obstacle = float('inf')

    def control_loop(self):
        """Main control loop"""
        if self.robot_state == 'idle':
            self.navigate_safely()
        elif self.robot_state == 'navigating':
            self.check_navigation_progress()

    def navigate_safely(self):
        """Safe navigation logic"""
        if hasattr(self, 'closest_obstacle') and self.closest_obstacle < 0.5:
            # Stop if obstacle too close
            cmd_msg = String()
            cmd_msg.data = 'STOP'
            self.cmd_publisher.publish(cmd_msg)
        else:
            # Continue navigation
            cmd_msg = String()
            cmd_msg.data = 'FORWARD'
            self.cmd_publisher.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    controller = PythonRobotController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Interrupted by user')
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Python Service Implementation

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
import threading
import time

class PythonCalculatorService(Node):
    def __init__(self):
        super().__init__('python_calculator_service')
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.add_callback)

        # Simulate complex computation
        self.computation_lock = threading.Lock()
        self.active_computations = 0

    def add_callback(self, request, response):
        with self.computation_lock:
            self.active_computations += 1
            self.get_logger().info(
                f'Starting computation #{self.active_computations}: {request.a} + {request.b}'
            )

        # Simulate computation time
        time.sleep(0.1)

        response.sum = request.a + request.b

        with self.computation_lock:
            self.active_computations -= 1
            self.get_logger().info(f'Result: {response.sum}')

        return response

def main(args=None):
    rclpy.init(args=args)
    service = PythonCalculatorService()

    try:
        rclpy.spin(service)
    except KeyboardInterrupt:
        service.get_logger().info('Service interrupted')
    finally:
        service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## C++ in ROS 2

C++ is ideal for performance-critical applications, real-time systems, and low-level hardware interfaces.

### C++ Package Structure

```
my_robot_cpp/
├── CMakeLists.txt
├── package.xml
└── src/
    ├── publisher_member_function.cpp
    └── subscriber_member_function.cpp
```

### C++ Node Implementation

```cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

using namespace std::chrono_literals;

class CppRobotController : public rclcpp::Node
{
public:
    CppRobotController()
    : Node("cpp_robot_controller"), closest_obstacle_(std::numeric_limits<float>::infinity())
    {
        // Publishers
        cmd_publisher_ = this->create_publisher<std_msgs::msg::String>("robot_command", 10);

        // Subscribers
        laser_subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "scan", 10,
            std::bind(&CppRobotController::laser_callback, this, std::placeholders::_1));

        // Timer
        timer_ = this->create_wall_timer(
            100ms, std::bind(&CppRobotController::control_loop, this));
    }

private:
    void laser_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        float min_range = std::numeric_limits<float>::infinity();

        for (const auto& range : msg->ranges) {
            if (std::isfinite(range) && range > 0 && range < min_range) {
                min_range = range;
            }
        }

        closest_obstacle_ = min_range;
        RCLCPP_DEBUG(this->get_logger(), "Closest obstacle: %f", closest_obstacle_);
    }

    void control_loop()
    {
        auto cmd_msg = std_msgs::msg::String();

        if (closest_obstacle_ < 0.5) {
            cmd_msg.data = "STOP";
        } else {
            cmd_msg.data = "FORWARD";
        }

        cmd_publisher_->publish(cmd_msg);
        RCLCPP_DEBUG(this->get_logger(), "Published command: %s", cmd_msg.data.c_str());
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr cmd_publisher_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr laser_subscription_;
    float closest_obstacle_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CppRobotController>());
    rclcpp::shutdown();
    return 0;
}
```

### C++ Service Implementation

```cpp
#include "example_interfaces/srv/add_two_ints.hpp"
#include "rclcpp/rclcpp.hpp"

#include <chrono>
#include <cstdlib>
#include <memory>

class CppCalculatorService : public rclcpp::Node
{
public:
    CppCalculatorService()
    : Node("cpp_calculator_service")
    {
        service_ = this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_two_ints",
            [this](const example_interfaces::srv::AddTwoInts::Request::SharedPtr request,
                   example_interfaces::srv::AddTwoInts::Response::SharedPtr response) -> void
            {
                RCLCPP_INFO(this->get_logger(), "Incoming request: %ld + %ld",
                           request->a, request->b);

                // Simulate computation
                std::this_thread::sleep_for(std::chrono::milliseconds(50));

                response->sum = request->a + request->b;
                RCLCPP_INFO(this->get_logger(), "Sending result: %ld", response->sum);
            });
    }

private:
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CppCalculatorService>());
    rclcpp::shutdown();
    return 0;
}
```

## CMakeLists.txt for C++ Package

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)

# Declare C++ executables
add_executable(robot_controller src/robot_controller.cpp)
add_executable(calculator_service src/calculator_service.cpp)

# Link libraries to executables
ament_target_dependencies(robot_controller
  rclcpp
  std_msgs
  sensor_msgs
)

ament_target_dependencies(calculator_service
  rclcpp
  example_interfaces
)

# Install executables
install(TARGETS
  robot_controller
  calculator_service
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
```

## Language Selection Guidelines

### Use Python When:
- Rapid prototyping and development
- AI/ML integration (TensorFlow, PyTorch)
- High-level decision making
- Data processing and visualization
- Web services integration
- Complex algorithms that don't require real-time performance

### Use C++ When:
- Real-time performance requirements
- Low-level hardware interfaces
- High-frequency control loops
- Memory-constrained environments
- Integration with existing C/C++ libraries
- Performance-critical applications

## Integration Patterns

### Mixed-Language Systems

In most robotics applications, you'll use both languages:

```
Python Nodes (High-level logic, AI)
    ↔ ROS 2 Middleware
        ↔ C++ Nodes (Low-level control, performance)
```

### Example: Perception Pipeline

- **C++**: Image acquisition, low-level processing, sensor fusion
- **Python**: Object detection, decision making, path planning

### Data Sharing Between Languages

ROS 2 messages provide seamless data sharing:

```python
# Python node publishing sensor data
msg = sensor_msgs.msg.Image()
msg.data = processed_image_data
publisher.publish(msg)
```

```cpp
// C++ node subscribing to same topic
subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
    "processed_image", 10,
    [this](const sensor_msgs::msg::Image::SharedPtr msg) {
        // Process in C++ for performance
        process_image_high_performance(msg);
    });
```

## Performance Comparison

### Python Advantages:
- Faster development
- Rich ecosystem of libraries
- Easier debugging and testing
- Better for AI/ML integration

### C++ Advantages:
- Higher performance
- Better memory management
- Real-time capabilities
- Lower latency

### Hybrid Approach Benefits:
- Best of both worlds
- Optimize critical paths with C++
- Maintain flexibility with Python
- Separate concerns by performance needs

## Best Practices

1. **Separation of Concerns**: Use appropriate language for each component
2. **Interface Design**: Design clean interfaces between Python and C++ components
3. **Error Handling**: Implement robust error handling in both languages
4. **Testing**: Test components individually and as integrated systems
5. **Documentation**: Document interfaces between language boundaries

## Summary

This chapter covered implementing ROS 2 applications in both Python and C++. The choice of language depends on performance requirements, development speed needs, and existing codebase considerations. In the next module, we'll explore digital twin technologies with Gazebo and Unity.