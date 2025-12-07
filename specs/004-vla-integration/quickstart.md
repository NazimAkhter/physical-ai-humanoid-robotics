# Quickstart Guide: VLA Integration Module

## Overview
This guide provides a quick introduction to setting up and working with the Vision-Language-Action (VLA) Integration module. This module teaches students how to connect voice commands to robot actions using OpenAI Whisper, LLM cognitive planning, and perception grounding.

## Prerequisites
- Computer with internet access and microphone
- OpenAI API key for Whisper and LLM services
- ROS 2 Humble Hawksbill installed
- Python 3.8+ with pip
- Node.js 18+ for documentation
- Docker (for simulation environments)

## Development Environment Setup

### 1. OpenAI API Configuration
```bash
# Set up environment variables for OpenAI API
export OPENAI_API_KEY="your-openai-api-key"
export WHISPER_MODEL_SIZE="large"  # tiny, base, small, medium, large
```

### 2. ROS 2 Environment
```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

# Install required ROS 2 packages
sudo apt update
sudo apt install ros-humble-vision-msgs ros-humble-perception ros-humble-navigation2
```

### 3. Python Dependencies
```bash
# Create virtual environment
python3 -m venv vla_env
source vla_env/bin/activate  # On Windows: vla_env\Scripts\activate

# Install required packages
pip install openai torch torchvision torchaudio ros2-web-bridge
```

### 4. Docusaurus Documentation Setup
```bash
# Navigate to docs directory
cd docs

# Install dependencies
npm install

# Start local development server
npm start
```

### 5. Project Structure
```
physical_ai_book/
├── docs/
│   └── modules/
│       └── 04-vla-integration/
│           ├── index.md
│           ├── chapter-1-voice-to-action-pipeline.md
│           ├── chapter-2-llm-cognitive-planning.md
│           ├── chapter-3-perception-for-vla.md
│           └── chapter-4-capstone-integration.md
├── static/
│   ├── img/
│   ├── audio/
│   └── models/
├── src/
│   └── components/
├── backend/
│   └── src/
│       └── api/
│           ├── vla/
│           └── rag/
└── specs/
    └── 04-vla-integration/
```

## Chapter 1: Voice-to-Action Pipeline

### Processing Voice Commands with Whisper
```python
import openai
import asyncio

async def process_voice_command(audio_file_path):
    """Process a voice command using OpenAI Whisper"""

    # Transcribe audio to text
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    # Extract intent from transcribed text
    intent_extraction_prompt = f"""
    Extract the intent from this voice command: "{transcript['text']}"

    Return in JSON format:
    {{
      "intent": "action_to_perform",
      "entities": {{
        "object": "object_to_act_on",
        "location": "location_if_mentioned",
        "action": "action_type"
      }},
      "confidence": 0.95
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": intent_extraction_prompt}],
        temperature=0.1
    )

    intent_data = response.choices[0].message.content
    return transcript, intent_data

# Example usage
audio_path = "path/to/voice/command.wav"
transcript, intent = asyncio.run(process_voice_command(audio_path))
print(f"Transcription: {transcript['text']}")
print(f"Intent: {intent}")
```

### Voice Command Processing Node
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData
import openai
import json

