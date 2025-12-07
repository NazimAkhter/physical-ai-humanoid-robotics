# Project Deployment

## Overview

This chapter covers the deployment of the Physical AI & Humanoid Robotics platform to production environments, including robot hardware, cloud infrastructure, and edge computing setups. We'll explore various deployment strategies and best practices for maintaining robust, scalable robotic systems.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Deploy the integrated platform to robot hardware
2. Set up cloud infrastructure for remote operation
3. Configure edge computing solutions for real-time processing
4. Implement monitoring and maintenance procedures
5. Create deployment pipelines for continuous integration

## Deployment Architectures

### On-Robot Deployment

For humanoid robots or mobile platforms with sufficient compute:

```
┌─────────────────────────────────────────┐
│              Robot Hardware             │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │   Physical AI Platform Core     │    │
│  │  ┌─────────────────────────────┐│    │
│  │  │ • ROS 2 Bridge              ││    │
│  │  │ • VLA Pipeline              ││    │
│  │  │ • Perception System         ││    │
│  │  │ • Control System            ││    │
│  │  └─────────────────────────────┘│    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │     AI Processing Engine        │    │
│  │  ┌─────────────────────────────┐│    │
│  │  │ • Vision Models             ││    │
│  │  │ • Language Models           ││    │
│  │  │ • Planning Models           ││    │
│  │  └─────────────────────────────┘│    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Cloud-Edge Hybrid Deployment

For scenarios requiring heavy AI computation:

```
┌─────────────────────────────────────────┐
│              Cloud Layer                │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │    AI Model Serving Cluster     │    │
│  │  ┌─────────────────────────────┐│    │
│  │  │ • Vision Model API          ││    │
│  │  │ • Language Model API        ││    │
│  │  │ • Planning Model API        ││    │
│  │  └─────────────────────────────┘│    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│              Edge Layer                 │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │      Robot Controller           │    │
│  │  ┌─────────────────────────────┐│    │
│  │  │ • ROS 2 Interface           ││    │
│  │  │ • Sensor Fusion             ││    │
│  │  │ • Control System            ││    │
│  │  │ • Local Perception          ││    │
│  │  └─────────────────────────────┘│    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## Robot Hardware Deployment

### System Requirements for Robot Deployment

#### Minimum Requirements
- **Compute**: NVIDIA Jetson AGX Orin (64GB RAM) or equivalent
- **GPU**: 10GB+ VRAM for AI inference
- **CPU**: 8+ core ARM64 processor
- **Storage**: 256GB NVMe SSD
- **Network**: WiFi 6 or Gigabit Ethernet

#### Recommended Requirements
- **Compute**: NVIDIA Jetson Orin Ultra (64GB RAM)
- **GPU**: 32GB VRAM for full model deployment
- **CPU**: 12+ core ARM64 processor
- **Storage**: 512GB+ NVMe SSD
- **Network**: Dual-band WiFi 6 + Ethernet

### Robot-Specific Installation

```bash
# Install system dependencies on robot
sudo apt update && sudo apt upgrade -y

# Install NVIDIA JetPack (includes CUDA, drivers, etc.)
# Follow NVIDIA's JetPack installation guide for your Jetson model

# Install robotics dependencies
sudo apt install -y ros-humble-desktop-full
sudo apt install -y ros-humble-navigation2 ros-humble-moveit
sudo apt install -y ros-humble-ros-gz ros-humble-gazebo-ros-pkgs

# Install Python environment
sudo apt install -y python3-pip python3-venv python3-dev

# Create robot-specific user
sudo useradd -m -s /bin/bash robot
sudo usermod -aG dialout,sudo robot
```

### Robot Platform Configuration

```yaml
# robot_config.yaml
robot:
  name: "physical_ai_robot"
  type: "humanoid"  # or "mobile_manipulator", "wheeled"

sensors:
  camera:
    topic: "/camera/image_raw"
    resolution: [640, 480]
    fps: 30
  lidar:
    topic: "/scan"
    range: [0.1, 25.0]
  imu:
    topic: "/imu/data"
  odometry:
    topic: "/odom"

actuators:
  joints:
    - name: "head_pan_joint"
      type: "revolute"
      limits: [-1.57, 1.57]
    - name: "head_tilt_joint"
      type: "revolute"
      limits: [-0.78, 0.78]
    # Add other joints as needed

control:
  max_linear_vel: 1.0  # m/s
  max_angular_vel: 1.0 # rad/s
  control_frequency: 50 # Hz

ai:
  model_paths:
    vision: "/models/vision.pt"
    language: "/models/language.pt"
    planning: "/models/planning.pt"
  inference_timeout: 5.0
```

