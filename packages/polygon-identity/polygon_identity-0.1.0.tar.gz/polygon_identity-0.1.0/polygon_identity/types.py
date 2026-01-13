from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class IdentityConfig:
    """Configuration for identity management.
    
    Args:
        rpc_url: Polygon RPC endpoint URL
        contract_address: Deployed IdentityManager contract address
        private_key: Optional private key for signing transactions
        wallet_provider: Optional Web3 provider instance
    """
    rpc_url: str
    contract_address: str
    private_key: Optional[str] = None
    wallet_provider: Optional[Any] = None

@dataclass
class IdentityKeys:
    """Cryptographic key pair for identity.
    
    Args:
        private_key: Private key (keep secure!)
        public_key: Public key
        address: Ethereum address derived from keys
    """
    private_key: str
    public_key: str
    address: str

@dataclass
class IdentityData:
    """Identity information from blockchain.
    
    Args:
        owner: Address that owns this identity
        public_key: Public key hash
        created_at: Unix timestamp of creation
        is_active: Whether identity is currently active
    """
    owner: str
    public_key: str
    created_at: int
    is_active: bool

@dataclass
class RecoveryConfig:
    """Social recovery configuration.
    
    Args:
        guardians: List of guardian addresses
        threshold: Number of approvals needed for recovery
    """
    guardians: List[str]
    threshold: int

