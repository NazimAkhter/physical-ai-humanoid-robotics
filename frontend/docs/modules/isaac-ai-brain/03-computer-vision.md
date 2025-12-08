# Chapter 3: Computer Vision for Robotics

## Overview

This chapter explores computer vision techniques specifically applied to robotics within the NVIDIA Isaac ecosystem, including object detection, tracking, SLAM, and visual navigation systems.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Implement computer vision pipelines for robotic perception
2. Use Isaac Sim for synthetic data generation and model training
3. Deploy vision models on robotic platforms
4. Integrate vision systems with robot control and navigation

## Computer Vision Fundamentals for Robotics

### Vision Pipeline Architecture

A typical robotics vision pipeline consists of:

```
Image Acquisition → Preprocessing → Feature Extraction → Object Detection → Decision Making → Action
```

Each stage requires careful consideration of real-time constraints, accuracy requirements, and computational efficiency.

### Key Computer Vision Tasks in Robotics

1. **Object Detection**: Identifying and localizing objects in the environment
2. **Semantic Segmentation**: Pixel-level classification of scene elements
3. **Instance Segmentation**: Distinguishing individual object instances
4. **Pose Estimation**: Determining 6D pose of objects relative to robot
5. **SLAM**: Simultaneous Localization and Mapping
6. **Optical Flow**: Motion estimation between frames
7. **Depth Estimation**: 3D scene understanding

## Isaac Sim for Vision Training

### Synthetic Data Generation

