# Hugging Face Spaces Deployment Guide

This guide provides step-by-step instructions for deploying the Physical AI Chatbot Backend to Hugging Face Spaces.

## Prerequisites

✅ **Completed**:
- Backend code is production-ready with Docker configuration
- All endpoints tested locally (/health, /, /chat)
- Error handling and CORS configured
- Environment variable validation implemented

📋 **Required**:
- Hugging Face account (free tier works)
- API keys ready:
  - Cohere API key (for embeddings)
  - OpenAI or Groq API key (for LLM)
  - Qdrant Cloud URL and API key (for vector database)

## Deployment Steps

### Step 1: Create Hugging Face Space (T014)

1. Go to https://huggingface.co/new-space
2. Fill in Space details:
   - **Space name**: `physical-ai-chatbot-backend`
   - **License**: Apache 2.0 (or your choice)
   - **Select SDK**: Choose **Docker** (IMPORTANT!)
   - **Visibility**: Public or Private (your choice)
3. Click **Create Space**
4. You will be redirected to your new Space page

### Step 2: Prepare Backend Code for Push (T015)

The backend directory needs to be pushed to the HF Space repository. You have two options:

#### Option A: Clone Space and Copy Files (Recommended)

```bash
# Clone your new Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/physical-ai-chatbot-backend
cd physical-ai-chatbot-backend

# Copy all backend files (from this project's backend/ directory)
cp -r /path/to/physical_ai_book/backend/* .

# Verify critical files are present
ls -la Dockerfile README.md app.py api.py requirements.txt

# Add all files
git add .

# Commit
git commit -m "feat: initial deployment of Physical AI Chatbot Backend

- FastAPI application with RAG chatbot endpoint
- Docker SDK configuration for HF Spaces
- Health check with service connectivity tests
- Production error handling and logging
- CORS configuration for Vercel frontend

Feature: 010-hf-spaces-deployment"

# Push to HF Space
git push
```

#### Option B: Add HF Space as Remote (Alternative)

```bash
# Navigate to your backend directory
cd /path/to/physical_ai_book/backend

# Add HF Space as a remote
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/physical-ai-chatbot-backend

# Create a new branch for deployment
git checkout -b hf-spaces-deploy

# Push to HF Space
git push huggingface hf-spaces-deploy:main
```

### Step 3: Monitor Build Process (T015 continued)

1. Go to your Space page: `https://huggingface.co/spaces/YOUR_USERNAME/physical-ai-chatbot-backend`
2. Click **Open Logs** button (top right)
3. Watch the **Build** tab:
   - Docker image building (2-5 minutes)
   - Installing dependencies from requirements.txt
   - Expected output: "Successfully built" message
4. If build fails, check error messages and fix issues

**Common Build Issues**:
- Missing Dockerfile → Ensure it's in the repository root
- Invalid requirements.txt → Verify syntax
- Timeout → Build may take up to 10 minutes on free tier

### Step 4: Configure Environment Secrets (T016)

🔒 **CRITICAL**: Configure these secrets BEFORE the application starts successfully.

1. Navigate to Space Settings: `https://huggingface.co/spaces/YOUR_USERNAME/physical-ai-chatbot-backend/settings`
2. Scroll to **Variables and secrets** section
3. Click **New secret** and add each of the following:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `COHERE_API_KEY` | Your Cohere API key | `co_xxxxxxxxxxxxx` |
| `QDRANT_URL` | Your Qdrant Cloud URL | `https://xxxxx.qdrant.io` |
| `QDRANT_API_KEY` | Your Qdrant API key | `xxxxxxxxxxxxx` |
| `OPENAI_API_KEY` | Your OpenAI API key (if using OpenAI) | `sk-xxxxxxxxxxxxx` |
| `GROQ_API_KEY` | Your Groq API key (if using Groq) | `gsk_xxxxxxxxxxxxx` |

**Note**: You need either `OPENAI_API_KEY` OR `GROQ_API_KEY` (not both required, but one is mandatory).

4. After adding all secrets, **restart the Space**:
   - Go to Space page
   - Click **⋮** (three dots menu) → **Restart Space**
   - Wait for rebuild and startup

### Step 5: Verify Deployment (T017)

1. Wait for Space status to show **Running** (green indicator)
2. Your Space URL will be: `https://YOUR_USERNAME-physical-ai-chatbot-backend.hf.space`

Test the health endpoint:
```bash
curl https://YOUR_USERNAME-physical-ai-chatbot-backend.hf.space/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "dependencies": {
    "qdrant": "connected",
    "cohere": "connected",
    "openai": "connected"
  }
}
```

If status is `"degraded"`, check Container logs for errors.