### Deployment Scripts for Robot

```bash
#!/bin/bash
# deploy_to_robot.sh

set -e  # Exit on error

echo "Starting Physical AI Platform deployment to robot..."

# Configuration
ROBOT_IP="192.168.1.100"  # Update with robot IP
ROBOT_USER="robot"
DEPLOY_DIR="/home/robot/physical_ai_platform"

# Create deployment directory on robot
ssh $ROBOT_USER@$ROBOT_IP "mkdir -p $DEPLOY_DIR"

# Copy source code to robot
rsync -av --exclude '__pycache__' --exclude '.git' \
  ~/physical_ai_project/ $ROBOT_USER@$ROBOT_IP:$DEPLOY_DIR/

# Install Python dependencies on robot
ssh $ROBOT_USER@$ROBOT_IP << 'EOF'
cd /home/robot/physical_ai_platform

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements/robot_requirements.txt

# Install ROS packages
source /opt/ros/humble/setup.bash
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
EOF

echo "Deployment completed successfully!"
echo "To start the platform, SSH to the robot and run:"
echo "  cd $DEPLOY_DIR && source venv/bin/activate && python main_integration_framework.py"
```

## Containerized Deployment

### Docker Compose for Platform Services

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ROS 2 bridge service
  ros-bridge:
    build:
      context: .
      dockerfile: Dockerfile.ros
    container_name: physical_ai_ros_bridge
    network_mode: host
    environment:
      - ROS_DOMAIN_ID=0
      - ROS_IP=127.0.0.1
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
      - ./config:/app/config
    devices:
      - /dev/dri:/dev/dri
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
    restart: unless-stopped

  # VLA API service
  vla-api:
    build:
      context: .
      dockerfile: Dockerfile.vla
    container_name: physical_ai_vla_api
    ports:
      - "8001:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_URL=${QDRANT_URL}
    volumes:
      - ./models:/app/models
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '4.0'
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  # Web interface
  web-interface:
    build:
      context: .
      dockerfile: Dockerfile.web
    container_name: physical_ai_web
    ports:
      - "8000:8000"
    depends_on:
      - ros-bridge
      - vla-api
    environment:
      - BACKEND_URL=http://vla-api:8000
      - ROS_BRIDGE_URL=http://ros-bridge:8765
    restart: unless-stopped

  # Database for conversation history
  postgres:
    image: postgres:15
    container_name: physical_ai_postgres
    environment:
      POSTGRES_DB: physical_ai
      POSTGRES_USER: robot
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Vector database for RAG
  qdrant:
    image: qdrant/qdrant:latest
    container_name: physical_ai_qdrant
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
      - "6334:6334"
    restart: unless-stopped

volumes:
  postgres_data:
  qdrant_data:
```

### Dockerfile for ROS Bridge

```dockerfile
# Dockerfile.ros
FROM osrf/ros:humble-desktop-full-jammy

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN pip3 install --upgrade pip setuptools wheel

# Install ROS packages
RUN apt-get update && apt-get install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-moveit \
    ros-humble-moveit-visual-tools \
    ros-humble-ros-gz \
    ros-humble-gazebo-ros-pkgs \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /workspace
RUN mkdir -p ros2_ws/src

# Copy source code
COPY ros2_ws/src/ /workspace/ros2_ws/src/

# Build workspace
WORKDIR /workspace/ros2_ws
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install

# Source workspace
RUN echo "source /workspace/ros2_ws/install/setup.bash" >> ~/.bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Copy application code
COPY . /app/
WORKDIR /app

# Install Python dependencies
COPY requirements/robot_requirements.txt .
RUN pip3 install -r robot_requirements.txt

# Expose ports
EXPOSE 8765