```python
import omni
from omni.isaac.synthetic_utils import SyntheticDataHelper
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import get_prim_at_path
import numpy as np
import cv2
import json
import random

class VisionTrainingDataGenerator:
    def __init__(self, output_dir="vision_dataset"):
        self.output_dir = output_dir
        self.sd_helper = SyntheticDataHelper()
        self.world = World()
        self.scene_objects = []

        # Create output directories
        import os
        os.makedirs(f"{output_dir}/rgb", exist_ok=True)
        os.makedirs(f"{output_dir}/depth", exist_ok=True)
        os.makedirs(f"{output_dir}/seg", exist_ok=True)
        os.makedirs(f"{output_dir}/annotations", exist_ok=True)

    def setup_training_scene(self):
        """Setup a scene for vision training with diverse objects"""
        # Add ground plane
        self.world.scene.add_default_ground_plane()

        # Add diverse objects for training
        object_configs = [
            {"type": "cube", "size": 0.3, "color": [1, 0, 0], "name": "red_cube"},
            {"type": "sphere", "size": 0.2, "color": [0, 1, 0], "name": "green_sphere"},
            {"type": "cylinder", "size": 0.25, "color": [0, 0, 1], "name": "blue_cylinder"},
        ]

        for i, config in enumerate(object_configs):
            # Random position on the ground plane
            position = [
                random.uniform(-3, 3),
                random.uniform(-3, 3),
                config["size"] / 2 + 0.01  # Slightly above ground
            ]

            self.add_object_to_scene(
                obj_type=config["type"],
                position=position,
                size=config["size"],
                color=config["color"],
                name=f"{config['name']}_{i}"
            )

    def add_object_to_scene(self, obj_type, position, size, color, name):
        """Add an object to the Isaac Sim scene"""
        prim_path = f"/World/Objects/{name}"

        if obj_type == "cube":
            from omni.isaac.core.objects import DynamicCuboid
            self.world.scene.add(
                DynamicCuboid(
                    prim_path=prim_path,
                    name=name,
                    position=position,
                    size=size,
                    color=np.array(color)
                )
            )
        elif obj_type == "sphere":
            from omni.isaac.core.objects import DynamicSphere
            self.world.scene.add(
                DynamicSphere(
                    prim_path=prim_path,
                    name=name,
                    position=position,
                    radius=size,
                    color=np.array(color)
                )
            )
        elif obj_type == "cylinder":
            # Add cylinder implementation
            pass

    def randomize_scene_for_training(self):
        """Randomize the scene for diverse training data"""
        # Randomize lighting
        self.randomize_lighting()

        # Randomize object positions and orientations
        self.randomize_object_poses()

        # Randomize camera position and parameters
        self.randomize_camera_parameters()

    def randomize_lighting(self):
        """Randomize lighting conditions"""
        # Get light prim and randomize properties
        light_prim = get_prim_at_path("/World/Light")

        # Randomize intensity, color, position
        intensity = random.uniform(500, 2000)
        color = [random.uniform(0.8, 1.0), random.uniform(0.8, 1.0), random.uniform(0.8, 1.0)]
        position = [
            random.uniform(-5, 5),
            random.uniform(-5, 5),
            random.uniform(3, 8)
        ]

        # Apply changes (implementation depends on light type)

    def randomize_object_poses(self):
        """Randomize object positions and orientations"""
        for obj_name in self.world.scene.object_names:
            if obj_name.startswith("World/Objects/"):
                # Randomize position
                new_pos = [
                    random.uniform(-4, 4),
                    random.uniform(-4, 4),
                    random.uniform(0.1, 2.0)
                ]

                # Randomize orientation
                new_rot = [
                    random.uniform(-0.5, 0.5),
                    random.uniform(-0.5, 0.5),
                    random.uniform(-0.5, 0.5),
                    random.uniform(0.5, 1.0)
                ]

                # Apply new pose to object

    def capture_training_data(self, sample_id):
        """Capture RGB, depth, and segmentation data for training"""
        # Capture RGB image
        rgb_data = self.sd_helper.get_rgb_data("/World/Camera")

        # Capture depth data
        depth_data = self.sd_helper.get_depth_data("/World/Camera")

        # Capture segmentation data
        seg_data = self.sd_helper.get_semantic_segmentation("/World/Camera")

        # Save the captured data
        self.save_training_sample(rgb_data, depth_data, seg_data, sample_id)

        # Generate annotations
        annotations = self.generate_annotations(seg_data, sample_id)

        return annotations

    def save_training_sample(self, rgb_data, depth_data, seg_data, sample_id):
        """Save training data to disk"""
        from PIL import Image

        # Save RGB image
        rgb_image = Image.fromarray(rgb_data, 'RGB')
        rgb_image.save(f"{self.output_dir}/rgb/{sample_id:06d}.png")

        # Save depth data
        depth_normalized = ((depth_data - depth_data.min()) /
                           (depth_data.max() - depth_data.min()) * 255).astype(np.uint8)
        depth_image = Image.fromarray(depth_normalized)
        depth_image.save(f"{self.output_dir}/depth/{sample_id:06d}.png")

        # Save segmentation mask
        seg_image = Image.fromarray(seg_data, 'L')
        seg_image.save(f"{self.output_dir}/seg/{sample_id:06d}.png")

    def generate_annotations(self, seg_data, sample_id):
        """Generate annotations from segmentation data"""
        annotations = {
            "sample_id": sample_id,
            "objects": [],
            "image_size": seg_data.shape
        }

        # Find unique object IDs in segmentation
        unique_ids = np.unique(seg_data)

        for obj_id in unique_ids:
            if obj_id == 0:  # Skip background
                continue

            # Create mask for this object
            mask = (seg_data == obj_id)
            if np.sum(mask) < 50:  # Skip very small objects
                continue

            # Calculate bounding box
            coords = np.where(mask)
            y_min, y_max = coords[0].min(), coords[0].max()
            x_min, x_max = coords[1].min(), coords[1].max()

            # Calculate center and area
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2
            area = np.sum(mask)

            # Get object name (simplified mapping)
            obj_name = f"object_{obj_id}"

            annotations["objects"].append({
                "name": obj_name,
                "id": int(obj_id),
                "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)],
                "center": [float(center_x), float(center_y)],
                "area": int(area),
                "pixel_count": int(np.sum(mask))
            })

        # Save annotations
        import json
        with open(f"{self.output_dir}/annotations/{sample_id:06d}.json", 'w') as f:
            json.dump(annotations, f)

        return annotations

    def generate_training_dataset(self, num_samples=1000):
        """Generate a complete training dataset"""
        print(f"Generating {num_samples} training samples...")

        for i in range(num_samples):
            if i % 100 == 0:
                print(f"Generated {i}/{num_samples} samples")

            # Randomize scene
            self.randomize_scene_for_training()

            # Capture data
            self.capture_training_data(i)

        print(f"Dataset generation complete! Generated {num_samples} samples")
```