### Step 6: Test Chat Endpoint (T018)

Test the RAG chatbot functionality:

```bash
curl -X POST https://YOUR_USERNAME-physical-ai-chatbot-backend.hf.space/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

**Expected Response**:
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is...",
  "sources": [
    {
      "title": "Chapter 1: ROS 2 Architecture Overview",
      "url": "https://physical-ai-humanoid-robotics-iota-nine.vercel.app/docs/...",
      "score": 0.59
    }
  ]
}
```

### Step 7: Test CORS from Frontend

Open your Vercel frontend in a browser:
- URL: https://physical-ai-humanoid-robotics-iota-nine.vercel.app
- Open browser DevTools (F12) → Console tab
- Try sending a chat message through the chatbot UI
- Verify no CORS errors appear in console
- Verify chatbot responds successfully

## Troubleshooting

### Build Fails

**Check Build logs** in HF Space:
1. Open Logs → Build tab
2. Look for error messages
3. Common issues:
   - Missing dependencies in requirements.txt
   - Syntax errors in Python files
   - Dockerfile configuration errors

**Solution**: Fix the issue locally, commit, and push again.

### Runtime Error / Space Shows "Sleeping"

**Check Container logs**:
1. Open Logs → Container tab
2. Look for startup errors
3. Common issues:
   - Missing environment secrets
   - Invalid API keys
   - Network connectivity to external services

**Solution**: Verify all secrets are configured correctly in Space Settings.

### Health Check Returns "degraded"

**Symptom**: `/health` endpoint returns:
```json
{"status": "degraded", "dependencies": {"qdrant": "unreachable", ...}}
```

**Diagnosis**: Check which service is failing in the response.

**Solutions**:
- If `cohere: unreachable` → Verify COHERE_API_KEY is set correctly
- If `openai: unreachable` → Verify OPENAI_API_KEY or GROQ_API_KEY is set
- If `qdrant: unreachable` → Verify QDRANT_URL and QDRANT_API_KEY are correct

### CORS Errors from Frontend

**Symptom**: Browser console shows:
```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Solution**: Verify CORS configuration in `backend/api.py` includes your Vercel URL:
```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://physical-ai-humanoid-robotics-iota-nine.vercel.app",
]
```

If you need to add a new origin, modify api.py and redeploy.

### Space Goes to Sleep After 48 Hours

**Explanation**: Free tier Spaces sleep after 48 hours of inactivity.

**Solutions**:
1. **Accept cold starts**: First request after sleep takes 30-60 seconds
2. **Periodic health pings**: Set up a cron job to ping `/health` every 24 hours
3. **Upgrade to paid tier**: Eliminates sleep mode

## Post-Deployment Checklist

- [ ] T014: Space created successfully
- [ ] T015: Code pushed, Docker build successful
- [ ] T016: All environment secrets configured
- [ ] T017: Space shows "Running", /health returns 200
- [ ] T018: /chat endpoint responds with RAG results
- [ ] CORS test: Frontend can communicate with backend
- [ ] Monitoring: Consider setting up UptimeRobot for health checks

## Next Steps

After successful deployment:

1. **Update Frontend**: Configure frontend to use your HF Space URL:
   ```javascript
   const BACKEND_URL = "https://YOUR_USERNAME-physical-ai-chatbot-backend.hf.space";
   ```

2. **Set Up Monitoring** (T042-T044):
   - Sign up for UptimeRobot (free tier)
   - Create a monitor for your `/health` endpoint
   - Set check interval to 5 minutes
   - Configure email alerts for downtime

3. **Document URL**: Update main project README with deployed backend URL

4. **Production Testing**: Test end-to-end from Vercel frontend

## Support Resources

- **HF Spaces Documentation**: https://huggingface.co/docs/hub/spaces
- **Docker SDK Guide**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Project Deployment Guide**: See `backend/deployment.md` for detailed troubleshooting

## Summary

**What You Deployed**:
- FastAPI application on port 7860
- Docker container with Python 3.10
- RAG chatbot with Qdrant vector database
- Cohere embeddings + OpenAI/Groq LLM
- Health monitoring with service connectivity tests
- Production-ready error handling and logging

**Your Space URL**: `https://YOUR_USERNAME-physical-ai-chatbot-backend.hf.space`

**API Endpoints**:
- `GET /` - Service information
- `GET /health` - Health check with service status
- `POST /chat` - RAG chatbot endpoint (JSON body: `{"query": "..."}`)
- `GET /docs` - Interactive API documentation (Swagger UI)

---

🎉 **Congratulations!** Your Physical AI Chatbot Backend is now deployed on Hugging Face Spaces!
