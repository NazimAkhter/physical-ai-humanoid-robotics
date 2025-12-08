# Chapter 1: Voice Processing with OpenAI Whisper

## Overview

In this chapter, we'll explore how to process voice commands using OpenAI Whisper, converting natural language into structured intent for robotics applications. Voice processing is a critical component of the VLA (Vision-Language-Action) pipeline, enabling natural human-robot interaction.

## Learning Objectives

By the end of this chapter, you will be able to:
1. Set up and configure OpenAI Whisper for voice processing
2. Process audio input and convert speech to text
3. Extract intent and entities from transcribed text
4. Integrate voice processing into the broader VLA pipeline

## Prerequisites

- Completion of Module 1 (ROS 2 Nervous System)
- Basic understanding of audio processing concepts
- OpenAI API access with Whisper capabilities
- Python programming experience

## Introduction to Voice Processing in Robotics

Voice processing enables robots to understand and respond to natural language commands. In the context of robotics, this involves:
- Converting speech to text (Automatic Speech Recognition)
- Understanding the intent behind the command
- Extracting relevant entities (objects, locations, actions)
- Converting these elements into actionable robot commands

## OpenAI Whisper API Integration

OpenAI Whisper is a state-of-the-art speech recognition model that excels at converting speech to text with high accuracy across multiple languages and domains.

### API Setup

First, ensure you have your OpenAI API key configured:

```python
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### Audio File Processing

Whisper processes audio files in various formats (MP3, MP4, M4A, WAV, etc.). For robotics applications, you'll typically process short voice commands:

```python
def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text
```

## Intent Extraction and Entity Recognition

After transcribing speech to text, the next step is to extract the intent and relevant entities from the text. This involves identifying:
- The main action requested (e.g., "pick up", "move to", "detect")
- Objects to act upon (e.g., "red cube", "blue cylinder")
- Target locations (e.g., "table", "shelf", "box")
- Other relevant parameters (e.g., quantities, colors, sizes)

### Example Implementation

Here's how you might implement intent extraction using OpenAI's language models:

```python
def extract_intent_and_entities(transcription):
    prompt = f"""
    Extract the intent and entities from the following voice command:
    "{transcription}"

    Provide the result in the following JSON format:
    {{
        "intent": "the main action requested",
        "entities": {{
            "action": "specific action verb",
            "object": "object to act upon",
            "location": "target location",
            "color": "color of object if specified",
            "quantity": "number if specified"
        }}
    }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    import json
    return json.loads(response.choices[0].message.content)
```

## Voice Processing Pipeline

The complete voice processing pipeline for robotics involves several steps:

1. **Audio Capture**: Recording voice commands from users
2. **Transcription**: Converting speech to text using Whisper
3. **Intent Extraction**: Understanding the purpose of the command
4. **Entity Recognition**: Identifying objects, locations, and parameters
5. **Validation**: Ensuring the command is safe and executable
6. **Integration**: Passing processed information to the planning module

## Practical Exercise: Voice Command Processing

Let's implement a complete voice processing function that integrates all the components:

```python
import asyncio
import tempfile
import os
from openai import OpenAI

async def process_voice_command(audio_file):
    """
    Complete voice processing pipeline
    """
    client = OpenAI()

    # Create temporary file to save uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
        temp_file.write(await audio_file.read())
        temp_path = temp_file.name

    try:
        # Step 1: Transcribe audio using Whisper
        with open(temp_path, "rb") as audio_file:
            transcription_result = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcription = transcription_result.text

        # Step 2: Extract intent and entities
        extraction_prompt = f"""
        Extract intent and entities from this voice command:
        "{transcription}"

        Return in JSON format with intent and entities (action, object, location, color, quantity).
        """

        extraction_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": extraction_prompt}],
            temperature=0.1
        )

        import json
        extracted_data = json.loads(extraction_response.choices[0].message.content)

        # Step 3: Return structured result
        result = {
            "transcription": transcription,
            "intent": extracted_data.get("intent"),
            "entities": extracted_data.get("entities", {}),
            "confidence": 0.9  # Placeholder - would come from actual confidence scores
        }

        return result

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
```

## Integration with VLA Pipeline

The voice processing module integrates with the broader VLA pipeline by passing processed commands to the planning module. The output includes:
- Transcribed text
- Extracted intent
- Recognized entities
- Confidence scores
- Additional metadata

This information is then used by the LLM planning module to generate appropriate action sequences for the robot.

## Best Practices

1. **Audio Quality**: Ensure clear audio input for best transcription results
2. **Command Structure**: Use consistent command structures to improve recognition accuracy
3. **Error Handling**: Implement robust error handling for API failures
4. **Privacy**: Handle voice data according to privacy regulations
5. **Validation**: Validate commands for safety before execution

## Summary

Voice processing with OpenAI Whisper enables natural human-robot interaction by converting speech commands into structured data that can be used by the VLA pipeline. The combination of high-quality transcription and intelligent intent extraction makes it possible for users to interact with robots using natural language.

## Next Steps

In the next chapter, we'll explore how to use Large Language Models for cognitive planning, converting natural language commands into sequences of robot actions.