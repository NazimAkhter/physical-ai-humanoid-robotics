# Quickstart: Deploy Docusaurus Site to GitHub Pages

## Overview

This guide provides step-by-step instructions to deploy your Docusaurus-based Physical AI & Humanoid Robotics educational platform to GitHub Pages with automated CI/CD using GitHub Actions.

## Prerequisites

Before starting, ensure you have:

1. A GitHub account with a repository containing your Docusaurus site
2. Admin rights to configure GitHub Actions and GitHub Pages for the repository
3. Node.js 18+ and npm installed locally (for testing)
4. A properly configured Docusaurus site that builds successfully

## Step 1: Verify Your Docusaurus Site

First, ensure your Docusaurus site builds correctly:

```bash
# Clone your repository (if not already done)
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# Install dependencies
npm install

# Test the build locally
npm run build

# Verify the site works locally (optional)
npm start
```

## Step 2: Configure Docusaurus for GitHub Pages

Update your `docusaurus.config.js` file with the correct GitHub Pages settings:

```javascript
// docusaurus.config.js
const config = {
  // ... other configuration options

  // GitHub Pages configuration
  url: 'https://<your-username>.github.io', // Replace <your-username> with your GitHub username
  baseUrl: '/<your-repo-name>/', // Replace <your-repo-name> with your repository name
  organizationName: '<your-username>', // Usually your GitHub org/user name
  projectName: '<your-repo-name>', // Usually your repo name
  deploymentBranch: 'gh-pages', // Branch to deploy to GitHub Pages
  trailingSlash: false, // Set to true if you want trailing slashes

  // ... rest of your configuration
};
```

For the Physical AI & Humanoid Robotics platform, your configuration should look like:

```javascript
// docusaurus.config.js (example)
const config = {
  title: 'Physical AI & Humanoid Robotics Education',
  tagline: 'Learn Robotics, AI, and Humanoid Systems',
  favicon: 'img/favicon.ico',

  // GitHub Pages configuration
  url: 'https://nazimakhter.github.io',
  baseUrl: '/physical_ai_book/',
  organizationName: 'NazimAkhter',
  projectName: 'physical_ai_book',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // ... rest of configuration
};
```

## Step 3: Create GitHub Actions Workflow

Create the GitHub Actions workflow file to automate deployment:

```bash
# Create the workflow directory if it doesn't exist
mkdir -p .github/workflows
```

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main  # Change this to your default branch if different
  pull_request:
    branches:
      - main

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build website
        run: npm run build

      # Popular action to deploy to GitHub Pages:
      # Docs: https://github.com/peaceiris/actions-gh-pages
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Build output to publish to the `gh-pages` branch:
          publish_dir: ./build
          # The following lines assign commit authorship to the official
          # GH-Actions bot for deploys to `gh-pages` branch:
          # https://github.com/actions/checkout/issues/13#issuecomment-724415212
          # The GH actions bot is used by default if you didn't specify the two fields.
          # You can swap them out with your own user credentials.
          user_name: github-actions[bot]
          user_email: 41898282+github-actions[bot]@users.noreply.github.com
```

## Step 4: Enable GitHub Pages in Repository Settings

1. Go to your GitHub repository
2. Click on the "Settings" tab
3. Scroll down to the "Pages" section in the left sidebar
4. Under "Source", select "Deploy from a branch"
5. Choose "gh-pages" as the branch and "/" as the folder
6. Click "Save"

## Step 5: Commit and Push Changes

```bash
# Add all changes
git add .

# Commit with a descriptive message
git commit -m "feat: Configure GitHub Pages deployment with GitHub Actions

- Update docusaurus.config.js for GitHub Pages
- Add GitHub Actions workflow for automated deployment
- Configure deployment settings"

# Push changes to trigger the first deployment
git push origin main
```

## Step 6: Monitor the Deployment

1. Go to the "Actions" tab in your GitHub repository
2. You should see a workflow running titled "Deploy to GitHub Pages"
3. Wait for the workflow to complete successfully
4. Once complete, check the "Pages" section in your repository settings to see the deployment URL

## Step 7: Verify the Deployment

After the workflow completes successfully:

1. Visit `https://<your-username>.github.io/<your-repo-name>/` to see your deployed site
2. Verify that all pages load correctly
3. Test navigation and interactive elements
4. Check that images, CSS, and JavaScript assets load properly

## Troubleshooting Common Issues

### Issue: Site not loading after deployment
**Solution**: Verify your `baseUrl` in `docusaurus.config.js` matches your repository name exactly, including capitalization.

### Issue: CSS/JS assets not loading
**Solution**: Check that your `baseUrl` includes the trailing slash if required, and that all asset references are relative paths.

### Issue: GitHub Actions workflow not triggering
**Solution**: Ensure the workflow file is in the correct location (`.github/workflows/deploy.yml`) and that the branch name matches your default branch.

### Issue: Build failures in GitHub Actions
**Solution**: Check the workflow logs in the Actions tab for specific error messages. Common issues include:
- Missing dependencies in package.json
- Incorrect Node.js version
- Problems with the docusaurus.config.js file

## Custom Domain Setup (Optional)

If you want to use a custom domain:

1. Add a `CNAME` file to your repository's root with your domain name:
   ```
   yourdomain.com
   ```

2. In your DNS provider, create a CNAME record pointing your domain to `<your-username>.github.io`

3. Update the `CNAME` file in your GitHub Pages settings under the "Pages" section.

## Verification Checklist

- [ ] Docusaurus site builds successfully locally (`npm run build`)
- [ ] `docusaurus.config.js` has correct GitHub Pages configuration
- [ ] GitHub Actions workflow file exists at `.github/workflows/deploy.yml`
- [ ] GitHub Pages is enabled in repository settings
- [ ] Workflow runs successfully in Actions tab
- [ ] Site is accessible at the GitHub Pages URL
- [ ] All pages and assets load correctly
- [ ] Navigation works properly
- [ ] Images and styling appear correctly

## Next Steps

1. **Customize your site**: Add your educational content to the Docusaurus site
2. **Set up monitoring**: Consider adding uptime monitoring for your deployed site
3. **Optimize performance**: Implement image optimization and other performance enhancements
4. **Add analytics**: Integrate analytics to track site usage and engagement
5. **Configure HTTPS**: Ensure your site uses HTTPS (automatic with GitHub Pages)

## Additional Resources

- [Docusaurus Deployment Guide](https://docusaurus.io/docs/deployment)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docusaurus GitHub Pages Deployment](https://docusaurus.io/docs/deployment#github-pages)

Your Docusaurus site is now set up for automated deployment to GitHub Pages! Any changes pushed to your main branch will automatically trigger a new build and deployment.