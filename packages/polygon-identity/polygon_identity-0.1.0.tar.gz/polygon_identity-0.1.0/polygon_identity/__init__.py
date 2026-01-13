from .identity import PolygonIdentity
from .zk_identity import ZKIdentity, ZKProof
from .social_recovery import SocialRecovery
from .types import IdentityConfig, IdentityKeys, IdentityData, RecoveryConfig

__version__ = "0.1.0"
__all__ = [
    "PolygonIdentity",
    "ZKIdentity",
    "ZKProof",
    "SocialRecovery",
    "IdentityConfig",
    "IdentityKeys",
    "IdentityData",
    "RecoveryConfig"
]

