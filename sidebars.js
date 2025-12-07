// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  curriculumSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['index'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 Nervous System',
      items: [
        'modules/ros2-nervous-system/index',
        'modules/ros2-nervous-system/architecture-overview',
        'modules/ros2-nervous-system/node-communication',
        'modules/ros2-nervous-system/topic-services-actions',
        'modules/ros2-nervous-system/ros2-with-python-cpp'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin (Gazebo & Unity)',
      items: [
        'modules/gazebo-unity-digital-twin/index',
        'modules/gazebo-unity-digital-twin/gazebo-simulation',
        'modules/gazebo-unity-digital-twin/unity-integration',
        'modules/gazebo-unity-digital-twin/robot-modeling',
        'modules/gazebo-unity-digital-twin/unity-robotics-hub'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 3: Isaac AI Brain',
      items: [
        'modules/isaac-ai-brain/index',
        'modules/isaac-ai-brain/isaac-sim-overview',
        'modules/isaac-ai-brain/ai-robot-training',
        'modules/isaac-ai-brain/computer-vision',
        'modules/isaac-ai-brain/reinforcement-learning'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) Integration',
      items: [
        'modules/vla-integration/index',
        'modules/vla-integration/voice-processing',
        'modules/vla-integration/llm-planning',
        'modules/vla-integration/perception-grounding',
        'modules/vla-integration/complete-integration'
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Project Integration',
      items: [
        'project/introduction',
        'project/setup',
        'project/development',
        'project/deployment'
      ],
      collapsed: false,
    }
  ],
};

export default sidebars;