## Object Detection for Robotics

### Real-time Object Detection Pipeline

```python
import torch
import torchvision
from torchvision import transforms
import cv2
import numpy as np
from PIL import Image
import time

class RobotVisionPipeline:
    def __init__(self, model_path=None, confidence_threshold=0.5):
        self.confidence_threshold = confidence_threshold
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load pre-trained object detection model
        self.model = self.load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

        # Preprocessing transforms
        self.transform = transforms.Compose([
            transforms.ToTensor(),
        ])

        # COCO class names for 80-class detection
        self.coco_names = [
            '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
            'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
            'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
            'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
            'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
            'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]

    def load_model(self, model_path):
        """Load the object detection model"""
        if model_path:
            # Load custom trained model
            model = torch.load(model_path)
        else:
            # Load pre-trained model
            model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

        return model

    def preprocess_image(self, image):
        """Preprocess image for model inference"""
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image and apply transforms
        pil_image = Image.fromarray(image)
        tensor_image = self.transform(pil_image).unsqueeze(0)

        return tensor_image.to(self.device)

    def detect_objects(self, image):
        """Detect objects in the input image"""
        # Preprocess image
        input_tensor = self.preprocess_image(image)

        # Perform inference
        with torch.no_grad():
            start_time = time.time()
            outputs = self.model(input_tensor)
            inference_time = time.time() - start_time

        # Process outputs
        detections = self.process_outputs(outputs, image.shape)

        return detections, inference_time

    def process_outputs(self, outputs, original_shape):
        """Process model outputs to extract meaningful detections"""
        # Get the first (and typically only) image results
        output = outputs[0]

        # Filter detections by confidence
        scores = output['scores'].cpu().numpy()
        boxes = output['boxes'].cpu().numpy()
        labels = output['labels'].cpu().numpy()

        # Apply confidence threshold
        valid_indices = scores >= self.confidence_threshold
        valid_boxes = boxes[valid_indices]
        valid_labels = labels[valid_indices]
        valid_scores = scores[valid_indices]

        # Create detection results
        detections = []
        for i in range(len(valid_boxes)):
            box = valid_boxes[i]
            label = self.coco_names[valid_labels[i]]
            score = valid_scores[i]

            detection = {
                'bbox': [int(box[0]), int(box[1]), int(box[2]), int(box[3])],  # [x1, y1, x2, y2]
                'label': label,
                'confidence': float(score),
                'center': [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]  # Center coordinates
            }

            detections.append(detection)

        return detections

    def visualize_detections(self, image, detections):
        """Draw bounding boxes and labels on the image"""
        result_image = image.copy()

        for detection in detections:
            bbox = detection['bbox']
            label = detection['label']
            confidence = detection['confidence']

            # Draw bounding box
            cv2.rectangle(result_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

            # Draw label and confidence
            text = f"{label}: {confidence:.2f}"
            cv2.putText(result_image, text, (bbox[0], bbox[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return result_image

    def get_object_position_3d(self, detection, depth_image):
        """Estimate 3D position of detected object using depth information"""
        bbox = detection['bbox']
        center_x, center_y = int(detection['center'][0]), int(detection['center'][1])

        # Get depth value at object center
        depth_value = depth_image[center_y, center_x]

        # Convert 2D image coordinates to 3D world coordinates
        # This requires camera intrinsic parameters
        # Simplified calculation - in practice, use proper camera model
        if depth_value > 0:
            # Convert to world coordinates (simplified)
            # This would use actual camera parameters in real implementation
            world_x = (center_x - depth_image.shape[1] / 2) * depth_value / 1000  # Simplified
            world_y = (center_y - depth_image.shape[0] / 2) * depth_value / 1000  # Simplified
            world_z = depth_value

            return [world_x, world_y, world_z]

        return [0, 0, 0]  # Default if no depth available
```