class VoiceCommandProcessor(Node):
    def __init__(self):
        super().__init__('voice_command_processor')

        # Subscription for audio data
        self.audio_sub = self.create_subscription(
            AudioData,
            'microphone/audio',
            self.audio_callback,
            10
        )

        # Publisher for processed commands
        self.command_pub = self.create_publisher(
            String,
            'vla/processed_command',
            10
        )

        # Store API key securely
        self.openai_api_key = self.declare_parameter(
            'openai_api_key',
            ''
        ).value

        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        else:
            self.get_logger().error("OpenAI API key not provided!")

    def audio_callback(self, msg):
        """Process incoming audio data"""
        try:
            # Convert audio message to file-like object for Whisper
            audio_data = bytes(msg.data)

            # In practice, you'd save this to a temporary file
            # and process it with Whisper API
            # This is a simplified example

            # For now, simulate processing
            simulated_result = {
                "text": "Move the red cube to the left",
                "intent": "move_object",
                "entities": {
                    "object": "red cube",
                    "direction": "left"
                }
            }

            # Publish processed command
            command_msg = String()
            command_msg.data = json.dumps(simulated_result)
            self.command_pub.publish(command_msg)

            self.get_logger().info(f'Processed command: {simulated_result["text"]}')
        except Exception as e:
            self.get_logger().error(f'Error processing audio: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    processor = VoiceCommandProcessor()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        pass
    finally:
        processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Chapter 2: LLM Cognitive Planning

### Generating Action Sequences from Natural Language
```python
import openai
import json

def generate_action_sequence(instruction, context={}):
    """Generate a sequence of ROS 2 actions from natural language instruction"""

    planning_prompt = f"""
    Convert this natural language instruction into a sequence of ROS 2 actions:
    Instruction: "{instruction}"

    Context:
    - Environment: {context.get('environment', 'unknown')}
    - Robot capabilities: {context.get('robot_capabilities', [])}
    - Previous actions: {context.get('previous_actions', [])}

    Return in JSON format:
    {{
      "action_sequence": [
        {{
          "step": 1,
          "action_type": "navigate_to",
          "parameters": {{"x": 1.0, "y": 2.0, "theta": 0.0}},
          "preconditions": ["robot_is_idle"],
          "expected_effects": ["robot_at_destination"],
          "timeout_seconds": 30
        }},
        {{
          "step": 2,
          "action_type": "detect_object",
          "parameters": {{"target_object": "red cube"}},
          "preconditions": ["robot_at_destination"],
          "expected_effects": ["object_detected"],
          "timeout_seconds": 10
        }}
      ],
      "estimated_execution_time": 60,
      "safety_rating": "safe"
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": planning_prompt}],
        temperature=0.2
    )

    result = response.choices[0].message.content
    # Parse the JSON response (in practice, you'd want to handle this more robustly)
    return json.loads(result)

# Example usage
instruction = "Go to the kitchen, find the red mug, and bring it to the table"
context = {
    "environment": "home environment with kitchen, dining room",
    "robot_capabilities": ["navigation", "manipulation", "object_detection"]
}

action_sequence = generate_action_sequence(instruction, context)
print(json.dumps(action_sequence, indent=2))
```

## Chapter 3: Perception for VLA

### Object Detection and Grounding
```python
import cv2
import numpy as np
import torch
from torchvision import transforms

def detect_objects_in_image(image_path, command):
    """Detect objects in image and ground them to command entities"""

    # Load pre-trained object detection model (YOLOv8 or similar)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    # Load and process image
    img = cv2.imread(image_path)
    results = model(img)

    # Parse detection results
    detections = results.pandas().xyxy[0].to_dict()

    # Ground objects to command entities
    command_entities = extract_entities_from_command(command)
    grounded_objects = []

    for idx, detection in enumerate(detections['name']):
        obj_info = {
            'object_id': f"obj_{idx}",
            'class': detection,
            'confidence': detections['confidence'][idx],
            'bbox': {
                'x': int(detections['xmin'][idx]),
                'y': int(detections['ymin'][idx]),
                'width': int(detections['xmax'][idx] - detections['xmin'][idx]),
                'height': int(detections['ymax'][idx] - detections['ymin'][idx])
            },
            'is_target': detection.lower() in command_entities
        }

        if obj_info['is_target']:
            grounded_objects.append(obj_info)

    return {
        'command': command,
        'detected_objects': [obj for obj in detections['name']],
        'grounded_targets': grounded_objects,
        'grounding_confidence': len(grounded_objects) / len(command_entities) if command_entities else 0
    }

def extract_entities_from_command(command):
    """Extract object entities from a command string"""
    # Simple keyword matching - in practice, use NLP techniques
    import re

    # Look for common object descriptors
    object_patterns = [
        r'(red|blue|green|yellow|white|black)\s+(\w+)',  # "red ball"
        r'(\w+)\s+(cube|mug|cup|box|ball)',  # "small cube"
        r'(big|small|large|tiny)\s*(\w+)'  # "big mug"
    ]

    entities = []
    for pattern in object_patterns:
        matches = re.findall(pattern, command.lower())
        for match in matches:
            entities.extend([m for m in match if m])  # Add both descriptor and object

    # Add simple object names
    simple_objects = ['cube', 'mug', 'ball', 'box', 'cup', 'bottle', 'book']
    for obj in simple_objects:
        if obj in command.lower():
            entities.append(obj)

    return list(set(entities))  # Remove duplicates

# Example usage
image_path = "path/to/room/image.jpg"
command = "Pick up the red cube"
result = detect_objects_in_image(image_path, command)
print(json.dumps(result, indent=2))
```

## Chapter 4: Capstone Integration

### Complete VLA Pipeline
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import openai
import json

class VLAPipeline(Node):
    def __init__(self):
        super().__init__('vla_pipeline')

        # Subscriptions for voice and visual input
        self.voice_sub = self.create_subscription(
            String,
            'vla/processed_command',
            self.voice_callback,
            10
        )

        self.image_sub = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            10
        )

        # Publisher for action commands
        self.action_pub = self.create_publisher(
            String,
            'vla/action_sequence',
            10
        )

        # Store pipeline state
        self.pending_voice_command = None
        self.latest_image = None

        # Set up OpenAI API
        self.openai_api_key = self.declare_parameter(
            'openai_api_key',
            ''
        ).value

        if self.openai_api_key:
            openai.api_key = self.openai_api_key

    def voice_callback(self, msg):
        """Handle voice command input"""
        try:
            command_data = json.loads(msg.data)
            self.pending_voice_command = command_data
            self.get_logger().info(f'Received voice command: {command_data["text"]}')

            # If we have a recent image, process the pipeline
            if self.latest_image is not None:
                self.execute_pipeline()
        except json.JSONDecodeError:
            self.get_logger().error("Invalid JSON in voice command message")

    def image_callback(self, msg):
        """Handle image input"""
        self.latest_image = msg
        self.get_logger().info('Received image from camera')

        # If we have a pending voice command, process the pipeline
        if self.pending_voice_command is not None:
            self.execute_pipeline()

    def execute_pipeline(self):
        """Execute the complete VLA pipeline: voice → plan → perception → action"""
        if not self.pending_voice_command or self.latest_image is None:
            return

        try:
            # Step 1: Generate action plan using LLM
            instruction = self.pending_voice_command["text"]
            action_sequence = self.generate_action_plan(instruction)

            # Step 2: Enhance with perception grounding
            grounded_sequence = self.ground_to_perception(
                action_sequence,
                self.pending_voice_command
            )

            # Step 3: Publish action sequence for execution
            action_msg = String()
            action_msg.data = json.dumps({
                "action_sequence": grounded_sequence,
                "source_command": self.pending_voice_command["text"]
            })

            self.action_pub.publish(action_msg)
            self.get_logger().info('Published action sequence for execution')

            # Clear pending command after publishing
            self.pending_voice_command = None

        except Exception as e:
            self.get_logger().error(f'Error in VLA pipeline: {str(e)}')

    def generate_action_plan(self, instruction):
        """Generate high-level action plan from natural language"""
        # This would typically call the LLM planning function
        # Simplified for this example
        return [
            {"action": "navigate", "params": {"target_location": "kitchen"}},
            {"action": "detect", "params": {"target_object": "red cube"}},
            {"action": "grasp", "params": {"object_id": "red_cube_1"}}
        ]

    def ground_to_perception(self, action_sequence, voice_command):
        """Enhance action sequence with perception-based specifics"""
        # This would integrate with perception system
        # Simplified for this example
        enhanced_sequence = []
        for action in action_sequence:
            if action["action"] == "detect":
                # Add specific object detection parameters
                action["params"]["object_name"] = voice_command.get("entities", {}).get("object", "unknown")
            enhanced_sequence.append(action)

        return enhanced_sequence

