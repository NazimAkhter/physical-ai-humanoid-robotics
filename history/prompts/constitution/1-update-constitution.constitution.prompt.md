---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Unknown User
command: /sp.constitution Project: Unified Book & RAG Chatbot: Physical AI & Humanoid Robotics
labels: [constitution, spec-kit-plus, physical-ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Project: Unified Book & RAG Chatbot: Physical AI & Humanoid Robotics

Core principles:

Spec-Driven Development: strictly follow Spec-Kit Plus workflows for content and code generation.

Educational Efficacy: content must bridge theoretical AI concepts with practical robotics application (ROS 2, Isaac, VLA).

Seamless Integration: tight coupling between the static documentation (Docusaurus) and dynamic AI agents (RAG Chatbot).

Reproducibility: all code examples (Python/rclpy, URDF, Gazebo) must be syntactically correct and deployable.

Key standards:

Frontend/Book: Docusaurus (latest stable), deployed to GitHub Pages.

Chatbot Backend: FastAPI service using OpenAI Agents/ChatKit SDKs.

Data Persistence: Neon Serverless Postgres for conversation history/metadata.

Vector Search: Qdrant Cloud (Free Tier) for RAG implementation.

Content Structure: 4 Modules (ROS 2, Digital Twin, NVIDIA Isaac, VLA) + Capstone.

Feature Requirement: Chatbot must support context-aware queries based on user-selected text within the book.

Constraints:

Tooling: Must use Claude Code and Spec-Kit Plus exclusively for generation.

Hosting: GitHub Pages for the book artifact.

Database Limits: Optimize for Qdrant Free Tier limits.

Curriculum Alignment: Content must strictly adhere to the provided 4-module structure (Robotic Nervous System to VLA).

Success criteria:

Book is live on GitHub Pages with all 4 modules and the capstone project documented.

RAG Chatbot is embedded in the Docusaurus UI and functional.

Chatbot accurately retrieves answers from the book content using Qdrant.

"Select-text-to-ask" functionality works seamlessly in the browser.
```

## Response snapshot

Updated the project constitution with specific principles and standards for the Unified Book & RAG Chatbot: Physical AI & Humanoid Robotics project. The constitution now includes:

- Core Principles: Spec-Driven Development, Educational Efficacy, Seamless Integration, Reproducibility, Tooling Constraint, Curriculum Alignment
- Key Standards: Docusaurus frontend, FastAPI backend, Neon Postgres, Qdrant vector search
- Constraints: Tooling, hosting, database limits, curriculum alignment
- Governance: Success criteria for the project

## Outcome

- ✅ Impact: Created initial project constitution with specific principles and standards
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific constitution
- 🔁 Next prompts: Plan feature specifications based on this constitution
- 🧠 Reflection: Constitution successfully created with all required project-specific details

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on constitution