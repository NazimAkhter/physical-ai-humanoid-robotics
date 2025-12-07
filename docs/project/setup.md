# Project Setup

## Overview

This chapter provides detailed instructions for setting up the complete Physical AI & Humanoid Robotics platform, including all required software components, dependencies, and initial configuration.

## System Requirements

### Hardware Requirements
- **Development Machine**:
  - CPU: 8+ core processor (Intel i7 / AMD Ryzen 7 or better)
  - RAM: 32GB or more
  - GPU: NVIDIA RTX 3080 / RTX 4080 or better (24GB VRAM recommended)
  - Storage: 256GB SSD for OS + 1TB+ for datasets and models

- **Robot Platform** (Optional for simulation-only):
  - Compute: NVIDIA Jetson AGX Orin or equivalent
  - Sensors: RGB-D camera, IMU, encoders
  - Actuators: Servo motors or other actuators

### Software Requirements
- **Operating System**: Ubuntu 22.04 LTS (recommended) or Windows 11 with WSL2
- **Docker**: Version 20.10 or higher
- **NVIDIA Drivers**: Version 535 or higher with CUDA support
- **Python**: Version 3.8 - 3.11

## Prerequisites Installation

### 1. Install System Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential cmake git curl wget unzip htop iotop

# Install graphics and display libraries
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# Install audio libraries (for voice processing)
sudo apt install -y pulseaudio alsa-utils

# Install additional utilities
sudo apt install -y python3-pip python3-dev python3-venv
```

### 2. Install NVIDIA Drivers and CUDA

```bash
# Add NVIDIA package repository
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update

# Install CUDA toolkit
sudo apt install -y cuda-toolkit-12-8

# Install NVIDIA Container Toolkit for Docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 3. Install Docker

```bash
# Remove old versions
sudo apt remove docker docker-engine docker.io containerd runc

# Install Docker using convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker run hello-world
```

## ROS 2 Installation (Humble Hawksbill)

### 1. Set up sources

```bash
# Add ROS 2 GPG key
sudo apt update && sudo apt install -y curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add ROS 2 repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update package list
sudo apt update
```

### 2. Install ROS 2 packages

```bash
# Install ROS 2 Humble desktop
sudo apt install -y ros-humble-desktop
sudo apt install -y ros-humble-ros-base

# Install additional ROS packages for robotics
sudo apt install -y ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install -y ros-humble-moveit ros-humble-moveit-visual-tools
sudo apt install -y ros-humble-ros-gz ros-humble-gazebo-ros-pkgs
sudo apt install -y ros-humble-rosbridge-suite ros-humble-web-video-server
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool
```

### 3. Initialize rosdep and setup environment

```bash
# Initialize rosdep
sudo rosdep init
rosdep update

# Setup environment
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Isaac Sim Installation

### Option 1: Docker Installation (Recommended)

```bash
# Pull Isaac Sim Docker image
docker pull nvcr.io/nvidia/isaac-sim:4.2.0

# Create a script to run Isaac Sim
cat << 'EOF' > ~/run-isaac-sim.sh
#!/bin/bash
xhost +local:docker
docker run --gpus all \
  --rm \
  -e "ACCEPT_EULA=Y" \
  -e "PRIVACY_CONSENT=Y" \
  --network=host \
  --pid=host \
  --mount "type=bind,src=/tmp/.X11-unix,dst=/tmp/.X11-unix,readonly" \
  --mount "type=bind,src=/home/$USER,dst=/home/$USER" \
  --mount "type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock" \
  --mount "type=bind,src=/dev/dri,dst=/dev/dri,readonly" \
  --device /dev/snd \
  -v /home/$USER/.Xauthority:/root/.Xauthority:rw \
  --privileged \
  --name isaac-sim \
  nvcr.io/nvidia/isaac-sim:4.2.0
EOF

chmod +x ~/run-isaac-sim.sh
```

### Option 2: Local Installation

```bash
# Download Isaac Sim from NVIDIA Developer website
# Follow the installation instructions for local setup
# This requires more complex configuration but offers better performance
```

## Unity Setup for Robotics

### 1. Install Unity Hub and Editor

```bash
# Download Unity Hub from Unity website
# Install Unity 2022.3 LTS version
# Install packages:
# - Universal Render Pipeline
# - Unity Robotics Hub
# - Visual Scripting
```

### 2. Install Unity Robotics Packages

In Unity Package Manager, install:
- ROS-TCP-Connector
- URDF-Importer
- Robotics Examples

## Python Environment Setup

### 1. Create Virtual Environment

```bash
# Create project directory
mkdir ~/physical_ai_project
cd ~/physical_ai_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### 2. Install Python Dependencies