# Default command
CMD ["bash", "-c", "source /opt/ros/humble/setup.bash && source /workspace/ros2_ws/install/setup.bash && python3 ros_bridge.py"]
```

### Kubernetes Deployment (Advanced)

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: physical-ai-platform
  labels:
    app: physical-ai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: physical-ai
  template:
    metadata:
      labels:
        app: physical-ai
    spec:
      containers:
      - name: ros-bridge
        image: physical-ai/ros-bridge:latest
        ports:
        - containerPort: 8765
        env:
        - name: ROS_DOMAIN_ID
          value: "0"
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
          limits:
            memory: "4Gi"
            cpu: "4"
        volumeMounts:
        - name: config-volume
          mountPath: /app/config

      - name: vla-api
        image: physical-ai/vla-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "4Gi"
            cpu: "4"
            nvidia.com/gpu: 1
          limits:
            memory: "8Gi"
            cpu: "8"
            nvidia.com/gpu: 1

      volumes:
      - name: config-volume
        configMap:
          name: physical-ai-config

---
apiVersion: v1
kind: Service
metadata:
  name: physical-ai-service
spec:
  selector:
    app: physical-ai
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Cloud Deployment

### AWS Deployment with EC2

```bash
#!/bin/bash
# aws_deployment.sh

# Create EC2 instance with GPU support
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \  # Ubuntu 22.04 with NVIDIA drivers
  --count 1 \
  --instance-type g4dn.xlarge \
  --key-name physical-ai-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --user-data file://cloud-init.sh

# Cloud init script
cat > cloud-init.sh << 'EOF'
#!/bin/bash

# Install Docker
apt-get update
apt-get install -y docker.io docker-compose-v2
usermod -aG docker ubuntu

# Install NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
apt-get update
apt-get install -y nvidia-container-toolkit
systemctl restart docker

# Clone and deploy application
git clone https://github.com/your-org/physical-ai-platform.git
cd physical-ai-platform
docker-compose up -d
EOF
```

### Docker Compose for Cloud Deployment

```yaml
# docker-compose.cloud.yml
version: '3.8'

services:
  # Cloud-optimized VLA API with load balancing
  vla-api:
    build:
      context: .
      dockerfile: Dockerfile.vla.cloud
    container_name: physical_ai_vla_api_cloud
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_URL=${QDRANT_URL}
      - MODEL_CACHE_DIR=/cache/models
    volumes:
      - /mnt/ssd/cache:/cache
      - ./models:/app/models:ro
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4.0'
          nvidia.com/gpu: 1
      replicas: 2
    restart: unless-stopped

  # Load balancer for API requests
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - vla-api
    restart: unless-stopped

  # Monitoring and logging
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  grafana_data:
```

## Edge Computing Deployment

### NVIDIA Fleet Command Setup

```yaml
# edge-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: physical-ai-edge
spec:
  replicas: 1
  selector:
    matchLabels:
      app: physical-ai-edge
  template:
    metadata:
      labels:
        app: physical-ai-edge
    spec:
      nodeSelector:
        nvidia.com/gpu.present: "true"
      containers:
      - name: perception-engine
        image: physical-ai/perception:edge-latest
        resources:
          requests:
            nvidia.com/gpu: 1
            memory: "4Gi"
            cpu: "4"
          limits:
            nvidia.com/gpu: 1
            memory: "8Gi"
            cpu: "8"
        env:
        - name: GPU_MEMORY_FRACTION
          value: "0.8"
        - name: BATCH_SIZE
          value: "4"
        volumeMounts:
        - name: models
          mountPath: /models
        - name: data
          mountPath: /data

      - name: control-engine
        image: physical-ai/control:edge-latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
          limits:
            memory: "4Gi"
            cpu: "4"
        env:
        - name: CONTROL_FREQ
          value: "50"
        - name: SAFETY_TIMEOUT
          value: "5.0"

      volumes:
      - name: models
        hostPath:
          path: /opt/models
          type: Directory
      - name: data
        hostPath:
          path: /opt/data
          type: Directory
```

## Monitoring and Observability

### System Monitoring Setup

```python
# monitoring.py
import psutil
import GPUtil
import time
import json
from datetime import datetime
from typing import Dict, Any
import asyncio
import aiohttp
from prometheus_client import Counter, Gauge, Histogram, start_http_server

