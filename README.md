# Physical AI & Humanoid Robotics Educational Platform

Welcome to the Physical AI & Humanoid Robotics educational platform! This comprehensive curriculum teaches advanced robotics concepts using ROS 2, digital twins, AI brains, and vision-language-action integration.

## 🚀 Live Demo

**Deployment URL**: TBD (will be available after Vercel deployment)

The site will be deployed on Vercel for optimal performance and global CDN distribution.

## 📚 Curriculum Overview

This educational platform covers 4 comprehensive modules:

### Module 1: ROS 2 Nervous System
- ROS 2 architecture and communication patterns
- Node communication, topics, services, and actions
- Python and C++ integration with ROS 2
- Real-world robotics communication patterns

### Module 2: Digital Twin (Gazebo & Unity)
- Gazebo simulation environments
- Unity integration for digital twins
- Robot modeling and simulation techniques
- Digital twin applications in robotics

### Module 3: Isaac AI Brain
- NVIDIA Isaac Sim for AI-powered robotics
- Computer vision and perception systems
- Reinforcement learning for robot training
- AI-driven decision making

### Module 4: Vision-Language-Action (VLA) Integration
- Voice processing with OpenAI Whisper
- LLM-based cognitive planning
- Perception grounding for action execution
- Complete VLA pipeline integration

## 🛠️ Technical Architecture

### Frontend
- **Framework**: Docusaurus v3
- **Deployment**: Vercel with automated CI/CD
- **CDN**: Vercel Edge Network for global distribution
- **Styling**: Custom CSS with educational focus
- **Responsive**: Mobile-first design approach

### Backend Services
- **ROS 2**: Robot Operating System 2 (Humble Hawksbill)
- **Isaac Sim**: NVIDIA Isaac Sim for AI training
- **Gazebo**: Physics simulation environment
- **Unity**: Digital twin visualization

### AI Integration
- **OpenAI APIs**: Whisper for voice processing, GPT for planning
- **Computer Vision**: Perception and object detection
- **Reinforcement Learning**: Robot training and optimization
- **RAG System**: Retrieval-Augmented Generation for Q&A

## 🔧 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ or Windows 10+ (WSL2 recommended)
- **RAM**: 16GB+ (32GB recommended)
- **Storage**: 50GB+ available space
- **GPU**: NVIDIA GPU with CUDA support (for Isaac Sim)

### Software Requirements
- **Node.js**: 18.x or higher
- **Python**: 3.8 or higher
- **ROS 2**: Humble Hawksbill
- **Docker**: For containerized services
- **Git**: For version control

## 📦 Installation

### Quick Start
```bash
# Clone the repository
git clone https://github.com/NazimAkhter/physical_ai_book.git
cd physical_ai_book

# Install dependencies
npm install

# Start the development server
npm start
```

### Backend Services Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start backend services
python src/main.py
```

## 🚀 Development

### Running Locally
```bash
# Start Docusaurus development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve
```

### Adding New Content
1. Create new markdown files in the `docs/` directory
2. Update `sidebars.js` to include new pages in navigation
3. Use Docusaurus MDX components for interactive content
4. Test locally before committing

## 🔄 Deployment

The site is automatically deployed to Vercel:

### Automatic Deployment
1. Push changes to any branch
2. Vercel automatically detects and deploys
   - **Production**: Deployed from `master` branch
   - **Preview**: Unique URL for each branch and pull request
3. Site builds and deploys to Vercel CDN

### Vercel Setup
1. Visit [vercel.com](https://vercel.com) and sign in with GitHub
2. Import repository: `NazimAkhter/hackathon_01_humanoid_book`
3. Vercel auto-detects Docusaurus configuration
4. Click "Deploy"

### Local Testing
```bash
# Build for production
npm run build

# Serve production build locally
npm run serve
```

## 🏗️ Project Structure

```
physical_ai_book/
├── docs/                   # Educational content
│   ├── modules/            # Curriculum modules
│   ├── project/            # Project integration
│   └── reference/          # Reference materials
├── src/                    # Custom Docusaurus components
├── static/                 # Static assets
├── backend/                # Backend services
│   ├── src/                # Backend source code
│   └── requirements.txt    # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── docusaurus.config.js    # Site configuration
├── sidebars.js             # Navigation structure
└── package.json            # Frontend dependencies
```

## 🤝 Contributing

We welcome contributions to improve the educational content and platform:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Content Contribution Guidelines
- Follow the existing module structure
- Include practical examples and exercises
- Use clear, educational language
- Test all code examples
- Add appropriate diagrams and illustrations

## 📈 Learning Outcomes

Students completing this curriculum will be able to:
- Design and implement ROS 2-based robotic systems
- Create and utilize digital twin environments
- Apply AI and machine learning to robotics
- Integrate vision, language, and action systems
- Deploy and operate physical AI systems

## 🎯 Target Audience

- Robotics engineers and researchers
- AI/ML practitioners interested in robotics
- Computer science students
- Hardware engineers transitioning to AI
- Anyone interested in humanoid robotics

## 📞 Support

For questions, issues, or support:
- **Issues**: [GitHub Issues](https://github.com/NazimAkhter/hackathon_01_humanoid_book/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NazimAkhter/hackathon_01_humanoid_book/discussions)
- **Email**: [Contact the maintainers](mailto:nazim.akhter@example.com)

## 📄 License

This educational platform is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- NVIDIA for Isaac Sim and AI technologies
- Open Robotics for ROS 2
- Docusaurus team for the documentation platform
- Vercel for hosting and deployment platform
- GitHub for repository hosting
- The open source robotics community

---

**Ready to start your journey in Physical AI & Humanoid Robotics?** Begin with [Module 1: ROS 2 Nervous System](./docs/modules/ros2-nervous-system/index.md) to learn the fundamentals of robot communication and coordination.

*Made with ❤️ for the robotics education community*