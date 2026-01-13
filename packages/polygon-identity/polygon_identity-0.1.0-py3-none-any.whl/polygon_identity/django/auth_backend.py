from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from polygon_identity import PolygonIdentity
import jwt

User = get_user_model()

class PolygonIdentityBackend(BaseBackend):
    def authenticate(self, request, token=None, **kwargs):
        if not token:
            return None

        try:
            jwt_secret = getattr(settings, 'POLYGON_IDENTITY_JWT_SECRET', None)
            if not jwt_secret:
                return None

            decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            identity_address = decoded.get('identityAddress')

            rpc_url = getattr(settings, 'POLYGON_IDENTITY_RPC_URL', None)
            contract_address = getattr(settings, 'POLYGON_IDENTITY_CONTRACT_ADDRESS', None)
            
            if not rpc_url or not contract_address:
                return None

            from polygon_identity.types import IdentityConfig
            config = IdentityConfig(
                rpc_url=rpc_url,
                contract_address=contract_address
            )
            identity_manager = PolygonIdentity(config)

            identity_data = identity_manager.get_identity(identity_address)
            
            if not identity_data.is_active:
                return None

            verified = identity_manager.verify_identity(identity_address)
            if not verified:
                return None

            user, created = User.objects.get_or_create(
                username=identity_address,
                defaults={'email': f'{identity_address}@polygon.identity'}
            )

            return user

        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