class SystemMonitor:
    """System monitoring for the Physical AI platform"""

    def __init__(self, platform):
        self.platform = platform
        self.metrics = {
            'cpu_percent': Gauge('cpu_percent', 'CPU usage percentage'),
            'memory_percent': Gauge('memory_percent', 'Memory usage percentage'),
            'gpu_percent': Gauge('gpu_percent', 'GPU usage percentage'),
            'gpu_memory_percent': Gauge('gpu_memory_percent', 'GPU memory usage percentage'),
            'robot_status': Gauge('robot_status', 'Robot operational status'),
            'api_requests_total': Counter('api_requests_total', 'Total API requests'),
            'api_request_duration': Histogram('api_request_duration_seconds', 'API request duration'),
            'sensor_data_frequency': Gauge('sensor_data_frequency', 'Sensor data frequency'),
        }

    def collect_system_metrics(self) -> Dict[str, float]:
        """Collect system-level metrics"""
        metrics = {}

        # CPU metrics
        metrics['cpu_percent'] = psutil.cpu_percent()
        metrics['cpu_count'] = psutil.cpu_count()

        # Memory metrics
        memory = psutil.virtual_memory()
        metrics['memory_percent'] = memory.percent
        metrics['memory_available_gb'] = memory.available / (1024**3)
        metrics['memory_used_gb'] = memory.used / (1024**3)

        # GPU metrics
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Primary GPU
            metrics['gpu_percent'] = gpu.load * 100
            metrics['gpu_memory_percent'] = gpu.memoryUtil * 100
            metrics['gpu_temperature'] = gpu.temperature
            metrics['gpu_memory_used_gb'] = gpu.memoryUsed / 1024
            metrics['gpu_memory_total_gb'] = gpu.memoryTotal / 1024

        # Disk metrics
        disk = psutil.disk_usage('/')
        metrics['disk_percent'] = (disk.used / disk.total) * 100
        metrics['disk_free_gb'] = disk.free / (1024**3)

        return metrics

    def collect_platform_metrics(self) -> Dict[str, Any]:
        """Collect platform-specific metrics"""
        metrics = {}

        # Platform state
        if hasattr(self.platform, 'context'):
            metrics['platform_state'] = self.platform.context.state.value
            metrics['uptime_seconds'] = time.time() - self.platform.context.timestamp

        # ROS bridge metrics
        if hasattr(self.platform, 'ros_bridge'):
            # Count active subscribers/publishers
            metrics['ros_active_nodes'] = len(getattr(self.platform.ros_bridge, 'active_processes', {}))

        # AI model metrics
        if hasattr(self.platform, 'vla_pipeline'):
            # Track model inference times
            pass

        return metrics

    async def start_monitoring_loop(self):
        """Start the monitoring loop"""
        print("Starting system monitoring...")

        # Start Prometheus metrics server
        start_http_server(8002)

        while True:
            try:
                # Collect system metrics
                sys_metrics = self.collect_system_metrics()

                # Update Prometheus metrics
                for key, value in sys_metrics.items():
                    if key in self.metrics:
                        self.metrics[key].set(value)

                # Collect platform metrics
                platform_metrics = self.collect_platform_metrics()

                # Log metrics (in production, send to monitoring service)
                timestamp = datetime.now().isoformat()
                log_entry = {
                    'timestamp': timestamp,
                    'type': 'metrics',
                    'system': sys_metrics,
                    'platform': platform_metrics
                }

                print(f"Metrics collected: {json.dumps(log_entry, indent=2)}")

                # Wait before next collection
                await asyncio.sleep(5)  # Collect every 5 seconds

            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)

