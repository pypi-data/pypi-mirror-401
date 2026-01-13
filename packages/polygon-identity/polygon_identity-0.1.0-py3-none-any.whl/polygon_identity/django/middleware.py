from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import jwt
from polygon_identity import PolygonIdentity
from typing import Optional

class PolygonIdentityMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            request.identity = None
            return None

        try:
            token = auth_header.split(' ')[1]
            
            jwt_secret = getattr(request, 'polygon_identity_jwt_secret', None)
            if not jwt_secret:
                request.identity = None
                return None

            decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            identity_address = decoded.get('identityAddress')

            identity_manager = getattr(request, 'polygon_identity_manager', None)
            if not identity_manager:
                request.identity = None
                return None

            identity_data = identity_manager.get_identity(identity_address)
            
            if not identity_data.is_active:
                request.identity = None
                return None

            verified = identity_manager.verify_identity(identity_address)
            if not verified:
                request.identity = None
                return None

            request.identity = {
                'address': identity_address,
                'public_key': identity_data.public_key,
                'owner': identity_data.owner
            }

        except Exception:
            request.identity = None

        return None

