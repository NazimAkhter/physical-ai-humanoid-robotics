<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution)
- Modified principles: N/A (new constitution)
- Added sections: All principles and sections based on user input
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated / ⚠ pending
  - .specify/templates/spec-template.md ✅ updated / ⚠ pending
  - .specify/templates/tasks-template.md ✅ updated / ⚠ pending
  - .specify/templates/commands/*.md ✅ updated / ⚠ pending
- Follow-up TODOs: RATIFICATION_DATE needs to be set
-->

# Unified Book & RAG Chatbot: Physical AI & Humanoid Robotics Constitution

## Core Principles

### Spec-Driven Development
strictly follow Spec-Kit Plus workflows for content and code generation

### Educational Efficacy
content must bridge theoretical AI concepts with practical robotics application (ROS 2, Isaac, VLA)

### Seamless Integration
tight coupling between the static documentation (Docusaurus) and dynamic AI agents (RAG Chatbot)

### Reproducibility
all code examples (Python/rclpy, URDF, Gazebo) must be syntactically correct and deployable

### Tooling Constraint
Must use Claude Code and Spec-Kit Plus exclusively for generation

### Curriculum Alignment
Content must strictly adhere to the provided 4-module structure (Robotic Nervous System to VLA)

## Key Standards
- Frontend/Book: Docusaurus (latest stable), deployed to GitHub Pages
- Chatbot Backend: FastAPI service using OpenAI Agents/ChatKit SDKs
- Data Persistence: Neon Serverless Postgres for conversation history/metadata
- Vector Search: Qdrant Cloud (Free Tier) for RAG implementation
- Content Structure: 4 Modules (ROS 2, Digital Twin, NVIDIA Isaac, VLA) + Capstone
- Feature Requirement: Chatbot must support context-aware queries based on user-selected text within the book

## Constraints
- Tooling: Must use Claude Code and Spec-Kit Plus exclusively for generation
- Hosting: GitHub Pages for the book artifact
- Database Limits: Optimize for Qdrant Free Tier limits
- Curriculum Alignment: Content must strictly adhere to the provided 4-module structure (Robotic Nervous System to VLA)

## Governance
Success criteria: Book is live on GitHub Pages with all 4 modules and the capstone project documented; RAG Chatbot is embedded in the Docusaurus UI and functional; Chatbot accurately retrieves answers from the book content using Qdrant; 'Select-text-to-ask' functionality works seamlessly in the browser

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): to be determined | **Last Amended**: 2025-12-07
