"""
AscendNet Health Check Routes
"""

from fastapi import APIRouter
from ...utils.logger import get_logger

logger = get_logger("Health")
router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AscendNet API",
        "version": "1.0.0-alpha"
    }

@router.get("/status")
async def system_status():
    """System status endpoint"""
    return {
        "api": "operational",
        "p2p": "operational", 
        "storage": "operational",
        "compute": "operational",
        "payments": "operational"
    }
