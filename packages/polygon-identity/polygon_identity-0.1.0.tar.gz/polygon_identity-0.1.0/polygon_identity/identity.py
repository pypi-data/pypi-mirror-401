from web3 import Web3
import web3
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from typing import Optional
from .types import IdentityConfig, IdentityKeys, IdentityData

IDENTITY_MANAGER_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "publicKey", "type": "bytes32"}],
        "name": "createIdentity",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "identityAddress", "type": "address"},
            {"internalType": "bytes32", "name": "newPublicKey", "type": "bytes32"}
        ],
        "name": "updatePublicKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "deactivateIdentity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "recoverIdentity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "getIdentity",
        "outputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "bytes32", "name": "publicKey", "type": "bytes32"},
            {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
            {"internalType": "bool", "name": "isActive", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "verifyIdentity",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identityAddress", "type": "address"},
            {"indexed": False, "internalType": "bytes32", "name": "publicKey", "type": "bytes32"},
            {"indexed": True, "internalType": "address", "name": "owner", "type": "address"}
        ],
        "name": "IdentityCreated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identityAddress", "type": "address"},
            {"indexed": False, "internalType": "bytes32", "name": "newPublicKey", "type": "bytes32"}
        ],
        "name": "IdentityUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [{"indexed": True, "internalType": "address", "name": "identityAddress", "type": "address"}],
        "name": "IdentityDeactivated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "identityAddress", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
        ],
        "name": "IdentityRecovered",
        "type": "event"
    }
]

class PolygonIdentity:
    def __init__(self, config: IdentityConfig):
        self.config = config
        self.w3 = Web3(Web3.HTTPProvider(config.rpc_url))
        
        if config.private_key:
            self.account = self.w3.eth.account.from_key(config.private_key)
        else:
            self.account = None

        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(config.contract_address),
            abi=IDENTITY_MANAGER_ABI
        )

    def generate_key_pair(self) -> IdentityKeys:
        account = self.w3.eth.account.create()
        
        private_key = account.key.hex()
        public_key = account.address
        
        return IdentityKeys(
            private_key=private_key,
            public_key=public_key,
            address=account.address
        )

    def create_identity(self, public_key: Optional[str] = None) -> str:
        if not self.account:
            raise ValueError("Account required for creating identity")

        if public_key:
            if public_key.startswith('0x'):
                public_key_bytes = bytes.fromhex(public_key[2:])
            else:
                public_key_bytes = bytes.fromhex(public_key)
        else:
            keys = self.generate_key_pair()
            public_key_bytes = bytes.fromhex(keys.address[2:])

        public_key_hash = Web3.keccak(public_key_bytes)

        tx = self.contract.functions.createIdentity(public_key_hash).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # Check if transaction succeeded
        if receipt.get('status') != 1:
            raise ValueError(f"Transaction failed with status {receipt.get('status')}")

        # Extract identity address from event logs
        # The IdentityCreated event has identityAddress as the first indexed parameter (topics[1])
        for log in receipt.get('logs', []):
            # Check if this log is from our contract
            if log.get('address', '').lower() == self.config.contract_address.lower():
                topics = log.get('topics', [])
                # IdentityCreated event should have: topic[0] = event signature, topic[1] = identityAddress, topic[2] = owner
                if len(topics) >= 2:
                    # Extract identityAddress from topic[1] (first indexed parameter)
                    identity_address = '0x' + topics[1].hex()[-40:]  # Last 40 hex chars (20 bytes = address)
                    # Verify this is a valid address by checking if we can get identity data
                    try:
                        test_identity = self.get_identity(identity_address)
                        if test_identity.is_active:
                            return identity_address
                    except (ValueError, AttributeError, Exception):
                        pass

        # Fallback: Try web3.py's event processing
        try:
            events = self.contract.events.IdentityCreated().process_receipt(receipt)
            if events and len(events) > 0:
                event = events[0]
                if hasattr(event, 'args') and hasattr(event.args, 'identityAddress'):
                    return event.args.identityAddress
        except Exception:
            pass

        # If all methods fail
        raise ValueError(
            f"Could not extract identity address from transaction. "
            f"Transaction hash: {tx_hash.hex()}. "
            f"Check: https://amoy.polygonscan.com/tx/{tx_hash.hex()}"
        )

    def get_identity(self, identity_address: str) -> IdentityData:
        identity_address = Web3.to_checksum_address(identity_address)
        result = self.contract.functions.getIdentity(identity_address).call()
        
        return IdentityData(
            owner=result[0],
            public_key=result[1].hex(),
            created_at=result[2],
            is_active=result[3]
        )

    def verify_identity(self, identity_address: str) -> bool:
        identity_address = Web3.to_checksum_address(identity_address)
        return self.contract.functions.verifyIdentity(identity_address).call()

    def update_public_key(self, identity_address: str, new_public_key: str) -> None:
        if not self.account:
            raise ValueError("Account required for updating identity")

        identity_address = Web3.to_checksum_address(identity_address)
        public_key_bytes = bytes.fromhex(new_public_key.replace('0x', ''))
        public_key_hash = Web3.keccak(public_key_bytes)

        tx = self.contract.functions.updatePublicKey(
            identity_address, public_key_hash
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 150000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def deactivate_identity(self, identity_address: str) -> None:
        if not self.account:
            raise ValueError("Account required for deactivating identity")

        identity_address = Web3.to_checksum_address(identity_address)
        tx = self.contract.functions.deactivateIdentity(identity_address).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def recover_identity(self, identity_address: str) -> None:
        if not self.account:
            raise ValueError("Account required for recovering identity")

        identity_address = Web3.to_checksum_address(identity_address)
        tx = self.contract.functions.recoverIdentity(identity_address).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.account.sign_transaction(tx)
        raw_transaction = getattr(signed_tx, 'rawTransaction', None) or getattr(signed_tx, 'raw_transaction', None)
        tx_hash = self.w3.eth.send_raw_transaction(raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_provider(self):
        return self.w3

    def get_contract(self):
        return self.contract

