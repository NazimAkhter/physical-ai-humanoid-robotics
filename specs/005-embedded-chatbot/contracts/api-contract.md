# Chatbot API Contract

**Feature**: 005-embedded-chatbot  
**Date**: 2025-12-22

## Overview

This document defines the expected API contract for the chatbot backend (implementation out of scope for this feature, but interface must be defined for frontend integration).

## Endpoints

### POST /api/chat

Send a user message and receive a bot response.

**Request**:
```json
{
  "message": "string (1-2000 chars)",
  "context": {
    "pageUrl": "string",
    "pageTitle": "string",
    "selectedText": "string | null"
  }
}
```

**Response** (200 OK):
```json
{
  "message": "string",
  "timestamp": "number"
}
```

**Error Response** (4xx/5xx):
```json
{
  "error": "string"
}
```

## Integration Notes

- Frontend will mock this API during development
- Backend team will implement this endpoint separately
- CORS must be configured on backend
- Rate limiting recommended (10 requests/minute per session)
