"""
VLA (Vision-Language-Action) API for the Physical AI & Humanoid Robotics educational platform.
This module handles voice processing, LLM planning, and perception grounding for the VLA Integration module.
"""
from fastapi import APIRouter
from typing import Dict, Any
from .voice import voice_router
from .planning import planning_router
from .perception import perception_router
from .integration import vla_integration_router

vla_router = APIRouter(prefix="/vla", tags=["vla"])

# Include all VLA sub-routers
vla_router.include_router(voice_router)
vla_router.include_router(planning_router)
vla_router.include_router(perception_router)
vla_router.include_router(vla_integration_router)

@vla_router.get("/health")
async def health_check():
    """Health check endpoint for the VLA service"""
    return {"status": "healthy", "service": "vla"}