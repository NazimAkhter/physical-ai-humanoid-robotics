# Chapter 2: LLM Cognitive Planning

## Overview

In this chapter, we'll explore how Large Language Models (LLMs) can be used for cognitive planning in robotics. We'll learn how to convert natural language instructions into executable action sequences that robots can understand and execute safely.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Design prompts for LLM-based robotic planning
2. Convert natural language instructions into action sequences
3. Define preconditions and expected effects for robot actions
4. Implement safety checks and validation for generated plans
5. Integrate planning with perception and execution systems

## Prerequisites

- Completion of Chapter 1 (Voice Processing with OpenAI Whisper)
- Understanding of ROS 2 action architecture
- Basic knowledge of AI planning concepts
- Familiarity with OpenAI GPT models

## Introduction to Cognitive Planning

Cognitive planning in robotics involves translating high-level goals expressed in natural language into sequences of low-level actions that achieve those goals. This requires:
- Understanding the semantics of the instruction
- Reasoning about the current state of the world
- Planning a sequence of actions to achieve the desired outcome
- Ensuring safety and feasibility of the plan

## LLM-Based Planning Architecture

The LLM-based planning system uses the following architecture:

1. **Input Processing**: Natural language instruction with context
2. **World Modeling**: Current state of the environment and robot
3. **Plan Generation**: LLM generates action sequence
4. **Validation**: Safety and feasibility checks
5. **Output**: Structured action sequence ready for execution

## Prompt Engineering for Robotic Planning

Effective prompt engineering is crucial for generating high-quality plans. A well-structured prompt should include:

- **Role specification**: Define the LLM as a robotic planning expert
- **Context**: Current state of the robot and environment
- **Instruction**: The natural language command to be executed
- **Action vocabulary**: Available actions the robot can perform
- **Constraints**: Safety requirements and limitations
- **Output format**: Structured JSON response

### Example Prompt Template

```python
def create_planning_prompt(instruction, context, available_actions):
    prompt = f"""
    You are an expert robotic planning system. Convert the following natural language instruction into a sequence of robot actions.

    AVAILABLE ACTIONS:
    {available_actions}

    CURRENT CONTEXT:
    {context}

    INSTRUCTION:
    {instruction}

    Generate a step-by-step action sequence that achieves the goal safely. Each action should have:
    - step number
    - action type
    - parameters
    - preconditions
    - expected effects
    - timeout

    Return the result as a JSON array of action objects.
    """
    return prompt
```

## Action Representation

Robot actions in the VLA system are represented with the following structure:

```json
{
  "step": 1,
  "action_type": "navigate_to",
  "parameters": {"x": 1.0, "y": 2.0, "theta": 0.0},
  "preconditions": ["robot_is_idle"],
  "expected_effects": ["robot_at_destination"],
  "timeout_seconds": 30
}
```

### Common Action Types

1. **Navigation Actions**:
   - `navigate_to`: Move robot to specific coordinates
   - `follow_path`: Follow a predefined path

2. **Manipulation Actions**:
   - `pick_object`: Pick up an object
   - `place_object`: Place an object at a location
   - `grasp`: Grasp an object with specific force

3. **Perception Actions**:
   - `detect_object`: Detect objects in the environment
   - `localize_object`: Get precise location of an object
   - `scan_environment`: Create a map of the environment

4. **Utility Actions**:
   - `wait`: Wait for a specified time
   - `check_condition`: Verify a condition is met
   - `execute_trajectory`: Execute a predefined movement

## Safety and Validation

Safety is paramount in robotic planning. The LLM planning system includes several validation layers:

### Pre-execution Validation
- **Feasibility Check**: Verify the plan is physically possible
- **Safety Constraints**: Ensure no dangerous conditions are created
- **Resource Availability**: Check that required resources are available

### Example Safety Validation

```python
def validate_plan(action_sequence):
    violations = []

    for action in action_sequence:
        # Check for navigation safety
        if action["action_type"] == "navigate_to":
            if not is_safe_path(action["parameters"]):
                violations.append(f"Unsafe path to {action['parameters']}")

        # Check for manipulation safety
        if action["action_type"] in ["pick_object", "place_object"]:
            if not is_safe_manipulation(action["parameters"]):
                violations.append(f"Unsafe manipulation: {action['parameters']}")

    return len(violations) == 0, violations
```

## Integration with Other VLA Components

The LLM planning module integrates with other components of the VLA system:

### Integration with Voice Processing
- Receives processed voice commands with intent and entities
- Uses extracted information to generate appropriate plans

### Integration with Perception
- Incorporates current scene understanding
- Updates plans based on real-time perception data
- Handles plan adjustments when expected objects are not found