## Visual SLAM Integration

### ORB-SLAM with Isaac Sim

```python
import numpy as np
import cv2
from collections import deque
import torch

class VisualSLAM:
    def __init__(self, camera_matrix, dist_coeffs=None):
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs if dist_coeffs is not None else np.zeros((4, 1))

        # ORB feature detector
        self.orb = cv2.ORB_create(nfeatures=1000)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Pose estimation
        self.current_pose = np.eye(4)
        self.keyframes = []
        self.keyframe_features = []

        # Tracking
        self.tracking_features = None
        self.frame_count = 0
        self.map_points = []

    def detect_features(self, image):
        """Detect ORB features in the image"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        return keypoints, descriptors

    def match_features(self, desc1, desc2):
        """Match features between two images"""
        if desc1 is None or desc2 is None or len(desc1) == 0 or len(desc2) == 0:
            return []

        matches = self.bf.match(desc1, desc2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches

    def estimate_pose(self, kp1, kp2, matches):
        """Estimate relative pose between two frames"""
        if len(matches) < 10:
            return None, False

        # Get matched points
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Estimate fundamental matrix
        F, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 4, 0.999)

        # Estimate essential matrix
        E = self.camera_matrix.T @ F @ self.camera_matrix

        # Decompose essential matrix
        _, R, t, _ = cv2.recoverPose(E, src_pts, dst_pts, self.camera_matrix)

        # Create transformation matrix
        transformation = np.eye(4)
        transformation[:3, :3] = R
        transformation[:3, 3] = t.ravel()

        return transformation, True

    def process_frame(self, image):
        """Process a single frame for SLAM"""
        keypoints, descriptors = self.detect_features(image)

        if self.tracking_features is not None:
            # Match with previous frame
            matches = self.match_features(self.tracking_features, descriptors)

            if len(matches) > 10:
                # Estimate pose
                transformation, success = self.estimate_pose(
                    self.tracking_features_kp, keypoints, matches
                )

                if success:
                    # Update current pose
                    self.current_pose = self.current_pose @ transformation

                    # Add to keyframes if significant movement
                    if self.should_add_keyframe(transformation):
                        self.add_keyframe(image, keypoints, descriptors)

        # Update tracking features
        self.tracking_features = descriptors
        self.tracking_features_kp = keypoints
        self.frame_count += 1

        return self.current_pose.copy()

    def should_add_keyframe(self, transformation):
        """Determine if a new keyframe should be added"""
        # Check for significant translation or rotation
        translation_norm = np.linalg.norm(transformation[:3, 3])
        rotation_angle = np.arccos(np.clip((np.trace(transformation[:3, :3]) - 1) / 2, -1, 1))

        return translation_norm > 0.1 or rotation_angle > 0.1

    def add_keyframe(self, image, keypoints, descriptors):
        """Add a keyframe to the map"""
        self.keyframes.append({
            'image': image.copy(),
            'pose': self.current_pose.copy(),
            'keypoints': keypoints,
            'descriptors': descriptors
        })

class IsaacSLAMIntegration:
    """Integration of SLAM with Isaac Sim"""

    def __init__(self, slam_system):
        self.slam = slam_system
        self.gt_poses = []  # Ground truth poses from simulation

    def integrate_with_isaac(self, rgb_image, gt_pose=None):
        """Integrate SLAM with Isaac Sim data"""
        # Process image with SLAM
        estimated_pose = self.slam.process_frame(rgb_image)

        # Store ground truth if available
        if gt_pose is not None:
            self.gt_poses.append(gt_pose)

        return estimated_pose

    def evaluate_slam_accuracy(self):
        """Evaluate SLAM accuracy against ground truth"""
        if len(self.gt_poses) < 2:
            return 0.0, 0.0  # Not enough data

        # Calculate trajectory error
        total_translation_error = 0
        total_rotation_error = 0

        for i in range(1, len(self.gt_poses)):
            # Calculate errors
            gt_trans = np.linalg.norm(self.gt_poses[i][:3, 3] - self.gt_poses[i-1][:3, 3])
            est_trans = np.linalg.norm(self.slam.keyframes[i]['pose'][:3, 3] -
                                      self.slam.keyframes[i-1]['pose'][:3, 3])

            total_translation_error += abs(gt_trans - est_trans)
            # Add rotation error calculation

        avg_translation_error = total_translation_error / (len(self.gt_poses) - 1)
        return avg_translation_error, total_rotation_error
```

