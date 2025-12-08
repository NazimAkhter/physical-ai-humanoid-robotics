# Deployment Guide for Physical AI & Humanoid Robotics Platform

## Vercel Deployment

The Physical AI & Humanoid Robotics educational platform is deployed to Vercel. Here's how the deployment process works:

### Automatic Deployment (Recommended)

The site is automatically deployed when changes are pushed to the repository:

1. Push your changes to any branch
2. Vercel will automatically detect and deploy:
   - Production deployments for `master` branch
   - Preview deployments for all other branches and pull requests
3. The deployment will:
   - Install dependencies with `npm install`
   - Build the Docusaurus site with `npm run build`
   - Deploy the built site to Vercel CDN

### Vercel Setup

To set up Vercel deployment:

1. Visit [vercel.com](https://vercel.com) and sign in with GitHub
2. Import your repository: `NazimAkhter/hackathon_01_humanoid_book`
3. Vercel will auto-detect Docusaurus configuration
4. Click "Deploy" to complete the setup

### Configuration

The site is configured for Vercel deployment:
- `vercel.json` contains build and deployment settings
- Build command: `npm run build`
- Output directory: `build`
- Framework preset: Docusaurus (auto-detected)

### Environment Variables

If your site requires environment variables:
1. Go to your project settings in Vercel dashboard
2. Navigate to "Environment Variables" section
3. Add any required variables (API keys, etc.)

### Custom Domain (Optional)

To use a custom domain:
1. Go to your project settings in Vercel dashboard
2. Navigate to "Domains" section
3. Add your custom domain and follow DNS configuration instructions

### Troubleshooting

If the deployment fails:
1. Check the Vercel deployment logs for error details
2. Verify that the build process completes successfully locally (`npm run build`)
3. Ensure all dependencies are listed in `package.json`
4. Check for any environment-specific issues in build logs

### Deployment URLs

- **Production**: Deployed from `master` branch
- **Preview**: Unique URL for each branch and pull request
- **Development**: Run locally with `npm start`