# Deployment Instructions: Hugging Face Spaces

This document provides instructions for deploying the Physical AI Chatbot Backend to Hugging Face Spaces.

## Prerequisites

- Hugging Face account with Spaces access
- API keys for:
  - Cohere (embeddings)
  - OpenAI (GPT-4)
  - Qdrant Cloud (vector database)

## Required Secrets

Configure these in **Space Settings → Variables and secrets**:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `COHERE_API_KEY` | Cohere API key for embeddings | `co_xxxxxxxxxxxxx` |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | `sk-xxxxxxxxxxxxx` |
| `QDRANT_URL` | Qdrant Cloud cluster URL | `https://xxxxx.qdrant.io` |
| `QDRANT_API_KEY` | Qdrant API key | `xxxxxxxxxxxxx` |

### Setting Secrets

1. Navigate to your Space: `https://huggingface.co/spaces/USERNAME/SPACE_NAME/settings`
2. Scroll to **Variables and secrets** section
3. Click **New secret**
4. Enter **Name** and **Value**
5. Click **Save**
6. Repeat for all required secrets

## Local Testing

Test the Docker build locally before deploying:

```bash
# Generate requirements.txt from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt

# Build Docker image
docker build -t physical-ai-backend .

# Run container (with environment variables)
docker run -p 7860:7860 \
  -e COHERE_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -e QDRANT_URL=your_url \
  -e QDRANT_API_KEY=your_key \
  physical-ai-backend

# Test health endpoint
curl http://localhost:7860/health

# Test chat endpoint
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?"}'
```

## Deployment Steps

### 1. Create Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Enter Space name: `physical-ai-chatbot-backend`
3. Select **Docker** SDK
4. Choose **Public** or **Private** visibility
5. Click **Create Space**

### 2. Push Code to Space

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/USERNAME/physical-ai-chatbot-backend
cd physical-ai-chatbot-backend

# Copy backend files
cp -r /path/to/physical_ai_book/backend/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### 3. Configure Secrets

Follow the steps in **Required Secrets** section above.

### 4. Monitor Build

1. Go to your Space page
2. Click **Open Logs** button
3. Monitor **Build** tab for Docker build progress
4. Monitor **Container** tab for application logs

### 5. Verify Deployment

Once the Space shows **Running** status:

```bash
# Test health endpoint
curl https://USERNAME-physical-ai-chatbot-backend.hf.space/health

# Test chat endpoint from frontend origin
# (Should work without CORS errors)
```

## Troubleshooting

### Space shows "Runtime error"

**Check Container logs:**
1. Click **Open Logs**
2. Check **Container** tab for error messages
3. Common issues:
   - Missing environment variables (see error log for specific variable)
   - API key authentication failures
   - Network connectivity to external services

**Solution:** Verify all secrets are configured correctly in Space Settings.

### CORS errors from frontend

**Symptom:** Browser console shows CORS policy errors

**Solution:** Verify `allow_origins` in api.py includes your Vercel URL:
```python
allow_origins=[
    "https://physical-ai-humanoid-robotics-iota-nine.vercel.app",
    "http://localhost:3000",
]
```

### Health check returns 503

**Symptom:** `/health` endpoint returns "degraded" status

**Solution:** Check which service is failing in the response body, then:
1. Verify the corresponding API key is set correctly
2. Check the service's status page (Cohere, OpenAI, Qdrant)
3. Review Container logs for detailed error messages

### Space goes to sleep

**Symptom:** First request after inactivity takes 30-60 seconds

**Explanation:** Free tier Spaces sleep after 48 hours of inactivity

**Solutions:**
1. **Accept cold starts**: Design frontend to show loading indicator
2. **Periodic pings**: Set up cron job to ping `/health` every 24 hours
3. **Upgrade to paid tier**: Eliminates sleep mode

## Monitoring

### Health Checks

Monitor endpoint availability:

```bash
# Manual check
curl https://USERNAME-physical-ai-chatbot-backend.hf.space/health

# Automated monitoring (using UptimeRobot or similar)
# Configure to ping /health every 5 minutes
```

### Logs

View application logs:

1. Navigate to Space page
2. Click **Open Logs**
3. Select **Container** tab
4. Monitor for errors and performance issues

### Performance

Key metrics to monitor:
- Health check response time (target: < 2s)
- Chat endpoint response time (target: < 5s for errors, variable for responses)
- Startup time after sleep (target: < 60s)

## Known Limitations

### Free Tier Constraints

1. **Sleep Mode**: Spaces sleep after 48 hours of inactivity
   - First request after sleep takes 30-60 seconds (cold start)
   - Solution: Accept cold starts or set up periodic health pings (every 24 hours)

2. **Resource Limits**: Free tier provides cpu-basic hardware
   - CPU: 2 vCPU
   - RAM: 16 GB
   - Disk: 50 GB (ephemeral - cleared on restart)
   - No persistent storage (data lost on sleep/restart)

3. **Cold Start Time**: Initial request after wake-up
   - Application startup: 30-60 seconds
   - External service connection establishment
   - Recommendation: Show loading indicator in frontend

4. **No Custom Domain**: Free tier uses `username-space-name.hf.space` subdomain
   - Custom domains require paid upgrade
   - DNS configuration not available

5. **Build Time**: Docker builds on every code push
   - Build time: 2-5 minutes depending on dependencies
   - No build caching on free tier
   - Failed builds count towards quota

6. **Environment Updates**: Secret changes require manual Space restart
   - No hot-reload for environment variables
   - Plan for brief downtime when updating secrets

### API Rate Limits

External services have their own rate limits:
- **Cohere**: Free tier limits apply (check Cohere dashboard)
- **OpenAI/Groq**: Rate limits per API plan
- **Qdrant Cloud**: Free tier limits (1M vectors, 1GB storage)

### Security Considerations

1. **Public Code**: If Space is public, all code is visible
   - Never hardcode secrets in code
   - Use HF Spaces secrets management exclusively

2. **CORS Configuration**: Currently whitelists specific origins
   - Modify `allow_origins` in api.py to add new frontends
   - Avoid wildcard (`*`) in production

## Updating the Deployment

To deploy updates:

```bash
# Make changes to backend code
git add .
git commit -m "Description of changes"
git push

# Space will automatically rebuild and redeploy
# Monitor in Open Logs → Build tab
```

## Rollback

If deployment fails:

```bash
# Revert to previous commit
git log  # Find last working commit hash
git revert <commit-hash>
git push
```

## Security Considerations

1. **Never commit secrets**: Always use Hugging Face Spaces secrets management
2. **Review logs**: Ensure no secrets appear in stdout/stderr
3. **CORS configuration**: Only allow trusted frontend origins
4. **Rate limiting**: Consider adding rate limiting if abuse occurs

## Support

For issues:
1. Check Container logs first
2. Verify secrets configuration
3. Test locally with Docker
4. Review [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces)