class HealthCheck:
    """Health check system for the platform"""

    def __init__(self, platform):
        self.platform = platform

    async def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {},
            'checks': {}
        }

        # Check ROS bridge
        ros_healthy = await self._check_ros_bridge()
        health_status['components']['ros_bridge'] = ros_healthy

        # Check AI services
        ai_healthy = await self._check_ai_services()
        health_status['components']['ai_services'] = ai_healthy

        # Check VLA pipeline
        vla_healthy = await self._check_vla_pipeline()
        health_status['components']['vla_pipeline'] = vla_healthy

        # Check digital twin
        twin_healthy = await self._check_digital_twin()
        health_status['components']['digital_twin'] = twin_healthy

        # Overall status
        all_healthy = all([
            ros_healthy['status'] == 'healthy',
            ai_healthy['status'] == 'healthy',
            vla_healthy['status'] == 'healthy',
            twin_healthy['status'] == 'healthy'
        ])

        health_status['overall_status'] = 'healthy' if all_healthy else 'degraded'

        return health_status

    async def _check_ros_bridge(self) -> Dict[str, Any]:
        """Check ROS bridge health"""
        try:
            # Check if ROS bridge is running
            if not self.platform.ros_bridge:
                return {'status': 'unhealthy', 'reason': 'ROS bridge not initialized'}

            # Check if ROS master is accessible
            # This would involve checking ROS topics/services

            return {'status': 'healthy', 'response_time_ms': 10}
        except Exception as e:
            return {'status': 'unhealthy', 'reason': str(e)}

    async def _check_ai_services(self) -> Dict[str, Any]:
        """Check AI services health"""
        try:
            # Check if AI models are loaded and responsive
            # This would involve testing model inference

            return {'status': 'healthy', 'models_loaded': 3}
        except Exception as e:
            return {'status': 'unhealthy', 'reason': str(e)}

    async def _check_vla_pipeline(self) -> Dict[str, Any]:
        """Check VLA pipeline health"""
        try:
            # Check if VLA components are available
            if not self.platform.vla_pipeline:
                return {'status': 'unhealthy', 'reason': 'VLA pipeline not initialized'}

            return {'status': 'healthy', 'components': 3}
        except Exception as e:
            return {'status': 'unhealthy', 'reason': str(e)}

    async def _check_digital_twin(self) -> Dict[str, Any]:
        """Check digital twin health"""
        try:
            # Check if digital twin is synchronized
            if not self.platform.digital_twin:
                return {'status': 'unhealthy', 'reason': 'Digital twin not initialized'}

            return {'status': 'healthy'}
        except Exception as e:
            return {'status': 'unhealthy', 'reason': str(e)}

# Example usage
async def run_monitoring_system():
    """Run the monitoring system"""
    # This would be integrated with the main platform
    pass
```

## Security and Access Control

### Authentication and Authorization

```python
# security.py
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import asyncio
import aiofiles

