from web3 import Web3
from typing import Optional
from .types import IdentityConfig, RecoveryConfig

SOCIAL_RECOVERY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "identityAddress", "type": "address"},
            {"internalType": "address[]", "name": "guardians", "type": "address[]"},
            {"internalType": "uint256", "name": "threshold", "type": "uint256"}
        ],
        "name": "setRecoveryConfig",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "requestRecovery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "approveRecovery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "getApprovalCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "recoveryConfigs",
        "outputs": [
            {"internalType": "address[]", "name": "guardians", "type": "address[]"},
            {"internalType": "uint256", "name": "threshold", "type": "uint256"},
            {"internalType": "bool", "name": "isActive", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identity", "type": "address"},
            {"indexed": False, "internalType": "address[]", "name": "guardians", "type": "address[]"},
            {"indexed": False, "internalType": "uint256", "name": "threshold", "type": "uint256"}
        ],
        "name": "RecoveryConfigSet",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identity", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "requester", "type": "address"}
        ],
        "name": "RecoveryRequested",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identity", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "guardian", "type": "address"}
        ],
        "name": "RecoveryApproved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identity", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
        ],
        "name": "IdentityRecovered",
        "type": "event"
    }
]

class SocialRecovery:
    def __init__(self, config: IdentityConfig, contract_address: str):
        self.config = config
        self.w3 = Web3(Web3.HTTPProvider(config.rpc_url))
        
        if config.private_key:
            self.account = self.w3.eth.account.from_key(config.private_key)
        else:
            self.account = None

        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=SOCIAL_RECOVERY_ABI
        )

    def set_recovery_config(
        self,
        identity_address: str,
        guardians: list,
        threshold: int
    ) -> None:
        if not self.account:
            raise ValueError("Account required for setting recovery config")

        identity_address = Web3.to_checksum_address(identity_address)
        guardians = [Web3.to_checksum_address(g) for g in guardians]

        tx = self.contract.functions.setRecoveryConfig(
            identity_address, guardians, threshold
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def request_recovery(self, identity_address: str) -> None:
        if not self.account:
            raise ValueError("Account required for requesting recovery")

        identity_address = Web3.to_checksum_address(identity_address)
        tx = self.contract.functions.requestRecovery(identity_address).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def approve_recovery(self, identity_address: str) -> None:
        if not self.account:
            raise ValueError("Account required for approving recovery")

        identity_address = Web3.to_checksum_address(identity_address)
        tx = self.contract.functions.approveRecovery(identity_address).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_approval_count(self, identity_address: str) -> int:
        identity_address = Web3.to_checksum_address(identity_address)
        count = self.contract.functions.getApprovalCount(identity_address).call()
        return count

    def get_recovery_config(self, identity_address: str) -> Optional[RecoveryConfig]:
        try:
            identity_address = Web3.to_checksum_address(identity_address)
            config = self.contract.functions.recoveryConfigs(identity_address).call()
            if not config[2]:
                return None
            return RecoveryConfig(
                guardians=list(config[0]),
                threshold=config[1]
            )
        except (ValueError, AttributeError, Exception):
            return None

