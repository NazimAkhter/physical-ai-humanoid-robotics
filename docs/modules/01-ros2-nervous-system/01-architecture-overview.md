# Chapter 1: ROS 2 Architecture Overview

## Overview

This chapter provides an introduction to the ROS 2 architecture and its role as the nervous system for robotics applications.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Understand the ROS 2 architecture and its components
2. Identify the differences between ROS 1 and ROS 2
3. Recognize the role of DDS in ROS 2 communication
4. Configure ROS 2 environments and workspaces

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is the next generation of the Robot Operating System, designed to address the limitations of ROS 1 and provide a more robust, scalable, and production-ready framework for robotics development.

### Key Features of ROS 2

- **Real-time support**: Better real-time capabilities for time-critical applications
- **Multi-robot systems**: Improved support for multi-robot systems
- **Security**: Built-in security features for safe robot operation
- **DDS-based communication**: Uses Data Distribution Service (DDS) for communication
- **Quality of Service (QoS)**: Configurable communication policies

## DDS in ROS 2

Data Distribution Service (DDS) is the middleware that powers ROS 2 communication. It provides:

- **Decentralized communication**: No single point of failure
- **Quality of Service policies**: Configurable reliability and performance settings
- **Language independence**: Support for multiple programming languages
- **Platform independence**: Works across different operating systems

## ROS 2 Concepts

### Nodes

Nodes are the fundamental building blocks of ROS 2 applications. Each node runs a specific task and communicates with other nodes through:

- **Topics**: For streaming data
- **Services**: For request-response communication
- **Actions**: For goal-oriented communication with feedback

### Topics, Services, and Actions

These three communication patterns form the core of ROS 2 communication:

- **Topics**: Unidirectional streaming data (publish/subscribe)
- **Services**: Bidirectional request/response communication
- **Actions**: Long-running tasks with goal, feedback, and result

## Setting Up ROS 2

### Installation

ROS 2 can be installed on various platforms:

1. Ubuntu Linux (recommended)
2. Windows
3. macOS
4. Docker containers

### Environment Setup

After installation, set up your ROS 2 environment:

```bash
source /opt/ros/humble/setup.bash  # For ROS 2 Humble Hawksbill
```

## Creating Your First ROS 2 Package

ROS 2 packages organize code and resources:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Summary

This chapter introduced the fundamental concepts of ROS 2 architecture. The next chapter will cover node communication patterns in detail.