### Integration with Execution
- Provides structured action sequences to execution system
- Monitors execution and generates recovery plans if needed

## Practical Exercise: Implementing LLM Planning

Let's implement a complete LLM planning function:

```python
from openai import OpenAI
import json

def generate_action_sequence(instruction, context=None, options=None):
    """
    Generate action sequence from natural language instruction using LLM
    """
    client = OpenAI()

    # Default context if none provided
    if context is None:
        context = {
            "robot_state": "idle",
            "current_objects": [],
            "environment_map": {},
            "robot_capabilities": ["navigate", "detect", "manipulate"]
        }

    # Default options if none provided
    if options is None:
        options = {
            "max_steps": 10,
            "safety_level": "high",
            "preferred_actions": []
        }

    # Define available actions
    available_actions = [
        {
            "name": "navigate_to",
            "description": "Navigate robot to specified coordinates",
            "parameters": ["x", "y", "theta"],
            "preconditions": ["robot_is_idle"],
            "effects": ["robot_at_destination"]
        },
        {
            "name": "detect_object",
            "description": "Detect objects in the environment",
            "parameters": ["target_object"],
            "preconditions": ["robot_has_perception"],
            "effects": ["object_detected"]
        },
        {
            "name": "pick_object",
            "description": "Pick up an object",
            "parameters": ["object_id"],
            "preconditions": ["robot_at_object_location", "object_available"],
            "effects": ["object_grasped"]
        },
        {
            "name": "place_object",
            "description": "Place an object at specified location",
            "parameters": ["object_id", "location"],
            "preconditions": ["object_grasped"],
            "effects": ["object_placed"]
        }
    ]

    # Create the planning prompt
    prompt = f"""
    You are an expert robotic planning system. Convert the following natural language instruction into a sequence of robot actions.

    AVAILABLE ACTIONS:
    {json.dumps(available_actions, indent=2)}

    CURRENT CONTEXT:
    {json.dumps(context, indent=2)}

    INSTRUCTION:
    {instruction}

    OPTIONS:
    {json.dumps(options, indent=2)}

    Generate a step-by-step action sequence that achieves the goal safely. Each action should have:
    - step number
    - action_type
    - parameters
    - preconditions
    - expected_effects
    - timeout_seconds

    Ensure the plan is feasible, safe, and efficient. Return the result as a JSON array of action objects.
    """

    # Generate the plan using OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    # Extract and parse the response
    response_text = response.choices[0].message.content

    # Extract JSON from response (in case there's additional text)
    import re
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        action_sequence = json.loads(json_str)
    else:
        # If no JSON found, try to parse the entire response
        action_sequence = json.loads(response_text)

    # Add metadata to the plan
    plan_result = {
        "plan_id": f"plan_{hash(instruction) % 10000}",
        "instruction": instruction,
        "action_sequence": action_sequence,
        "confidence_score": 0.85,  # Placeholder - would come from actual confidence assessment
        "estimated_execution_time": sum([action.get("timeout_seconds", 10) for action in action_sequence]),
        "safety_rating": "high",
        "generated_by": "gpt-4-turbo",
        "processing_time_ms": 500,  # Placeholder
        "timestamp": "2025-12-07T10:00:00Z"
    }

    return plan_result
```

## Plan Execution Monitoring

Once a plan is generated, it needs to be monitored during execution to handle unexpected situations:

```python
def monitor_plan_execution(plan, execution_callback):
    """
    Monitor plan execution and handle deviations
    """
    for i, action in enumerate(plan["action_sequence"]):
        try:
            # Execute the action
            result = execution_callback(action)

            # Check if action succeeded
            if not result["success"]:
                # Handle failure - could involve replanning or recovery
                recovery_plan = generate_recovery_plan(action, result["error"])
                return execute_recovery_plan(recovery_plan)

        except Exception as e:
            # Handle execution errors
            print(f"Error executing action {i}: {str(e)}")
            return handle_execution_error(action, e)

    return {"status": "completed", "plan_id": plan["plan_id"]}
```

## Best Practices

1. **Prompt Consistency**: Use consistent prompt structures for reliable results
2. **Validation**: Always validate generated plans before execution
3. **Safety First**: Prioritize safety over efficiency in plan generation
4. **Context Awareness**: Include relevant context to improve plan quality
5. **Error Handling**: Implement robust error handling and recovery mechanisms

## Summary

LLM cognitive planning bridges the gap between natural language instructions and executable robot actions. By carefully engineering prompts and implementing validation mechanisms, we can create robust planning systems that enable natural human-robot interaction.

## Next Steps

In the next chapter, we'll explore perception grounding systems that connect language to visual entities in the environment.