```bash
# Install core dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install tensorflow[and-cuda]
pip install numpy scipy matplotlib pandas

# Install robotics libraries
pip install transforms3d pyquaternion
pip install opencv-python open3d
pip install scipy scikit-image scikit-learn

# Install AI and ML libraries
pip install transformers datasets accelerate
pip install stable-baselines3[extra] sb3-contrib
pip install torchmetrics torchinfo

# Install API and web libraries
pip install fastapi uvicorn openai
pip install python-multipart python-dotenv
pip install requests aiohttp websockets

# Install visualization libraries
pip install plotly dash
pip install tensorboard wandb
```

### 3. Install Isaac Sim Python Packages

```bash
# Install Isaac Sim Python extensions
pip install omni-isaac-gym-py
pip install omni-isaac-orbit
pip install pxr-usd

# Install synthetic data generation tools
pip install omni.synthetic-utils
```

## Environment Configuration

### 1. Create Environment File

```bash
cat << 'EOF' > .env
# ROS 2 Configuration
ROS_DOMAIN_ID=0
ROS_LOG_DIR=./logs

# OpenAI Configuration (for VLA module)
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Configuration (for RAG)
QDRANT_URL=http://localhost:6333

# Database Configuration
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# Unity ROS Connection
UNITY_ROS_IP=127.0.0.1
UNITY_ROS_PORT=10000

# Isaac Sim Configuration
ISAAC_SIM_HEADLESS=0
ISAAC_SIM_VIEWER_WIDTH=1280
ISAAC_SIM_VIEWER_HEIGHT=720
EOF
```

### 2. Create Project Structure

```bash
# Create main project directories
mkdir -p {ros2_ws/src,isaac_ws/models,unity_project,vla_api/{voice,planning,perception},docs,scripts,tests}

# ROS 2 workspace setup
cd ~/physical_ai_project/ros2_ws
colcon build --symlink-install

# Source ROS 2 workspace
echo "source ~/physical_ai_project/ros2_ws/install/setup.bash" >> ~/.bashrc
```

## Testing Individual Components

### 1. Test ROS 2 Installation

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Test ROS 2
ros2 run demo_nodes_cpp talker &
ros2 run demo_nodes_py listener

# Should see messages passing between nodes
```

### 2. Test Isaac Sim Installation

```bash
# Run Isaac Sim Docker container
~/run-isaac-sim.sh

# In Isaac Sim, run a simple test script:
# Open Isaac Sim, create new stage, add a cube, run simulation
```

### 3. Test Python Environment

```bash
# Activate virtual environment
source ~/physical_ai_project/venv/bin/activate

# Test Python packages
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
```

## Workspace Configuration

### 1. Create Workspace Initialization Script

```bash
cat << 'EOF' > ~/physical_ai_project/setup_workspace.sh
#!/bin/bash

# Source ROS 2
source /opt/ros/humble/setup.bash
source ~/physical_ai_project/ros2_ws/install/setup.bash

# Activate Python virtual environment
source ~/physical_ai_project/venv/bin/activate

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:~/physical_ai_project/vla_api"
export GAZEBO_MODEL_PATH="${GAZEBO_MODEL_PATH}:~/physical_ai_project/isaac_ws/models"

# Print setup confirmation
echo "Physical AI Project workspace initialized!"
echo "ROS Domain ID: $ROS_DOMAIN_ID"
echo "Python Environment: $(python --version)"
EOF

chmod +x ~/physical_ai_project/setup_workspace.sh
```

### 2. Create Development Aliases

```bash
cat << 'EOF' >> ~/.bashrc

# Physical AI Project aliases
alias psetup='source ~/physical_ai_project/setup_workspace.sh'
alias pisaac='~/run-isaac-sim.sh'
alias pdocs='cd ~/physical_ai_project && python -m http.server 8000'
alias ptest='cd ~/physical_ai_project && python -m pytest tests/'
EOF

source ~/.bashrc
```

## Troubleshooting Common Issues

### 1. GPU Memory Issues
- Reduce Isaac Sim rendering quality during training
- Use smaller neural network models for initial testing
- Monitor GPU memory with `nvidia-smi`

### 2. ROS 2 Connection Issues
- Check ROS_DOMAIN_ID consistency across systems
- Verify network connectivity for multi-machine setups
- Ensure proper ROS 2 environment sourcing

### 3. Python Package Conflicts
- Use virtual environments to isolate dependencies
- Check package compatibility requirements
- Use conda if pip installations fail

## Next Steps

After completing the setup, proceed to the [Development](./development.md) section to learn about implementing the integrated system. The environment is now ready for developing the complete Physical AI & Humanoid Robotics platform.