## Deep Learning Vision Models

### Custom Vision Model for Robotics

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class RobotVisionNet(nn.Module):
    """Custom neural network for robotic vision tasks"""

    def __init__(self, num_classes=10, input_channels=3):
        super(RobotVisionNet, self).__init__()

        # Feature extraction backbone
        self.backbone = nn.Sequential(
            # First conv block
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Second conv block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Third conv block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Fourth conv block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # Adaptive pooling to handle different input sizes
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))

        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes)
        )

        # Object detection head (optional)
        self.detection_head = nn.Sequential(
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, 4)  # Bounding box coordinates
        )

    def forward(self, x):
        # Feature extraction
        features = self.backbone(x)
        features = self.adaptive_pool(features)
        features = torch.flatten(features, 1)

        # Classification
        class_logits = self.classifier(features)

        # Detection (if needed)
        detection_output = self.detection_head(features)

        return {
            'classification': class_logits,
            'detection': detection_output,
            'features': features
        }

class VisionModelTrainer:
    """Trainer for the vision model"""

    def __init__(self, model, device='cuda'):
        self.model = model.to(device)
        self.device = device
        self.optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
        self.criterion = nn.CrossEntropyLoss()

    def train_epoch(self, dataloader):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0

        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(self.device), target.to(self.device)

            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output['classification'], target)
            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()
            pred = output['classification'].max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)

        accuracy = 100. * correct / total
        avg_loss = total_loss / len(dataloader)

        return avg_loss, accuracy

    def validate(self, dataloader):
        """Validate the model"""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in dataloader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = self.criterion(output['classification'], target)

                total_loss += loss.item()
                pred = output['classification'].max(1, keepdim=True)[1]
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)

        accuracy = 100. * correct / total
        avg_loss = total_loss / len(dataloader)

        return avg_loss, accuracy
```

## Vision-Based Navigation

### Visual Navigation Pipeline

```python
import numpy as np
import cv2
from collections import deque