def main(args=None):
    rclpy.init(args=args)
    pipeline = VLAPipeline()

    try:
        rclpy.spin(pipeline)
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Running Examples

### 1. Build and Run Documentation
```bash
# Navigate to docs directory
cd docs

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### 2. Test VLA API Endpoints
```bash
# Process a voice command
curl -X POST "http://localhost:3000/api/v1/vla/voice/process" \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_file_path": "/path/to/audio.wav",
    "language": "en"
  }'

# Generate action sequence from instruction
curl -X POST "http://localhost:3000/api/v1/vla/planning/generate-actions" \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Go to the kitchen and bring me the red mug",
    "context": {
      "environment": "home environment with kitchen and living room",
      "robot_capabilities": ["navigation", "manipulation"]
    }
  }'
```

### 3. Validate VLA Configuration
```bash
# Check OpenAI API connectivity
python3 -c "import openai; openai.Model.list()"

# Verify ROS 2 nodes
ros2 run vla_integration voice_command_processor --ros-args -p openai_api_key:="YOUR_KEY"
```

## Documentation Commands

### Generate Documentation
```bash
# Build Docusaurus site
cd docs
npm run build

# Serve locally
npm run serve

# Deploy to GitHub Pages
npm run deploy
```

### Validate Content
```bash
# JavaScript/MDX validation
npm test

# Link checker
npx markdown-link-check "**/*.md"

# Build validation
npm run build
```

## Testing

### Run Documentation Tests
```bash
# JavaScript/MDX validation
npm test

# Link checker
npx markdown-link-check "**/*.md"

# Build validation
npm run build
```

## Next Steps
1. Complete all chapters in the VLA Integration module
2. Integrate with the RAG chatbot for interactive learning
3. Deploy documentation to GitHub Pages
4. Test with actual VLA pipeline in simulation