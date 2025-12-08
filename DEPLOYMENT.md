# Deployment Guide for Physical AI & Humanoid Robotics Platform

## Vercel Deployment

The Physical AI & Humanoid Robotics educational platform is deployed to Vercel. Here's how the deployment process works:

### Initial Setup (One-Time Configuration)

1. **Sign in to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Repository**
   - Click "Add New Project"
   - Select `NazimAkhter/hackathon_01_humanoid_book`
   - Click "Import"

3. **Configure Project Settings** ⚠️ IMPORTANT

   Before deploying, configure these settings:

   **Option A: Set Root Directory (Recommended)**
   - In "Build & Development Settings", set:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build` (auto-detected)
     - **Output Directory**: `build` (auto-detected)
     - **Install Command**: `npm install` (auto-detected)

   **Option B: Use Current Configuration (Already Done)**
   - If you keep Root Directory empty, the `vercel.json` in the repository handles the paths automatically
   - No additional configuration needed

4. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes for the first build

### Automatic Deployment

After initial setup, deployments happen automatically:

1. Push changes to any branch
2. Vercel automatically deploys:
   - **Production**: `master` branch → Production URL
   - **Preview**: Other branches → Unique preview URL
   - **Pull Requests**: Auto-deploy with preview URL in PR
3. Deployment process:
   - Install dependencies
   - Build Docusaurus site
   - Deploy to Vercel Edge Network (CDN)

### Configuration Files

The repository includes Vercel-optimized configuration:

**`vercel.json` (Root Directory)**
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/build",
  "installCommand": "cd frontend && npm install"
}
```

**`frontend/docusaurus.config.js`**
```javascript
{
  url: 'https://hackathon-01-humanoid-book.vercel.app',
  baseUrl: '/',  // Root path for Vercel
  organizationName: 'NazimAkhter',
  projectName: 'hackathon_01_humanoid_book'
}
```

### Monitoring Your Deployment

**Check Deployment Status:**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. View deployment logs and status

**Common Deployment States:**
- 🟢 **Ready** - Successfully deployed
- 🟡 **Building** - Build in progress
- 🔴 **Error** - Build failed (check logs)
- ⏸️ **Canceled** - Deployment canceled

### Environment Variables (Optional)

If your site needs environment variables:

1. Go to **Project Settings** → **Environment Variables**
2. Add variables for different environments:
   - **Production** - Live site only
   - **Preview** - Preview deployments only
   - **Development** - Local development only
3. Common variables for Docusaurus:
   - `DOCUSAURUS_CURRENT_LOCALE`
   - `DOCUSAURUS_SITE_URL`

### Custom Domain Setup (Optional)

To use your own domain:

1. **Add Domain in Vercel:**
   - Go to **Project Settings** → **Domains**
   - Click "Add" and enter your domain
   - Choose Production or Preview assignment

2. **Configure DNS:**
   - Add CNAME record pointing to: `cname.vercel-dns.com`
   - Or add A record pointing to: `76.76.21.21`

3. **Verify:**
   - Wait for DNS propagation (5-60 minutes)
   - Vercel will automatically provision SSL certificate

### Troubleshooting Common Issues

**Build Fails:**
1. Check Vercel deployment logs
2. Verify build works locally:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
3. Ensure all dependencies are in `package.json`
4. Check Node.js version compatibility (Vercel uses 18.x by default)

**404 Errors:**
1. Verify `baseUrl: '/'` in `docusaurus.config.js`
2. Check that `url` matches your Vercel domain
3. Ensure output directory is set to `frontend/build`

**Assets Not Loading:**
1. Verify static files are in `frontend/static/`
2. Check browser console for errors
3. Review cache headers in `vercel.json`

**Deployment is Slow:**
1. Check if dependencies are being cached
2. Review build logs for warnings
3. Consider enabling Vercel's Edge Caching

### Performance Optimization

Vercel automatically provides:
- ✅ **Edge Network** - Global CDN
- ✅ **Automatic Compression** - Gzip/Brotli
- ✅ **Smart Caching** - Static assets cached
- ✅ **Image Optimization** - WebP conversion
- ✅ **SSL/TLS** - HTTPS by default

### Deployment URLs

- **Production**: https://hackathon-01-humanoid-book.vercel.app
- **Preview**: `https://hackathon-01-humanoid-book-[branch]-[username].vercel.app`
- **Development**: http://localhost:3000 (run `npm start` in `frontend/`)