class VisualNavigationSystem:
    """Navigation system using visual input for path planning and obstacle avoidance"""

    def __init__(self, vision_pipeline, map_resolution=0.1, map_size=50):
        self.vision_pipeline = vision_pipeline
        self.map_resolution = map_resolution  # meters per cell
        self.map_size = map_size  # cells per dimension
        self.occupancy_map = np.zeros((map_size, map_size), dtype=np.uint8)

        # Robot state
        self.robot_position = np.array([0, 0])
        self.robot_orientation = 0  # radians

        # Path planning
        self.global_path = []
        self.local_path = []
        self.waypoints = deque()

        # Obstacle detection
        self.obstacle_buffer = deque(maxlen=10)

    def update_map_with_vision(self, image, depth_image=None):
        """Update occupancy map based on visual input"""
        # Detect obstacles in the image
        detections, _ = self.vision_pipeline.detect_objects(image)

        # Convert image detections to world coordinates
        for detection in detections:
            if detection['label'] in ['person', 'car', 'bicycle', 'chair']:  # Obstacle classes
                # Estimate distance using depth or size-based estimation
                distance = self.estimate_distance(detection, depth_image)

                if distance < 2.0:  # Consider as obstacle if closer than 2m
                    # Calculate world coordinates of obstacle
                    world_coords = self.image_to_world_coords(
                        detection['center'], distance
                    )

                    # Update occupancy map
                    self.update_occupancy_map(world_coords)

    def estimate_distance(self, detection, depth_image):
        """Estimate distance to detected object"""
        if depth_image is not None:
            # Use depth image for accurate distance
            center_x, center_y = int(detection['center'][0]), int(detection['center'][1])
            return depth_image[center_y, center_x]
        else:
            # Use size-based estimation (simplified)
            bbox = detection['bbox']
            size_in_pixels = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            # Invert size to get rough distance (larger objects are closer)
            return 10.0 / (size_in_pixels / 1000.0 + 0.1)  # Avoid division by zero

    def image_to_world_coords(self, image_coords, distance):
        """Convert image coordinates to world coordinates"""
        # Convert image coordinates to angles
        img_width, img_height = 640, 480  # Assuming standard resolution
        center_x, center_y = img_width / 2, img_height / 2

        # Calculate angles (simplified pinhole model)
        angle_x = (image_coords[0] - center_x) * 0.001  # Simplified focal length
        angle_y = (image_coords[1] - center_y) * 0.001

        # Calculate world coordinates
        world_x = self.robot_position[0] + distance * np.cos(self.robot_orientation + angle_x)
        world_y = self.robot_position[1] + distance * np.sin(self.robot_orientation + angle_y)

        return np.array([world_x, world_y])

    def update_occupancy_map(self, world_coords):
        """Update occupancy map with obstacle information"""
        # Convert world coordinates to map coordinates
        map_x = int((world_coords[0] - self.occupancy_map.shape[1]/2 * self.map_resolution) / self.map_resolution)
        map_y = int((world_coords[1] - self.occupancy_map.shape[0]/2 * self.map_resolution) / self.map_resolution)

        # Check bounds
        if 0 <= map_x < self.occupancy_map.shape[1] and 0 <= map_y < self.occupancy_map.shape[0]:
            # Mark as occupied with some uncertainty handling
            self.occupancy_map[map_y, map_x] = 255  # Occupied

    def plan_path_to_goal(self, goal_position):
        """Plan path to goal using visual information"""
        # Use A* or other path planning algorithm on the occupancy map
        # This is a simplified version - in practice, use proper path planning

        # For now, just set the goal as a waypoint
        self.waypoints.clear()
        self.waypoints.append(goal_position)

        # In a real implementation, this would:
        # 1. Use A* or RRT on the occupancy map
        # 2. Consider robot kinematics
        # 3. Generate smooth path
        # 4. Update both global and local paths

    def get_navigation_command(self):
        """Get navigation command based on visual input and planned path"""
        if not self.waypoints:
            return np.array([0.0, 0.0])  # Stop if no waypoints

        # Get next waypoint
        next_waypoint = self.waypoints[0]

        # Calculate direction to waypoint
        direction = next_waypoint - self.robot_position
        distance_to_waypoint = np.linalg.norm(direction)

        # Check for obstacles along the path
        if self.has_obstacle_in_path(direction):
            # Implement obstacle avoidance
            avoidance_command = self.avoid_obstacles()
            return avoidance_command

        # Calculate linear and angular velocities
        linear_vel = min(0.5, distance_to_waypoint * 0.5)  # Proportional to distance
        angular_vel = np.arctan2(direction[1], direction[0]) - self.robot_orientation

        # Normalize angular velocity
        while angular_vel > np.pi:
            angular_vel -= 2 * np.pi
        while angular_vel < -np.pi:
            angular_vel += 2 * np.pi

        angular_vel = np.clip(angular_vel, -1.0, 1.0)

        return np.array([linear_vel, angular_vel])

    def has_obstacle_in_path(self, direction):
        """Check if there are obstacles in the path to the target"""
        # Simplified obstacle checking
        # In practice, check the occupancy map along the path
        return False

    def avoid_obstacles(self):
        """Implement obstacle avoidance behavior"""
        # Simple obstacle avoidance - turn away from obstacles
        # In practice, use more sophisticated methods like VFH, DWA, etc.
        return np.array([0.0, 0.5])  # Turn in place