class AuthenticationManager:
    """Authentication and authorization for the platform"""

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.users = {}
        self.tokens = set()

    def create_user(self, username: str, password: str, roles: list = None) -> bool:
        """Create a new user account"""
        if username in self.users:
            return False

        # Hash password
        salt = secrets.token_hex(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        hashed_password_hex = hashed_password.hex()

        self.users[username] = {
            'password': hashed_password_hex,
            'salt': salt,
            'roles': roles or ['user'],
            'created_at': datetime.now().isoformat()
        }

        return True

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token"""
        if username not in self.users:
            return None

        user = self.users[username]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), user['salt'].encode(), 100000)
        hashed_password_hex = hashed_password.hex()

        if hashed_password_hex == user['password']:
            # Create JWT token
            token = jwt.encode({
                'user': username,
                'roles': user['roles'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, self.secret_key, algorithm='HS256')

            self.tokens.add(token)
            return {
                'token': token,
                'user': username,
                'roles': user['roles']
            }

        return None

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify authentication token"""
        if token not in self.tokens:
            return None

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.tokens.discard(token)
            return None
        except jwt.InvalidTokenError:
            return None

    def has_role(self, token: str, required_role: str) -> bool:
        """Check if user has required role"""
        payload = self.verify_token(token)
        if not payload:
            return False

        return required_role in payload.get('roles', [])

class RBACManager:
    """Role-Based Access Control manager"""

    def __init__(self):
        self.permissions = {
            'admin': ['read', 'write', 'execute', 'admin'],
            'operator': ['read', 'write', 'execute'],
            'user': ['read'],
            'guest': []
        }

        self.resource_permissions = {
            'robot_control': ['admin', 'operator'],
            'sensor_data': ['admin', 'operator', 'user'],
            'system_config': ['admin'],
            'logs': ['admin', 'operator']
        }

    def can_access(self, user_roles: list, resource: str, action: str) -> bool:
        """Check if user can perform action on resource"""
        # Check if any role has the required permission
        for role in user_roles:
            if role in self.permissions:
                role_permissions = self.permissions[role]
                if action in role_permissions:
                    # Check if role has access to resource
                    if role in self.resource_permissions.get(resource, []):
                        return True

        return False

# Example usage in API
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
auth_manager = AuthenticationManager()
rbac_manager = RBACManager()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    token = credentials.credentials
    user_data = auth_manager.verify_token(token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_data

def require_permission(resource: str, action: str):
    """Decorator to require specific permissions"""
    def permission_checker(current_user: dict = Depends(get_current_user)):
        if not rbac_manager.can_access(current_user['roles'], resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_checker
```

## Backup and Recovery

### Backup Strategy

```python
# backup.py
import asyncio
import shutil
import tarfile
import os
from datetime import datetime
from pathlib import Path
import boto3
from typing import List, Optional

class BackupManager:
    """Backup and recovery system for the platform"""

    def __init__(self, backup_dir: str = "/backups", retention_days: int = 30):
        self.backup_dir = Path(backup_dir)
        self.retention_days = retention_days
        self.backup_dir.mkdir(exist_ok=True)

    async def create_backup(self, backup_name: str = None) -> str:
        """Create a backup of the system"""
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_path = self.backup_dir / f"{backup_name}.tar.gz"

        # Define directories to backup
        backup_sources = [
            "/home/robot/physical_ai_platform/config",
            "/home/robot/physical_ai_platform/models",
            "/var/log/ros",
            "/home/robot/.ros/log"
        ]

        # Create backup archive
        with tarfile.open(backup_path, "w:gz") as tar:
            for source in backup_sources:
                source_path = Path(source)
                if source_path.exists():
                    tar.add(source_path, arcname=source_path.name)

        print(f"Backup created: {backup_path}")
        return str(backup_path)

    async def restore_backup(self, backup_path: str, restore_path: str = "/tmp/restore"):
        """Restore from backup"""
        restore_dir = Path(restore_path)
        restore_dir.mkdir(exist_ok=True)

        # Extract backup
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(path=restore_dir)

        print(f"Backup restored to: {restore_dir}")

    async def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        cutoff_time = datetime.now().timestamp() - (self.retention_days * 24 * 3600)

        for backup_file in self.backup_dir.glob("*.tar.gz"):
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                print(f"Removed old backup: {backup_file}")

    async def backup_to_cloud(self, backup_path: str, bucket_name: str, s3_key: str = None):
        """Upload backup to cloud storage"""
        if not s3_key:
            s3_key = f"backups/{Path(backup_path).name}"

        s3_client = boto3.client('s3')

        try:
            s3_client.upload_file(backup_path, bucket_name, s3_key)
            print(f"Backup uploaded to S3: s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Failed to upload backup to S3: {e}")

    async def list_backups(self) -> List[Dict[str, Any]]:
        """List available backups"""
        backups = []
        for backup_file in self.backup_dir.glob("*.tar.gz"):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'path': str(backup_file)
            })

        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        return backups

# Example usage
async def backup_procedure():
    """Example backup procedure"""
    backup_manager = BackupManager()

    # Create backup
    backup_path = await backup_manager.create_backup()

    # Upload to cloud
    await backup_manager.backup_to_cloud(
        backup_path,
        "physical-ai-backups",
        f"robot-{datetime.now().strftime('%Y%m')}/{Path(backup_path).name}"
    )

    # Cleanup old backups
    await backup_manager.cleanup_old_backups()
```

## Deployment Best Practices

### Configuration Management

```bash
# config_management.sh
#!/bin/bash

# Environment-specific configuration management
ENVIRONMENT=${1:-"development"}  # development, staging, production

case $ENVIRONMENT in
    "production")
        export ROS_DOMAIN_ID=10
        export MAX_LOG_LEVEL="WARN"
        export BACKUP_ENABLED="true"
        export MONITORING_ENABLED="true"
        ;;
    "staging")
        export ROS_DOMAIN_ID=5
        export MAX_LOG_LEVEL="INFO"
        export BACKUP_ENABLED="true"
        export MONITORING_ENABLED="true"
        ;;
    "development")
        export ROS_DOMAIN_ID=0
        export MAX_LOG_LEVEL="DEBUG"
        export BACKUP_ENABLED="false"
        export MONITORING_ENABLED="false"
        ;;
esac

echo "Environment: $ENVIRONMENT"
echo "ROS Domain ID: $ROS_DOMAIN_ID"
echo "Log Level: $MAX_LOG_LEVEL"
```

### Rolling Updates

```yaml
# rolling-update-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: physical-ai-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1      # Only 1 pod can be unavailable during update
      maxSurge: 1           # Only 1 pod can be created above desired count
  selector:
    matchLabels:
      app: physical-ai
  template:
    metadata:
      labels:
        app: physical-ai
    spec:
      containers:
      - name: platform
        image: physical-ai/platform:latest
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 10
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

## Summary

This chapter covered comprehensive deployment strategies for the Physical AI & Humanoid Robotics platform, including robot hardware deployment, containerized solutions, cloud infrastructure, edge computing, monitoring, security, and backup procedures. Proper deployment ensures the platform operates reliably in production environments with appropriate scalability, security, and maintainability.