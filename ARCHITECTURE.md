# Project Architecture

## Overview

This project follows a **monorepo** structure with clearly separated frontend and backend applications, optimized for independent deployment and development.

## Directory Structure

```
hackathon_01_humanoid_book/
├── frontend/              # Frontend application (deployed to Vercel)
├── backend/               # Backend services (Python-based)
├── specs/                 # Feature specifications (SDD artifacts)
├── plans/                 # Implementation plans
├── tasks/                 # Task breakdowns
├── history/               # Prompt history records (PHRs)
├── contracts/             # API contracts
├── data-models/           # Data models and schemas
└── vercel.json           # Vercel deployment configuration
```

## Frontend Architecture

### Technology Stack
- **Framework**: Docusaurus v3
- **Language**: JavaScript/TypeScript
- **Deployment**: Vercel
- **CDN**: Vercel Edge Network

### Directory Structure
```
frontend/
├── docs/                  # Educational content (Markdown/MDX)
│   └── modules/           # Course modules
├── src/                   # Custom React components
│   ├── components/        # Reusable components
│   ├── css/              # Custom styles
│   └── pages/            # Custom pages
├── static/               # Static assets (images, files)
├── docusaurus.config.js  # Docusaurus configuration
├── sidebars.js           # Navigation structure
└── package.json          # Dependencies
```

### Build Process
1. Install dependencies: `npm install`
2. Development: `npm start` (localhost:3000)
3. Production build: `npm run build`
4. Output: `frontend/build/` directory

### Deployment
- **Platform**: Vercel
- **Trigger**: Automatic on git push
- **Production**: `master` branch → Production URL
- **Preview**: Feature branches → Preview URLs
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/build`

## Backend Architecture

### Technology Stack
- **Language**: Python 3.8+
- **Framework**: FastAPI (or Flask, based on implementation)
- **Services**: ROS 2, Isaac Sim integration
- **Deployment**: TBD (Docker recommended)

### Directory Structure
```
backend/
├── src/                   # Source code
│   ├── main.py           # Application entry point
│   ├── services/         # Business logic services
│   │   ├── ros2/         # ROS 2 integration
│   │   ├── isaac/        # Isaac Sim integration
│   │   └── vla/          # VLA pipeline services
│   ├── api/              # API routes/endpoints
│   ├── models/           # Data models
│   ├── utils/            # Utility functions
│   └── config/           # Configuration files
├── tests/                # Unit and integration tests
├── requirements.txt      # Python dependencies
└── README.md            # Backend-specific documentation
```

### Development Workflow
1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. Install dependencies: `pip install -r requirements.txt`
4. Run development server: `python src/main.py`

### API Design
- RESTful API for frontend communication
- WebSocket support for real-time robotics data
- Integration with ROS 2 topics and services
- Isaac Sim simulation control endpoints

## Specification-Driven Development (SDD) Artifacts

### Specs Directory
Contains feature specifications following the SDD methodology:
```
specs/
├── 001-deploy-gh-pages/
│   └── spec.md
├── 001-ros2-nervous-system/
│   └── spec.md
└── [feature-name]/
    └── spec.md
```

### Plans Directory
Implementation plans derived from specifications:
```
plans/
└── [feature-name]/
    └── plan.md
```

### Tasks Directory
Detailed, testable task breakdowns:
```
tasks/
└── [feature-name]/
    └── tasks.md
```

### History Directory
Prompt History Records (PHRs) for traceability:
```
history/
├── prompts/
│   ├── constitution/      # Constitution-related
│   ├── [feature-name]/    # Feature-specific
│   └── general/           # General prompts
└── adr/                   # Architecture Decision Records
```

## Deployment Strategy

### Frontend Deployment (Vercel)
1. **Automatic Deployment**:
   - Push to `master` → Production deployment
   - Push to any branch → Preview deployment
   - Pull requests → Preview deployment with unique URL

2. **Configuration**:
   - Defined in `vercel.json` at repository root
   - Automatically detects Docusaurus framework
   - Serves static build from `frontend/build/`

3. **Environment Variables**:
   - Configure in Vercel dashboard
   - API endpoints, feature flags, etc.

### Backend Deployment (Future)
- **Recommended**: Docker containerization
- **Options**: AWS, Google Cloud, Azure, or dedicated servers
- **Requirements**:
  - ROS 2 runtime environment
  - NVIDIA GPU support for Isaac Sim
  - Network access to robotics hardware

## Development Principles

### Separation of Concerns
- **Frontend**: Focuses solely on educational content presentation
- **Backend**: Handles robotics logic, simulations, and AI processing
- **Clear API Contracts**: Defined interfaces between frontend and backend

### Independent Development
- Frontend and backend can be developed independently
- Each has its own dependency management
- Separate deployment pipelines

### Version Control
- Single repository (monorepo) for easier coordination
- Clear separation via directory structure
- Shared specifications and documentation

## Build and Test Commands

### Frontend
```bash
cd frontend
npm install          # Install dependencies
npm start           # Development server
npm run build       # Production build
npm run serve       # Serve production build locally
```

### Backend
```bash
cd backend
python -m venv venv                    # Create virtual environment
source venv/bin/activate               # Activate (Windows: venv\Scripts\activate)
pip install -r requirements.txt        # Install dependencies
python src/main.py                     # Run server
pytest                                 # Run tests (if configured)
```

## Configuration Files

### Root Level
- **vercel.json**: Vercel deployment configuration
- **.gitignore**: Git ignore rules for both frontend and backend
- **README.md**: Project overview and quick start
- **ARCHITECTURE.md**: This file

### Frontend
- **docusaurus.config.js**: Docusaurus site configuration
- **sidebars.js**: Documentation navigation
- **package.json**: NPM dependencies and scripts

### Backend
- **requirements.txt**: Python dependencies
- **config.py**: Application configuration (if applicable)
- **.env.example**: Environment variable template

## Future Enhancements

1. **Backend Deployment**:
   - Dockerize backend services
   - Set up CI/CD pipeline
   - Deploy to cloud platform

2. **API Gateway**:
   - Implement API gateway for unified frontend access
   - Add authentication and rate limiting

3. **Monitoring**:
   - Frontend: Vercel Analytics
   - Backend: Application monitoring (Sentry, DataDog)
   - ROS 2: rqt tools and logging

4. **Testing**:
   - Frontend: Jest for component testing
   - Backend: pytest for unit/integration tests
   - E2E: Playwright or Cypress

## Support and Documentation

- **Frontend Issues**: Related to Docusaurus, UI, content
- **Backend Issues**: Related to ROS 2, Isaac Sim, APIs
- **Architecture Questions**: Consult this document and ADRs

For detailed component documentation, see respective README files in `frontend/` and `backend/` directories.
