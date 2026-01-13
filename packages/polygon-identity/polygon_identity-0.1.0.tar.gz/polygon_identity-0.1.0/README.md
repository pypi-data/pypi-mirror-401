# Polygon Identity

A Python package for managing blockchain-based identities on Polygon. This package provides a simple way to create, manage, and verify decentralized identities with social recovery features and zero-knowledge proof support.

## Features

- **Identity Management**: Create and manage blockchain identities
- **Social Recovery**: Recover lost identities using trusted guardians
- **Zero-Knowledge Proofs**: Generate and verify proofs without revealing secrets
- **Framework Integration**: Ready-to-use middleware for Django and FastAPI
- **Type Safety**: Full type hints for better development experience

## Installation

Install the basic package:

```bash
pip install polygon-identity
```

### Framework-specific Installation

For Django projects:

```bash
pip install polygon-identity[django]
```

For FastAPI projects:

```bash
pip install polygon-identity[fastapi]
```

For development with all tools:

```bash
pip install polygon-identity[dev]
```

## Quick Start

### Basic Usage

```python
from polygon_identity import PolygonIdentity
from polygon_identity.types import IdentityConfig

# Configure the identity manager
config = IdentityConfig(
    rpc_url='https://rpc-amoy.polygon.technology',
    contract_address='0x849c0E1b4371E033e1ccf7d1824e6A2D24Cac4B4',
    private_key='your_private_key_here'
)

# Initialize the identity manager
identity_manager = PolygonIdentity(config)

# Create a new identity
identity_address = identity_manager.create_identity()
print(f'Identity created: {identity_address}')

# Retrieve identity information
identity = identity_manager.get_identity(identity_address)
print(f'Owner: {identity.owner}')
print(f'Created: {identity.created_at}')
print(f'Active: {identity.is_active}')

# Verify an identity
is_valid = identity_manager.verify_identity(identity_address)
print(f'Identity is valid: {is_valid}')
```

### Social Recovery

```python
from polygon_identity import SocialRecovery
from polygon_identity.types import IdentityConfig

config = IdentityConfig(
    rpc_url='https://rpc-amoy.polygon.technology',
    contract_address='0x849c0E1b4371E033e1ccf7d1824e6A2D24Cac4B4',
    private_key='your_private_key_here'
)

# Initialize social recovery
recovery = SocialRecovery(
    config,
    contract_address='0x4c676A17482D95571D5602e197D1eaF93990AFd9'
)

# Set up recovery guardians
guardians = [
    '0x1234567890123456789012345678901234567890',
    '0x2345678901234567890123456789012345678901',
    '0x3456789012345678901234567890123456789012'
]
threshold = 2  # Require 2 out of 3 guardians

recovery.set_recovery_config(identity_address, guardians, threshold)

# Request recovery (if identity is lost)
recovery.request_recovery(identity_address)

# Approve recovery (as a guardian)
recovery.approve_recovery(identity_address)

# Check approval status
approval_count = recovery.get_approval_count(identity_address)
print(f'Approvals: {approval_count}/{threshold}')
```

### Zero-Knowledge Proofs

```python
from polygon_identity import ZKIdentity

zk = ZKIdentity()

# Generate a proof
secret = 'my_secret_data'
public_data = 'public_context'
proof = zk.generate_proof(secret, public_data)

print(f'Commitment: {proof.commitment}')
print(f'Proof: {proof.proof}')

# Verify the proof
is_valid = zk.verify_proof(proof, public_data)
print(f'Proof is valid: {is_valid}')
```

## Framework Integration

### FastAPI

Create a FastAPI application with identity authentication:

```python
from fastapi import FastAPI, HTTPException
from polygon_identity import PolygonIdentity
from polygon_identity.types import IdentityConfig
import os

app = FastAPI()

config = IdentityConfig(
    rpc_url=os.getenv('RPC_URL'),
    contract_address=os.getenv('CONTRACT_ADDRESS'),
    private_key=os.getenv('PRIVATE_KEY')
)

identity_manager = PolygonIdentity(config)

@app.post('/identity/create')
async def create_identity():
    try:
        address = identity_manager.create_identity()
        return {'address': address}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/identity/{address}')
async def get_identity(address: str):
    try:
        identity = identity_manager.get_identity(address)
        return {
            'owner': identity.owner,
            'public_key': identity.public_key,
            'created_at': identity.created_at,
            'is_active': identity.is_active
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
```

### Django

Add polygon identity authentication to your Django project:

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'polygon_identity.django',
]

MIDDLEWARE = [
    # ... other middleware
    'polygon_identity.django.middleware.PolygonIdentityMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'polygon_identity.django.auth_backend.PolygonIdentityBackend',
    # ... other backends
]

