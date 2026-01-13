from fastapi import APIRouter, Depends
from typing import Dict
from .dependencies import verify_identity

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/me")
async def get_current_identity(
    identity: Dict[str, str] = Depends(verify_identity)
):
    return {
        "address": identity["address"],
        "public_key": identity["public_key"],
        "owner": identity["owner"]
    }

@router.get("/verify")
async def verify_identity_endpoint(
    identity: Dict[str, str] = Depends(verify_identity)
):
    return {
        "verified": True,
        "identity": identity
    }

