from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
import jwt
from polygon_identity import PolygonIdentity
from polygon_identity.types import IdentityConfig

security = HTTPBearer()

async def get_identity(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_secret: str = None,
    identity_manager: Optional[PolygonIdentity] = None
) -> Dict[str, str]:
    if not jwt_secret or not identity_manager:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Identity manager not configured"
        )

    try:
        token = credentials.credentials
        decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        identity_address = decoded.get('identityAddress')

        identity_data = identity_manager.get_identity(identity_address)
        
        if not identity_data.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identity is not active"
            )

        verified = identity_manager.verify_identity(identity_address)
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identity verification failed"
            )

        return {
            'address': identity_address,
            'public_key': identity_data.public_key,
            'owner': identity_data.owner
        }

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

async def verify_identity(
    identity: Dict[str, str] = Depends(get_identity)
) -> Dict[str, str]:
    return identity

