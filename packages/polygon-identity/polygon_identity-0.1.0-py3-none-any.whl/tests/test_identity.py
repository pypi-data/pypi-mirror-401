import pytest
from polygon_identity import PolygonIdentity
from polygon_identity.types import IdentityConfig

def test_identity_initialization():
    config = IdentityConfig(
        rpc_url='https://polygon-rpc.com',
        contract_address='0x0000000000000000000000000000000000000000',
        private_key='0x0000000000000000000000000000000000000000000000000000000000000001'
    )
    identity = PolygonIdentity(config)
    assert identity is not None

def test_generate_key_pair():
    config = IdentityConfig(
        rpc_url='https://polygon-rpc.com',
        contract_address='0x0000000000000000000000000000000000000000'
    )
    identity = PolygonIdentity(config)
    keys = identity.generate_key_pair()
    assert keys.private_key is not None
    assert keys.public_key is not None
    assert keys.address is not None