# Identity configuration
POLYGON_IDENTITY_CONFIG = {
    'rpc_url': 'https://rpc-amoy.polygon.technology',
    'contract_address': '0x849c0E1b4371E033e1ccf7d1824e6A2D24Cac4B4',
}
```

Then use it in your views:

```python
from django.contrib.auth.decorators import login_required
from polygon_identity.django import verify_identity

@login_required
def protected_view(request):
    # User is authenticated with their blockchain identity
    identity_address = request.user.username
    return render(request, 'protected.html', {
        'identity': identity_address
    })
```

## Configuration

### Environment Variables

Create a `.env` file in your project:

```env
RPC_URL=https://rpc-amoy.polygon.technology
CONTRACT_ADDRESS=0x849c0E1b4371E033e1ccf7d1824e6A2D24Cac4B4
SOCIAL_RECOVERY_ADDRESS=0x4c676A17482D95571D5602e197D1eaF93990AFd9
PRIVATE_KEY=your_private_key_here
```

Load them in your application:

```python
from dotenv import load_dotenv
import os

load_dotenv()

config = IdentityConfig(
    rpc_url=os.getenv('RPC_URL'),
    contract_address=os.getenv('CONTRACT_ADDRESS'),
    private_key=os.getenv('PRIVATE_KEY')
)
```

## Contract Addresses

The package is configured to work with deployed contracts on Polygon Amoy testnet:

- **IdentityManager**: `0x849c0E1b4371E033e1ccf7d1824e6A2D24Cac4B4`
- **SocialRecovery**: `0x4c676A17482D95571D5602e197D1eaF93990AFd9`

For mainnet deployment, you'll need to deploy the contracts yourself or use the official deployed addresses when available.

## API Reference

### PolygonIdentity

Main class for identity management.

#### Methods

- `create_identity(public_key: Optional[str] = None) -> str`: Create a new identity
- `get_identity(address: str) -> IdentityData`: Retrieve identity information
- `verify_identity(address: str) -> bool`: Verify if an identity is valid and active
- `update_public_key(identity_address: str, new_public_key: str) -> None`: Update identity public key
- `deactivate_identity(identity_address: str) -> None`: Deactivate an identity
- `generate_key_pair() -> IdentityKeys`: Generate a new key pair

### SocialRecovery

Class for managing social recovery.

#### Methods

- `set_recovery_config(identity_address: str, guardians: list, threshold: int) -> None`: Set up recovery guardians
- `request_recovery(identity_address: str) -> None`: Request recovery for a lost identity
- `approve_recovery(identity_address: str) -> None`: Approve a recovery request as a guardian
- `get_approval_count(identity_address: str) -> int`: Get current approval count
- `get_recovery_config(identity_address: str) -> Optional[RecoveryConfig]`: Get recovery configuration

### ZKIdentity

Class for zero-knowledge proof operations.

#### Methods

- `generate_commitment(data: str) -> str`: Generate a commitment hash
- `generate_proof(secret: str, public_data: str) -> ZKProof`: Generate a zero-knowledge proof
- `verify_proof(proof: ZKProof, public_data: str) -> bool`: Verify a zero-knowledge proof

## Examples

Check the `examples/` directory for more usage examples:

- `basic_usage.py`: Basic identity operations
- `fastapi_server.py`: FastAPI integration example

Run an example:

```bash
python examples/basic_usage.py
```

## Testing

Install development dependencies:

```bash
pip install polygon-identity[dev]
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=polygon_identity tests/
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Usamatahir23/polygon_identity_py
cd polygon_identity_py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]
```

### Code Quality

Format code with black:

```bash
black polygon_identity/
```

Run linter:

```bash
flake8 polygon_identity/
```

Type checking:

```bash
mypy polygon_identity/
```

## Security Notes

- Never commit your private keys to version control
- Always use environment variables for sensitive data
- Use testnet for development and testing
- Audit your code before deploying to mainnet
- Keep your dependencies up to date

## Troubleshooting

### Common Issues

**Issue**: `web3.exceptions.ContractLogicError`
- **Solution**: Check that you have enough MATIC in your wallet for gas fees

**Issue**: `AttributeError: 'SignedTransaction' object has no attribute 'rawTransaction'`
- **Solution**: The package handles both `rawTransaction` and `raw_transaction` attributes automatically

**Issue**: Identity creation fails
- **Solution**: Ensure your private key is correct and you're connected to the right network

### Getting Help

- Check the [examples](./examples) directory
- Review the [API documentation](#api-reference)
- Open an issue on GitHub

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for Polygon blockchain
- Inspired by decentralized identity standards
- Uses Web3.py for blockchain interactions

## Links

- [GitHub Repository](https://github.com/Usamatahir23/polygon_identity_py)
- [Polygon Documentation](https://docs.polygon.technology/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)

## Support

If you find this package useful, please consider:
- Starring the repository on GitHub
- Reporting bugs and suggesting features
- Contributing to the codebase

---

Made with ❤️ for the Polygon community