class VisionNavigationController:
    """Controller that integrates vision and navigation"""

    def __init__(self, vision_nav_system):
        self.vision_nav = vision_nav_system
        self.running = False

    def run_navigation(self, camera_feed):
        """Run the navigation loop"""
        self.running = True

        for frame in camera_feed:
            if not self.running:
                break

            # Update map with vision
            self.vision_nav.update_map_with_vision(frame)

            # Get navigation command
            command = self.vision_nav.get_navigation_command()

            # In a real system, this would send commands to the robot
            # self.send_command_to_robot(command)

            # Process the command
            self.execute_navigation_command(command)

    def execute_navigation_command(self, command):
        """Execute the navigation command"""
        linear_vel, angular_vel = command
        print(f"Command: linear={linear_vel:.2f}, angular={angular_vel:.2f}")
```

## Performance Optimization

### Real-time Vision Optimization

```python
import torch
import numpy as np
from torch2trt import torch2trt

class OptimizedVisionSystem:
    """Optimized vision system for real-time robotics applications"""

    def __init__(self, model, use_tensorrt=True):
        self.model = model
        self.use_tensorrt = use_tensorrt
        self.original_model = model

        if use_tensorrt:
            self.optimize_for_tensorrt()

        # Set to evaluation mode
        self.model.eval()

    def optimize_for_tensorrt(self):
        """Optimize model using TensorRT for NVIDIA GPUs"""
        try:
            # Create example input for TensorRT optimization
            example_input = torch.randn(1, 3, 224, 224).cuda()

            # Convert to TensorRT optimized model
            self.model = torch2trt(
                self.original_model,
                [example_input],
                fp16_mode=True,  # Use FP16 for better performance
                max_workspace_size=1<<25  # 32MB workspace
            )
            print("Model optimized with TensorRT")
        except ImportError:
            print("TensorRT not available, using original model")
        except Exception as e:
            print(f"TensorRT optimization failed: {e}")

    def preprocess_for_inference(self, image, target_size=(224, 224)):
        """Optimized preprocessing for inference"""
        # Resize image
        image = cv2.resize(image, target_size)

        # Convert to tensor
        image = torch.from_numpy(image).permute(2, 0, 1).float()
        image = image.unsqueeze(0)  # Add batch dimension

        # Normalize (if needed)
        image = image / 255.0

        return image.cuda() if torch.cuda.is_available() else image

def optimize_inference_pipeline():
    """Optimize the entire inference pipeline"""

    # Use mixed precision
    torch.backends.cudnn.benchmark = True

    # Enable TensorRT optimizations
    # Use batch processing when possible
    # Optimize memory allocation

    pass
```

## Best Practices

1. **Real-time Constraints**: Optimize models for the required frame rate
2. **Robustness**: Handle varying lighting and environmental conditions
3. **Calibration**: Properly calibrate cameras and sensors
4. **Validation**: Test on diverse real-world scenarios
5. **Safety**: Implement fallback behaviors when vision fails

## Summary

Computer vision is crucial for robotic perception and navigation. The integration of Isaac Sim with vision systems enables the creation of robust perception pipelines through synthetic data generation and simulation-based training. The next chapter will cover reinforcement learning for robotics.